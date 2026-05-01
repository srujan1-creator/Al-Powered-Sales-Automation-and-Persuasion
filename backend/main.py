from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import APIKeyHeader
import logging
import models, schemas, ai_engine
from database import engine, get_db
from config import settings

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("aura-api")

# API Key Security
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if not api_key or api_key != settings.backend_api_key:
        logger.warning(f"Unauthorized access attempt with key: {api_key}")
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

models.Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Aura AI Sales Assistant API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

@api_router.post("/context", response_model=schemas.ConversationResponse, dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")
def create_context(request: Request, context: schemas.LeadContextCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new context for industry: {context.industry}")
    try:
        # 1. Create Context
        db_context = models.LeadContext(**context.model_dump())
        db.add(db_context)
        db.commit()
        db.refresh(db_context)
        
        # 2. Create Conversation
        db_conversation = models.Conversation(context_id=db_context.id, lead_score=50.0)
        db.add(db_conversation)
        db.commit()
        db.refresh(db_conversation)
        
        # 3. Generate Intro Pitch using AI
        intro_text = ai_engine.generate_intro_pitch(
            context.company_size, 
            context.industry, 
            context.pain_points
        )
        
        # 4. Save AI message
        db_message = models.Message(
            conversation_id=db_conversation.id,
            sender="ai",
            content=intro_text
        )
        db.add(db_message)
        db.commit()
        
        # Refresh conversation to include messages
        db.refresh(db_conversation)
        return db_conversation
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error during context creation")

@api_router.post("/chat", response_model=schemas.ConversationResponse, dependencies=[Depends(verify_api_key)])
@limiter.limit("20/minute")
def send_message(request: Request, req: schemas.ChatRequest, db: Session = Depends(get_db)):
    logger.info(f"Processing chat message for conversation: {req.conversation_id}")
    db_conversation = db.query(models.Conversation).filter(models.Conversation.id == req.conversation_id).first()
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    try:
        # 1. Save User Message
        user_message = models.Message(conversation_id=req.conversation_id, sender="user", content=req.message)
        db.add(user_message)
        db.commit()
        
        # 2. Get Chat History
        messages = db.query(models.Message).filter(models.Message.conversation_id == req.conversation_id).order_by(models.Message.timestamp).all()
        history = [{"sender": m.sender, "content": m.content} for m in messages]
        
        # 3. Generate AI Response
        ai_response_text = ai_engine.generate_sales_response(history, req.message)
        
        # 4. Save AI Response
        ai_message = models.Message(conversation_id=req.conversation_id, sender="ai", content=ai_response_text)
        db.add(ai_message)
        db.commit()
        
        # 5. Update Lead Score
        messages = db.query(models.Message).filter(models.Message.conversation_id == req.conversation_id).order_by(models.Message.timestamp).all()
        full_history = [{"sender": m.sender, "content": m.content} for m in messages]
        new_score = ai_engine.analyze_lead_score(full_history)
        db_conversation.lead_score = new_score
        db.commit()
        
        db.refresh(db_conversation)
        return db_conversation
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error during chat processing")

@api_router.get("/conversation/{conversation_id}", response_model=schemas.ConversationResponse, dependencies=[Depends(verify_api_key)])
@limiter.limit("60/minute")
def get_conversation(request: Request, conversation_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching conversation: {conversation_id}")
    db_conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation

from fastapi.staticfiles import StaticFiles
import os

app.include_router(api_router)

# Serve Frontend Static Files
frontend_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
else:
    logger.warning(f"Frontend static directory not found at {frontend_path}")
