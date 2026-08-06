from pathlib import Path
from app.config import BASE_DIR, SYSTEM_DIR, PERSONAL_USER_FILE

def read_file(path: str) -> str:
    file_path = (BASE_DIR / path).resolve()
    
    if not str(file_path).startswith(str(BASE_DIR)):
        return "Error: Access denied. Cannot read files outside project directory."
        
    if file_path.name.startswith(".env") or ".env" in file_path.parts:
        return "Error: Access denied. Reading environment configuration files (.env) is prohibited."
        
    if not file_path.exists():
        return f"Error: File {path} not found."
        
    return file_path.read_text(encoding="utf-8")

def write_file(path: str, content: str) -> str:
    file_path = (BASE_DIR / path).resolve()
    if not str(file_path).startswith(str(BASE_DIR)):
        return "Error: Access denied. Cannot write files outside project directory."
        
    if file_path.name.startswith(".env") or ".env" in file_path.parts:
        return "Error: Access denied. Modifying environment configuration files is prohibited."
        
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return f"Successfully wrote to {path}"

def update_user_profile(fact: str, is_private: bool = False, is_important: bool = False) -> str:
    target_file = PERSONAL_USER_FILE if is_private else (SYSTEM_DIR / "USER.md")
    
    if not target_file.exists():
        target_file.parent.mkdir(parents=True, exist_ok=True)
        default_header = (
            "# Personal Sensitive User Info\n\n## Private Facts\n" 
            if is_private 
            else "# User Profile\n\n## General Info\n"
        )
        target_file.write_text(default_header, encoding="utf-8")

    current_content = target_file.read_text(encoding="utf-8")
    fact_clean = fact.strip()

    if fact_clean.lower() in current_content.lower():
        file_name = "PERSONAL_USER_INFO.md" if is_private else "USER.md"
        return f"Fact already exists in {file_name}. Skipped duplicate."

    formatted_fact = f"- [IMPORTANT] {fact_clean}" if is_important else f"- {fact_clean}"

    new_content = current_content.strip() + f"\n{formatted_fact}\n"
    target_file.write_text(new_content, encoding="utf-8")

    target_name = "personal/PERSONAL_USER_INFO.md (private)" if is_private else "system/USER.md (public)"
    return f"Successfully added fact to {target_name}: '{formatted_fact}'"
