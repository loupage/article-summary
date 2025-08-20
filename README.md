# Article Summarizer

A Python-based article summarizer that supports multiple AI providers for generating structured summaries of blog posts and articles.

## Features

- **Multiple AI Provider Support**: Choose between Ollama (local), OpenAI, or Anthropic
- **Structured Output**: Generates summaries in a consistent markdown format
- **Clipboard Integration**: Automatically copies summaries to your clipboard
- **Beginner-Friendly**: Well-commented code for learning purposes

## Supported AI Providers

- **Ollama** (Local): Runs AI models locally on your machine
- **OpenAI**: Uses OpenAI's GPT models via API
- **Anthropic**: Uses Claude models via API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/loupage/article-summary.git
cd article-summary
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Configuration

### API Keys

Create a `.env` file based on `.env.example` and add your API keys:

```bash
# For OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# For Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Ollama Setup

For local Ollama usage:

1. Install Ollama from [https://ollama.ai/](https://ollama.ai/)
2. Pull the required model:
```bash
ollama pull gemma3:latest
```
3. Ensure Ollama is running (it starts automatically after installation)

## Usage

Run the script:
```bash
python article_summarizer.py
```

Or make it executable:
```bash
chmod +x article_summarizer.py
./article_summarizer.py
```

### How to Use

1. **Select AI Provider**: Choose between Ollama (1), OpenAI (2), or Anthropic (3)
2. **Input Article**: Paste your article text and press `Ctrl+D` when finished
3. **Get Summary**: The AI will generate a structured summary
4. **Auto-Copy**: Summary is automatically copied to your clipboard

## Summary Format

The tool generates summaries in this structure:

```markdown
> [!Abstract]- 
>**Summary:**
  >>[One-sentence overview of the article's main point in 30-45 words.] 
  >
>**The details:** 
  > - [Key point #1]
  > - [Key point #2]
  > - [Key point #3]
>
>**Why it matters:**                                                                                  
     >>[Briefly explain the significance or impact of the article's content.]
```

## Dependencies

- `requests`: HTTP client for API calls
- `pyperclip`: Clipboard operations
- `python-dotenv`: Environment variable management

## Error Handling

The application includes comprehensive error handling for:
- Network connectivity issues
- API authentication failures
- Invalid response formats
- Missing environment variables
- Ollama service availability

## Development

This project includes detailed comments throughout the code to help beginners understand:
- How to integrate with different AI APIs
- Error handling best practices
- Environment variable management
- JSON response parsing

For development guidance, see `CLAUDE.md`.

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.