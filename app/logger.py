import json
from datetime import datetime
from pathlib import Path  # <--- Теперь используется ниже
from typing import Any
from app.config import BASE_DIR

LOGS_DIR = Path(BASE_DIR) / "logs"
LOGS_DIR.mkdir(exist_ok=True, parents=True)

def log_raw_interaction(provider: str, model: str, request_data: dict, response_data: Any):
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    timestamp_str = now.strftime("%H:%M:%S")
    
    log_file: Path = LOGS_DIR / f"{today_str}.log"

    def serialize_default(obj):
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)

    entry = (
        f"\n================================================================================\n"
        f"TIMESTAMP: [{timestamp_str}] | PROVIDER: {provider.upper()} | MODEL: {model}\n"
        f"================================================================================\n"
        f"--- RAW REQUEST DATA ---\n"
        f"{json.dumps(request_data, indent=2, ensure_ascii=False, default=serialize_default)}\n\n"
        f"--- RAW RESPONSE DATA ---\n"
        f"{json.dumps(response_data, indent=2, ensure_ascii=False, default=serialize_default)}\n"
    )

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)