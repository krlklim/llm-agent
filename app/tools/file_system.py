from pathlib import Path
from app.config import BASE_DIR, SYSTEM_DIR, MEMORY_DIR

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

def update_user_profile(fact: str) -> str:
    user_file = SYSTEM_DIR / "USER.md"
    current_content = user_file.read_text(encoding="utf-8") if user_file.exists() else "# User Profile\n"
    new_content = current_content.strip() + f"\n- {fact}\n"
    user_file.write_text(new_content, encoding="utf-8")
    return f"Fact added to USER.md: '{fact}'"