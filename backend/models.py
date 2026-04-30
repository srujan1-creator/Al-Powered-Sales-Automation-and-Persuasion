from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from database import Base

class LeadContext(Base):
    """
    Represents the business context of a lead.
    Stores company size, industry, and pain points used for AI personalization.
    """
    __tablename__ = "lead_contexts"

    id = Column(Integer, primary_key=True, index=True)
    company_size = Column(String)
    industry = Column(String)
    pain_points = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    conversations = relationship("Conversation", back_populates="context")

class Conversation(Base):
    """
    Represents a chat session with a lead.
    Tracks the AI-assigned lead score and the status of the conversation.
    """
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    context_id = Column(Integer, ForeignKey("lead_contexts.id"), index=True)
    lead_score = Column(Float, default=0.0) # 0 to 100
    status = Column(String, default="active") # active, converted, lost
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    context = relationship("LeadContext", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    """
    Represents a single message in a conversation.
    Can be sent by either the 'user' or the 'ai'.
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    sender = Column(String) # 'user' or 'ai'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    conversation = relationship("Conversation", back_populates="messages")
