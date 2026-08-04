from datetime import datetime
from app.config import SYSTEM_DIR, MEMORY_DIR

def read_file_safe(path):
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""

def build_system_prompt() -> str:
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S (%A)")
    daily_memory_file = MEMORY_DIR / f"{today_str}.md"
    
    soul = read_file_safe(SYSTEM_DIR / "SOUL.md")
    user_prof = read_file_safe(SYSTEM_DIR / "USER.md")
    agents_rules = read_file_safe(SYSTEM_DIR / "AGENTS.md")
    tools_info = read_file_safe(SYSTEM_DIR / "TOOLS.md")
    long_memory = read_file_safe(SYSTEM_DIR / "MEMORY.md")
    daily_memory = read_file_safe(daily_memory_file)
    
    prompt_parts = [
        f"### CURRENT TIME & DATE\nCurrent system time is: {current_time_str}",
        "### AGENT PERSONA & SOUL", soul,
        "### USER PROFILE", user_prof,
        "### SYSTEM & SAFETY RULES", agents_rules,
        "### INFRASTRUCTURE & TOOLS INFO", tools_info,
        "### LONG-TERM MEMORY", long_memory,
        f"### TODAY'S CONTEXT ({today_str})", daily_memory if daily_memory else "No notes for today yet."
    ]
    
    return "\n\n".join(prompt_parts)
