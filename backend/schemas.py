from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    sender: str = Field(..., description="Sender of the message, 'user' or 'ai'")
    content: str = Field(..., min_length=1, description="Content of the message")

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class LeadContextBase(BaseModel):
    company_size: str = Field(..., min_length=1, max_length=50, description="Size of the lead's company")
    industry: str = Field(..., min_length=1, max_length=100, description="Industry of the lead")
    pain_points: str = Field(..., min_length=1, max_length=1000, description="Pain points described by the lead")

class LeadContextCreate(LeadContextBase):
    pass

class LeadContextResponse(LeadContextBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    context_id: int
    lead_score: float = Field(default=0.0, ge=0.0, le=100.0)
    status: str
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    conversation_id: int = Field(..., description="ID of the conversation to append the message to")
    message: str = Field(..., min_length=1, description="Message content from the user")
