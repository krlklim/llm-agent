# Project Setup & Usage Guide

## Overview

This project is an AI-powered assistant that integrates with multiple LLM providers (Gemini, Anthropic, OpenAI) to deliver intelligent task automation and personal assistance across software engineering and lifestyle management.

---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### 1. Install Dependencies

First, install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install all necessary dependencies defined in the `requirements.txt` file.

### 2. Configure API Keys

Before running the project, you need to set up your environment variables with your API keys:

1. **Rename the configuration file**:
   ```bash
   mv .env.example .env
   ```

2. **Edit the `.env` file** and add your API keys for the providers you plan to use:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Only include the API keys for the providers you intend to use.

---

## Running the Project

### Basic Usage

To run the project with the default provider (Gemini):

```bash
python3 main.py
```

### Specifying a Different Provider

Use the `-p` or `--provider` flag to choose which LLM provider to use:

```bash
python3 main.py -p anthropic
```

### Available Providers

- **gemini** (default) - Google's Gemini model
- **anthropic** - Anthropic's Claude model
- **openai** - OpenAI's GPT model

### Examples

```bash
# Use Anthropic Claude
python3 main.py -p anthropic

# Use OpenAI GPT
python3 main.py -p openai

# Use default Gemini
python3 main.py
```

---

## Project Structure

```
project-root/
├── README.md                      # This file
├── main.py                        # Entry point - CLI interface with provider selection
├── requirements.txt               # Python dependencies
├── .env.example                   # Example environment configuration template
├── .env                           # Your actual API keys (create from .env.example)
│
├── app/                           # Main application package
│   ├── __init__.py
│   ├── config.py                  # Configuration, API keys, and directory paths
│   ├── context.py                 # System prompt builder and context management
│   ├── llm.py                     # LLM client with provider integration (OpenAI, Anthropic, Gemini)
│   │
│   └── tools/                     # Tool implementations for LLM
│       ├── file_system.py         # File read/write and user profile management
│       ├── web_tools.py           # Web search, page fetching, YouTube transcripts
│       └── schemas.py             # Tool definitions and schemas for LLM providers
│
├── system/                        # System configuration and persona files
│   ├── USER.md                    # User profile and preferences
│   ├── MEMORY.md                  # Long-term memory and lessons learned
│   ├── SOUL.md                    # Agent persona, tone, and core mission
│   ├── AGENTS.md                  # Execution rules and safety guidelines
│   └── TOOLS.md                   # Available tools and infrastructure info
│
└── memory/                        # Daily conversation logs
    └── YYYY-MM-DD.md              # Daily interaction records (auto-generated)
```

### Key Directories Explained

- **`app/`** - Core application logic with LLM integration and tool handlers
- **`system/`** - Agent configuration files that define personality, rules, and user preferences
- **`memory/`** - Persistent daily logs of conversations and interactions (auto-created)

---

## Troubleshooting

- **Missing dependencies**: Make sure you've run `pip install -r requirements.txt`
- **API key errors**: Verify your `.env` file is properly configured with valid API keys
- **Provider not recognized**: Check that you're using one of the supported providers: `gemini`, `anthropic`, or `openai`

---

## Support

For issues or questions, refer to the project documentation or check the logs in the `memory/` directory for detailed interaction history.
