import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SYSTEM_DIR = BASE_DIR / "system"
MEMORY_DIR = BASE_DIR / "memory"
PERSONAL_DIR = BASE_DIR / "personal"
PERSONAL_USER_FILE = PERSONAL_DIR / "PERSONAL_USER_INFO.md"

MEMORY_DIR.mkdir(exist_ok=True)

PERSONAL_DIR.mkdir(parents=True, exist_ok=True)
if not PERSONAL_USER_FILE.exists():
    PERSONAL_USER_FILE.write_text(
        "# Personal Sensitive User Info\n\n## Private Facts\n", 
        encoding="utf-8"
    )

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DEFAULT_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "anthropic")
