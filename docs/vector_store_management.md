# Vector Store Management Documentation

## Overview

This document explains how to refresh content and update vector stores for the Summer Smiles AI Chatbot. The system uses a two-step process: first extracting fresh content from the website, then uploading that content to OpenAI vector stores for AI-powered search.

## Content Types

The system currently manages three types of content:
- **Pages**: Website pages (static content)
- **Posts**: Blog posts and articles
- **Products**: Product listings and information

Each content type can be updated individually or all together, and supports both English and French languages.

## Process Overview

### Step 1: Content Extraction
Extract fresh content from the Summer Smiles website and save to local `content/` directory.

### Step 2: Vector Store Creation
Upload the extracted content files to OpenAI vector stores for AI-powered search functionality.

## Content Extraction Scripts

### Refresh All Content

**Script**: `scripts/refresh_all_content.py`

**Purpose**: Complete content refresh - deletes all existing content and re-extracts everything. Saves all updated content in the `content/` directory.

**Usage**:
```bash
python -m scripts.refresh_all_content
```

**What it does**:
1. Deletes all existing content from `content/` directory
2. Extracts and saves all pages content
3. Extracts and saves all posts content  
4. Extracts and saves all products content

**When to use**: When you want a complete refresh of all content types.

### Individual Content Type Scripts

For updating specific content types individually:

**Pages Only**:
```bash
python -m scripts.refresh_pages_content
```

**Posts Only**:
```bash
python -m scripts.refresh_posts_content
```

**Products Only**:
```bash
python -m scripts.refresh_products_content
```

**When to use**: When you know only specific content has changed (e.g., new blog posts but pages unchanged).

## Vector Store Management

### Create/Update Vector Stores

**Script**: `scripts/create_vector_store_from_content.py`

**Purpose**: Creates or updates OpenAI vector stores with the content from the `content/` directory.

**Usage**:
```bash
python -m scripts.create_vector_store_from_content [STORE_NAME]
```

**Available Store Names**:
- `SummerSmiles_English` - Production English content
- `SummerSmiles_English_DEV` - Development English content (staged)
- `SummerSmiles_French` - Production French content
- `SummerSmiles_French_DEV` - Development French content (staged)

**Examples**:
```bash
# Update production English vector store
python -m scripts.create_vector_store_from_content SummerSmiles_English

# Update development French vector store
python -m scripts.create_vector_store_from_content SummerSmiles_French_DEV
```

**What it does**:
1. Checks if the vector store already exists
2. If exists, prompts for confirmation to delete and recreate
3. Uploads all files from `content/` directory to the vector store
4. Displays the new vector store ID when complete

**Note**: There are more sophisticated options available for vector store updates, but this script is designed for simplicity and full recreation.

**Important Notes**:
- **Destructive Operation**: If a vector store exists, it will be completely deleted and recreated
- **Confirmation Required**: Script will prompt before deleting existing stores
- **All Languages**: The script uploads content for all languages to the specified store

## Complete Workflow Examples

### Full Production Update

When you want to update everything in production:

```bash
# Step 1: Refresh all content from website
python -m scripts.refresh_all_content

# Step 2: Update English production vector store
python -m scripts.create_vector_store_from_content SummerSmiles_English

# Step 3: Update French production vector store
python -m scripts.create_vector_store_from_content SummerSmiles_French
```

### Development Testing

When testing changes in development:

```bash
# Step 1: Refresh specific content type (if needed)
python -m scripts.refresh_posts_content

# Step 2: Update development vector store
python -m scripts.create_vector_store_from_content SummerSmiles_English_DEV
```

### Partial Content Update

When only blog posts have changed:

```bash
# Step 1: Refresh only posts
python -m scripts.refresh_posts_content

# Step 2: Update vector stores (both languages if needed)
python -m scripts.create_vector_store_from_content SummerSmiles_English
python -m scripts.create_vector_store_from_content SummerSmiles_French
```

## File Structure

After content extraction, the `content/` directory contains:

```
content/
├── pages/
│   ├── english/
│   └── french/
├── posts/
│   ├── english/
│   └── french/
└── products/
    ├── english/
    └── french/
```

Each file contains processed content ready for vector store upload.

## Future Automation

### Potential Improvements

1. **Automated Content Detection**: Scripts that detect which content types have changed
2. **API Endpoints**: Web API for triggering content updates remotely
3. **Scheduled Updates**: Automatic content refresh on schedule
4. **Incremental Updates**: Update only changed content instead of full recreation
5. **Rollback Capability**: Backup and restore vector stores

### Integration Opportunities

- **Webhook Integration**: Trigger updates when website content changes
- **CI/CD Pipeline**: Automated updates in deployment pipeline
- **Monitoring Dashboard**: Web interface for content and vector store status
- **Multi-Environment**: Enhanced dev/staging/production workflow

## Dependencies

### Required Services
- **ContentService**: For extracting website content
- **OpenAIService**: For vector store management
- **SummerSmilesAPIService**: For website data access

### Environment Requirements
- **OpenAI API Key**: Must be configured in environment
- **Internet Access**: For website content extraction and OpenAI API
- **File System Access**: For reading/writing content files 