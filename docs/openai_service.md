# OpenAIService Documentation

## Overview

The `OpenAIService` is an AI integration service that provides intelligent chat functionality powered by OpenAI's GPT models with file search capabilities. It serves as the bridge between the Summer Smiles content and AI-powered user interactions.

## Purpose

The OpenAIService provides:

- **Intelligent Chat**: Context-aware conversations using GPT models with file search
- **Vector Store Management**: Creation, updating, and maintenance of content knowledge bases
- **Multilingual Support**: Separate vector stores for English and French content
- **Content-Aware Responses**: AI responses informed by actual website content

## Core Functionality

### Chat Interface

- **Context-Aware Conversations**: Uses system prompts to maintain Summer Smiles brand voice and knowledge
- **File Search Integration**: Leverages vector stores to ground responses in actual website content
- **Conversation Continuity**: Supports multi-turn conversations with previous response tracking
- **Response Logging**: Comprehensive logging of AI interactions and context usage

### Vector Store Management

The service manages knowledge bases containing processed website content:

**Vector Store Operations**:

- **Creation**: Establishes new vector stores for different languages or content types
- **Updates**: Refreshes vector stores with latest content from ContentService
- **File Upload**: Processes and uploads content files to make them searchable
- **Retrieval**: Accesses stored content during chat sessions for context

**Language-Specific Stores**:

- **English Store**: Contains all English content (pages, posts, products)
- **French Store**: Contains all French content for bilingual support
- **Store Selection**: Automatically routes queries to appropriate language store

**NOTE**: The management of the vector stores within the api is controlled by the **NAME** of the vector store, not the **ID**. If there is more than 1 vector store with the same name in the account, it will cause an error in the API.

## Implementation Architecture

### AI Integration Layer

- **OpenAI Client**: Managed connection to OpenAI API with proper authentication
- **Model Configuration**: Optimized for chat with file search using GPT-4o-mini
- **Tool Integration**: File search tool integration for content-grounded responses
- **Error Handling**: Graceful handling of API failures and rate limits

### Content Integration

- **Vector Store Mapping**: Maintains mapping between store names and IDs for efficient access
- **File Management**: Handles content file uploads and updates through utility functions
- **Content Synchronization**: Coordinates with ContentService for fresh content updates

### Response Processing

- **Context Extraction**: Logs and tracks which content pieces influenced responses
- **Response Tracking**: Maintains conversation continuity through response IDs
- **Query Analysis**: Logs search queries used by the AI for transparency

## Key Features

### Intelligent Responses

- **Brand Voice**: Maintains consistent Summer Smiles brand personality through system prompts
- **Content Grounding**: Responses based on actual website content rather than general knowledge
- **Accuracy**: Reduces hallucinations by constraining responses to available content
- **Relevance**: Context-aware responses that understand user intent

### Content Management

- **Automatic Updates**: Vector stores can be refreshed when content changes
- **Efficient Storage**: Optimized vector representations for fast content retrieval
- **File Organization**: Systematic upload and management of content files
- **Version Control**: Supports updating content while maintaining service availability

### Monitoring and Debugging

- **Comprehensive Logging**: Detailed logs of AI interactions and context usage
- **Query Tracking**: Visibility into what content the AI accessed for each response
- **Performance Monitoring**: Response times and API usage tracking
- **Error Reporting**: Clear error handling and reporting for troubleshooting

## Configuration Dependencies

### External Dependencies

- **OpenAI API**: GPT model access and vector store functionality
- **Environment Variables**: Secure API key management through environment configuration
- **System Prompts**: Centralized prompt management for consistent AI behavior
- **Utility Functions**: Specialized functions for vector store operations

### Content Integration

- **ContentService**: Source of processed website content for vector stores
- **File System**: Access to processed content files for upload and management
- **Language Detection**: Routing logic for multilingual support

## Integration Patterns

The OpenAIService integrates with the broader system through:

- **Content Pipeline**: Receives processed content from ContentService for vector store updates
- **API Layer**: Can be exposed through web APIs for chat interfaces
- **Logging System**: Integrated monitoring and debugging through centralized logging
- **Configuration Management**: Environment-based configuration for different deployment scenarios
