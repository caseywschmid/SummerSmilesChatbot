# Summer Smiles FastAPI Chatbot

A FastAPI version of the Summer Smiles chatbot that provides the same functionality as the terminal version through a REST API.

## Features

- **Language Support**: English and French (en/fr)
- **Context Preservation**: Maintains conversation context using `previous_response_id`
- **Vector Store Integration**: Uses the same OpenAIService as the terminal chatbot
- **Single Endpoint Design**: One endpoint handles both initial connection and chat messages
- **CORS Support**: Ready for web frontend integration
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## API Endpoints

### GET `/`
Root endpoint with API information and available endpoints.

### POST `/chat`
Handle both initial connection and chat messages.

**For Initial Connection** (no user_input):
- **Request Body**:
  ```json
  {
    "language": "en"
  }
  ```
- **Response**:
  ```json
  {
    "response_text": "Hello! How can I help you today?",
    "response_id": null,
    "language": "en"
  }
  ```

**For Regular Chat Messages**:
- **Request Body**:
  ```json
  {
    "user_input": "Your message here",
    "language": "en",
    "previous_response_id": "optional-context-id"
  }
  ```
- **Response**:
  ```json
  {
    "response_text": "Bot response",
    "response_id": "unique-response-id",
    "language": "en"
  }
  ```

### GET `/health`
Health check endpoint for monitoring.

### GET `/docs`
Interactive API documentation (Swagger UI).

## Setup and Usage

### 1. Start the FastAPI Server

```bash
# Option 1: Using the startup script
python run_api.py

# Option 2: Using uvicorn directly
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

The server will start at `http://127.0.0.1:8000`

### 2. Test with the Interactive Client

```bash
python test_api_client.py
```

### 3. Use the API Documentation

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Example Usage

### Establish Initial Connection
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "language": "en"
  }'
```

### Send Chat Message
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Hello, how are you?",
    "language": "en"
  }'
```

### Maintain Context
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Can you tell me more about that?",
    "language": "en",
    "previous_response_id": "response-id-from-previous-call"
  }'
```

### French Language Example
```bash
# Initial connection in French
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "language": "fr"
  }'

# Chat message in French
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Bonjour, comment allez-vous?",
    "language": "fr"
  }'
```

## Architecture

The FastAPI chatbot uses a simplified single-endpoint design with the same core components as the terminal version:

- **OpenAIService**: Handles AI interactions and vector store management
- **Vector Stores**: Language-specific knowledge bases (SummerSmiles_English, SummerSmiles_French)
- **Context Management**: Maintains conversation context using response IDs
- **Automatic Language Routing**: Routes requests to appropriate vector stores based on language parameter
- **Initial Connection Detection**: Automatically detects first messages (no user_input) and provides welcome messages

## Flow

1. **Initial Connection**: Send POST request to `/chat` with only `language` parameter
2. **Welcome Message**: Receive welcome message in selected language (no response_id)
3. **Chat Messages**: Send messages with `user_input`, `language`, and optional `previous_response_id`
4. **Context Preservation**: Use `response_id` from previous responses to maintain conversation context

## Development

The FastAPI server supports auto-reload during development. Any changes to the code will automatically restart the server.

## Production Considerations

- Configure CORS origins appropriately for your frontend domain
- Set up proper logging and monitoring
- Consider rate limiting and authentication
- Use environment variables for configuration
- Deploy with a production ASGI server like Gunicorn + Uvicorn 