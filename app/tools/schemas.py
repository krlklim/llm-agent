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
        "description": (
            "Immediately saves a new preference, trait, fact, or tech stack detail about the user. "
            "Supports separating sensitive/private details (saved in personal/PERSONAL_USER_INFO.md) "
            "from general/public info (saved in system/USER.md), and marking high-priority facts."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "fact": {
                    "type": "string",
                    "description": "The new fact or preference about the user (e.g., 'Uses Ruby on Rails', 'Full Name: Kiryl Klimovich')."
                },
                "is_private": {
                    "type": "boolean",
                    "description": (
                        "Set to TRUE for sensitive, private, or confidential information (saved to personal/PERSONAL_USER_INFO.md).\n"
                        "EXAMPLES OF PRIVATE INFO:\n"
                        "- Identity & Legal: Full legal name, date of birth, passport/ID numbers.\n"
                        "- Contact & Financial: Phone numbers, personal home addresses, bank accounts/cards.\n"
                        "- Health & Well-being: Medical diagnoses, allergies, personal state or mood.\n"
                        "- Private Context: Personal correspondence, sensitive family/relationship details.\n\n"
                        "Set to FALSE for general public or professional info (saved to system/USER.md).\n"
                        "EXAMPLES OF PUBLIC INFO:\n"
                        "- Professional: Tech stack, programming languages, code guidelines, work roles.\n"
                        "- General Hobbies/Pets: 'Has a dog named Miki', 'Loves pizza', 'Enjoys cycling and swimming'."
                    )
                },
                "is_important": {
                    "type": "boolean",
                    "description": (
                        "Set to TRUE for critical, high-priority context, sensitive identifiers, or user instructions marked as vital.\n"
                        "EXAMPLES OF CRITICAL/IMPORTANT FACTS:\n"
                        "- Health alerts (e.g., 'Has asthma, needs daily medicine reminders').\n"
                        "- Crucial identifiers (Full name, passport number, primary phone number).\n"
                        "- Explicit user requests (e.g., 'Remember this, it is very important: ...')."
                    )
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
    },
    {
        "name": "read_logs",
        "description": (
            "Reads recent log entries from the latest file in the logs/ directory. "
            "Use this tool when an execution fails, a tool returns an unexpected error, "
            "or when asked to inspect application logs to diagnose issues."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "lines": {
                    "type": "integer",
                    "description": "Number of lines to read from the end of the log file. Default is 250 (optimal for capturing 1-2 recent API request/response blocks)."
                },
                "level": {
                    "type": "string",
                    "description": "Optional keyword or log level to filter entries (e.g., 'ERROR', 'Exception', 'WARNING', 'tool_result')."
                }
            }
        }
    },
]

ALL_ANTHROPIC_TOOLS = ANTHROPIC_SERVER_TOOLS + ANTHROPIC_FUNCTION_TOOLS
