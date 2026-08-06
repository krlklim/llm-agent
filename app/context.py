from datetime import datetime
from app.config import SYSTEM_DIR, MEMORY_DIR, PERSONAL_USER_FILE

DAILY_MEMORY_LIMIT = 5

def read_file_safe(path):
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""

def load_recent_daily_memories(memory_dir, limit: int = DAILY_MEMORY_LIMIT) -> str:
    if not memory_dir.exists():
        return "No recent memory logs available."

    daily_files = sorted(memory_dir.glob("????-??-??.md"))
    
    if not daily_files:
        return "No daily memory logs found."

    recent_files = daily_files[-limit:]
    
    recent_memories = []
    for file_path in recent_files:
        content = read_file_safe(file_path)
        if content:
            recent_memories.append(f"--- Log: {file_path.name} ---\n{content}")

    return "\n\n".join(recent_memories)

def build_system_prompt() -> str:
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S (%A)")
    daily_memory_file = MEMORY_DIR / f"{today_str}.md"
    
    soul = read_file_safe(SYSTEM_DIR / "SOUL.md")
    user_prof = read_file_safe(SYSTEM_DIR / "USER.md")
    personal_prof = read_file_safe(PERSONAL_USER_FILE)
    agents_rules = read_file_safe(SYSTEM_DIR / "AGENTS.md")
    tools_info = read_file_safe(SYSTEM_DIR / "TOOLS.md")
    daily_memory = read_file_safe(daily_memory_file)
    long_memory = read_file_safe(SYSTEM_DIR / "MEMORY.md")
    
    recent_daily_memories = load_recent_daily_memories(MEMORY_DIR, limit=DAILY_MEMORY_LIMIT)
    
    prompt_parts = [
        f"### CURRENT TIME & DATE\nCurrent system time is: {current_time_str}",
        "### AGENT PERSONA & SOUL", soul,
        "### PUBLIC USER PROFILE", user_prof,
        "### PRIVATE & CONFIDENTIAL USER PROFILE", personal_prof,
        "### SYSTEM & SAFETY RULES", agents_rules,
        "### INFRASTRUCTURE & TOOLS INFO", tools_info,
        "### LONG-TERM MEMORY", long_memory,
        f"### TODAY'S CONTEXT ({today_str})", daily_memory if daily_memory else "No notes for today yet.",
        "### RECENT DAILY MEMORIES (LAST FEW DAYS)", recent_daily_memories,
    ]
    
    return "\n\n".join(prompt_parts)
