# Summer Smiles AI Chatbot

A FastAPI-powered chatbot system that provides intelligent customer support using OpenAI's GPT models with content-aware responses. The system processes Summer Smiles website content and provides bilingual (English/French) chat functionality grounded in actual company information.

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd SummerSmilesChatbot

# Create and activate virtual environment
python -m venv .venv
. .venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:
Use the `.env.example` as a template:

```bash
# Copy the example file
cp .env.example .env
# Edit the .env file to include your OpenAI API key
nano .env
```

### 3. Start the API Server

```bash
# Start the FastAPI server using the provided script
python run_api.py
```

The API will be available at `http://127.0.0.1:8000`

### 4. Test the API

**Option 1: Interactive Test Client**

```bash
python tests/test_api_client.py
```

This provides an interactive chat interface with language selection and context preservation in the terminal calling the API.
This is useful for quick testing and provides an example of how to interact with the API programmatically.

**Option 2: Direct API Calls**

Visit `http://127.0.0.1:8000/docs` for interactive API documentation, or test with curl:

```bash
# Establish initial connection
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"language": "en"}'

# Send a chat message
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Hello, how can you help me?", "language": "en"}'

# Send follow-up message with context
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Tell me more about that", "language": "en", "previous_response_id": "response-id-from-previous-call"}'
```

## Features

- **AI-Powered Chat**: GPT-4o-mini with file search capabilities
- **Content-Aware**: Responses grounded in actual Summer Smiles website content
- **Bilingual Support**: English and French language options
- **Context Preservation**: Maintains conversation history
- **Single Endpoint Design**: Streamlined API with one endpoint for all chat interactions

## API Endpoints

- `GET /` - API information
- `POST /chat` - Handle both initial connection and chat messages
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## System Architecture

The system consists of three main services:

1. **ContentService** - Extracts and processes website content
2. **SummerSmilesAPIService** - Fetches data from Summer Smiles website
3. **OpenAIService** - Manages AI chat and vector stores

## Documentation

Detailed documentation available in the `docs/` folder:

- [ContentService Documentation](docs/content_service.md)
- [SummerSmilesAPIService Documentation](docs/summer_smiles_api_service.md)
- [OpenAIService Documentation](docs/openai_service.md)
- [API Documentation](docs/api_docs.md)
- [Vector Store Management](docs/vector_store_management.md)

## Development

The server supports auto-reload during development. Any code changes will automatically restart the server when running with `python run_api.py`.

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for content updates and AI API calls
