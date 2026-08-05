ANTHROPIC_SERVER_TOOLS = [
    {
        "type": "web_search_20250305",
        "name": "web_search",
        "max_uses": 5
    }
]

ANTHROPIC_FUNCTION_TOOLS = [
    {
        "name": "read_file",
        "description": "Reads the text content of a file within the project directory. Use this to inspect files like system/USER.md, system/MEMORY.md, code files, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the file from the project root (e.g., 'system/USER.md')."
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Writes text content to a specified file within the project directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path to the file (e.g., 'memory/2026-08-04.md')."
                },
                "content": {
                    "type": "string",
                    "description": "The exact content to write into the file."
                }
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "update_user_profile",
        "description": "Immediately saves a new personal preference, trait, fact, or tech stack detail about the user into system/USER.md.",
        "input_schema": {
            "type": "object",
            "properties": {
                "fact": {
                    "type": "string",
                    "description": "The new fact or preference about the user (e.g., 'Likes pizza', 'Uses Ruby on Rails')."
                }
            },
            "required": ["fact"]
        }
    },
    {
        "name": "get_youtube_transcript",
        "description": "Retrieves the subtitles/transcript of a YouTube video.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url_or_video_id": {"type": "string", "description": "YouTube video URL or 11-character video ID."}
            },
            "required": ["url_or_video_id"]
        }
    },
    {
        "name": "send_email",
        "description": "Sends an email to a target recipient. Make sure the subject is concise and relevant, and the body is fully composed, formatted, and contains polite sign-offs before calling this tool.",
        "input_schema": {
            "type": "object",
            "properties": {
                "to_email": {
                    "type": "string",
                    "description": "Recipient email address (e.g., 'example@ex.com')."
                },
                "subject": {
                    "type": "string",
                    "description": "Clear, professional, and context-appropriate email subject line."
                },
                "body": {
                    "type": "string",
                    "description": "The complete, formatted body of the email including greetings, main content, sign-off with user's name, and optional watermark."
                }
            },
            "required": ["to_email", "subject", "body"]
        }
    }
]

ALL_ANTHROPIC_TOOLS = ANTHROPIC_SERVER_TOOLS + ANTHROPIC_FUNCTION_TOOLS
