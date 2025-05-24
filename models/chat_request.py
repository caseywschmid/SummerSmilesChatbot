from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    """
    user_input: Optional[str] = None  # Optional to support initial connection
    language: str = "en"  # Default to English
    previous_response_id: Optional[str] = None  # Optional


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""

    response_text: str
    response_id: Optional[str]
    language: str
