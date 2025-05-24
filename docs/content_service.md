# ContentService Documentation

## Overview

The `ContentService` is a core service class responsible for extracting, processing, and saving textual content from the Summer Smiles website. It acts as a content management layer that bridges the API data retrieval and local content storage systems.

## Purpose

The ContentService serves as a centralized solution for:

- **Content Extraction**: Retrieving all content from the Summer Smiles website via API
- **Data Processing**: Converting HTML content to clean, structured text
- **Content Organization**: Systematically organizing content by type and language
- **Local Storage**: Persisting processed content as JSON files for offline access and analysis

## Core Functionality

### Content Types Handled

The service processes three distinct types of content:

1. **Pages**: Static website pages containing general information
2. **Posts**: Blog posts and articles with date-based content
3. **Products**: Product listings with detailed specifications, descriptions, and related information

### Language Support

All content is processed with full bilingual support:

- **English (en)**: English language content
- **French (fr)**: French language content

Content is automatically sorted and stored in language-specific directories.

### Content Processing Pipeline

#### 1. Data Retrieval

- Utilizes the `SummerSmilesAPIService` to fetch raw content from the website API
- Handles all three content types through dedicated API endpoints
- Processes content using Pydantic models for type safety and validation

#### 2. Text Extraction

- **HTML Parsing**: Uses BeautifulSoup to parse HTML content and extract clean text
- **Recursive Processing**: Traverses nested block structures to find all text fields
- **Content Filtering**: Removes empty or insignificant content blocks
- **Plain Text Generation**: Converts HTML to readable plain text while preserving meaning

#### 3. Data Cleaning

- **Line Terminator Normalization**: Removes unusual line terminators that could cause parsing issues
- **Filename Sanitization**: Ensures safe filenames for cross-platform compatibility
- **Content Validation**: Filters out empty or invalid content blocks

#### 4. Structured Data Organization

Each content type has specialized processing:

**Pages**:

- Extracts all text blocks from page structure
- Preserves page metadata (name, link, language)
- Maintains content hierarchy

**Posts**:

- Extracts article content, title, and publication date
- Converts HTML content to clean text
- Preserves post metadata

**Products**:

- Processes comprehensive product information including:
  - Long and short descriptions
  - Product characteristics
  - Dosage information and specifications
  - Safety warnings
  - SKU information
  - Related product links
- Handles complex nested data structures (dosage tables, characteristics lists)

#### 5. File System Organization

Content is systematically organized into directory structures:

```
content/
├── english/
│   ├── pages/
│   ├── posts/
│   └── products/
└── french/
    ├── pages/
    ├── posts/
    └── products/
```

Each piece of content is saved as an individual JSON file named after the content's sanitized name.

## Key Features

### Dependency Injection

- Accepts an optional `SummerSmilesAPIService` instance for flexible testing and configuration
- Defaults to creating its own API service instance if none provided

### Error Handling

- Validates language codes and raises appropriate errors for unsupported languages
- Handles missing or malformed content gracefully
- Ensures directory structure exists before attempting file operations

### Content Management

- **Bulk Operations**: Processes all content of a given type in single operations
- **Fresh Start Capability**: Can completely clear existing content for clean re-downloads
- **Incremental Updates**: Overwrites individual files allowing for selective updates

### Data Integrity

- **UTF-8 Encoding**: Ensures proper handling of international characters
- **JSON Formatting**: Pretty-prints JSON with proper indentation for human readability
- **Non-ASCII Preservation**: Maintains original character encoding for multilingual content

## Implementation Architecture

### Service Layer Pattern

The ContentService follows the service layer architectural pattern:

- **Separation of Concerns**: Isolates content processing logic from API communication
- **Single Responsibility**: Focused solely on content extraction and storage
- **Dependency Management**: Clean integration with other service components

### Data Flow

1. **API Integration**: Receives data from SummerSmilesAPIService
2. **Model Processing**: Works with Pydantic models for type safety
3. **Content Transformation**: Converts structured API data to flat text content
4. **File System Persistence**: Saves processed content to organized directory structure

### Scalability Considerations

- **Memory Efficient**: Processes content iteratively rather than loading everything into memory
- **File-based Storage**: Uses individual files for easy content management and updates
- **Language Isolation**: Separate processing paths prevent cross-language contamination

## Configuration Dependencies

The service relies on several external configurations:

- **Path Constants**: Predefined directory paths for content organization
- **API Service**: SummerSmilesAPIService for data retrieval
- **Utility Functions**: Helper functions for filename sanitization and text cleaning
- **Logging Configuration**: Structured logging for operation monitoring and debugging
