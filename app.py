# FastAPI chatbot using the OpenAIService
# Step-by-step:
# 1. Use OpenAIService for handling chat requests (same as terminal version)
# 2. Support language selection through vector store names
# 3. Maintain session context with previous_response_id
# 4. Detect first message (no user_input) and provide welcome message
# 5. Provide endpoints for chat and health check

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.ai.openai_service import OpenAIService
from models.chat_request import ChatRequest, ChatResponse
import logging
from services.logger import configure_logging
log = configure_logging(__name__, log_level=logging.DEBUG)

app = FastAPI(
    title="Summer Smiles Chatbot API",
    description="FastAPI version of the Summer Smiles chatbot with language support",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_service = OpenAIService()


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Summer Smiles Chatbot API",
        "endpoints": {
            "/chat": "POST - Send a chat message or establish initial connection",
            "/health": "GET - Health check",
            "/docs": "API documentation",
        },
    }


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Handle chat requests using OpenAIService
    """
    try:
        if request.language not in ("en", "fr"):
            raise HTTPException(
                status_code=400, detail="Invalid language. Supported: en, fr"
            )

        # Determine vector store name based on language
        # NOTE: Vector stores are already created and available
        if request.language == "en":
            vector_store_name = "SummerSmiles_English"
        else:
            vector_store_name = "SummerSmiles_French"

        if not request.user_input or request.user_input.strip() == "":
            if request.language == "en":
                welcome_message = "Hello! How can I help you today?"
            else:
                welcome_message = "Bonjour! Comment puis-je vous aider aujourd'hui?"

            return ChatResponse(
                response_text=welcome_message,
                response_id=None,
                language=request.language,
            )

        response_text, response_id = openai_service.chat(
            user_input=request.user_input,
            previous_response_id=request.previous_response_id,
            name=vector_store_name,
        )

        return ChatResponse(
            response_text=response_text,
            response_id=response_id,
            language=request.language,
        )

    except Exception as e:
        log.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "Summer Smiles Chatbot API"}
