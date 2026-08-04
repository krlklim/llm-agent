import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SYSTEM_DIR = BASE_DIR / "system"
MEMORY_DIR = BASE_DIR / "memory"

MEMORY_DIR.mkdir(exist_ok=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DEFAULT_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "gemini")
