# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based article summarizer that supports multiple AI providers (Ollama, OpenAI, and Anthropic). The tool takes article text input from the user and generates structured summaries using a consistent markdown format.

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (create .env file)
# Required for OpenAI: OPENAI_API_KEY=your_key_here
# Required for Anthropic: ANTHROPIC_API_KEY=your_key_here
# Ollama requires local installation and running service
```

### Running the Application
```bash
# Run the main script
python article_summarizer.py

# Or make it executable and run directly
chmod +x article_summarizer.py
./article_summarizer.py
```

## Architecture

### Core Components

- **Provider Selection (`select_ai_provider()`)**: Interactive menu for choosing between Ollama (local), OpenAI, or Anthropic
- **Input Handling (`get_user_input()`)**: Reads multi-line article text until EOF (Ctrl+D)
- **Prompt Engineering (`create_summary_prompt()`)**: Creates structured prompt with specific markdown format requirements
- **AI Provider Interfaces**: 
  - `query_ollama()`: Local Ollama API calls (default: gemma3:latest)
  - `query_openai()`: OpenAI API integration (default: gpt-4)
  - `query_anthropic()`: Anthropic API integration (default: claude-3-sonnet)
- **Output Processing (`copy_to_clipboard()`)**: Automatically copies summary to system clipboard

### Summary Format

The tool enforces a specific markdown structure:
- Abstract section with one-sentence summary (30-45 words)
- Details section with 3-5 bullet points
- "Why it matters" section explaining significance

### Dependencies

- `requests`: HTTP client for API calls
- `pyperclip`: Clipboard operations
- `python-dotenv`: Environment variable management

### Error Handling

Each provider has specific error handling for:
- Connection errors (especially Ollama service availability)
- Authentication failures (API keys)
- Response format validation
- JSON parsing errors