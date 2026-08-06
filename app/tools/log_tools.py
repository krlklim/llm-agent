import re
from collections import deque
from pathlib import Path
from app.config import LOGS_DIR

LOG_LINES_LIMIT = 250

def read_logs(lines: int = LOG_LINES_LIMIT, level: str = None) -> str:
    if not LOGS_DIR.exists():
        return "Error: Logs directory does not exist."

    log_files = sorted(
        [f for f in LOGS_DIR.glob("*") if f.suffix in [".log", ".md"]],
        key=lambda x: x.stat().st_mtime
    )

    if not log_files:
        return "No log files found in logs/ directory."

    latest_log_file = log_files[-1]

    try:
        with open(latest_log_file, "r", encoding="utf-8", errors="replace") as f:
            if level:
                level_pattern = re.compile(re.escape(level), re.IGNORECASE)
                filtered_lines = [line for line in f if level_pattern.search(line)]
                tail_lines = list(deque(filtered_lines, maxlen=lines))
            else:
                tail_lines = list(deque(f, maxlen=lines))

        if not tail_lines:
            return f"No log entries found in '{latest_log_file.name}' matching level/filter '{level}'."

        header = f"=== Log File: {latest_log_file.name} (Last {len(tail_lines)} lines) ===\n\n"
        return header + "".join(tail_lines)

    except Exception as e:
        return f"Error reading log file '{latest_log_file.name}': {str(e)}"
    