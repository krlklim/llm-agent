# app/llm.py
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from anthropic import Anthropic
from google import genai

from app.config import OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY
from app.tools.file_system import read_file, write_file, update_user_profile
from app.tools.web_tools import (
    duckduckgo_web_search,
    google_web_search,
    fetch_web_page,
    get_youtube_transcript,
)
from app.tools.schemas import ALL_ANTHROPIC_TOOLS
from app.logger import log_raw_interaction

ALL_TOOLS = [
    read_file,
    write_file,
    update_user_profile,
    duckduckgo_web_search,
    google_web_search,
    fetch_web_page,
    get_youtube_transcript,
]

TOOLS_MAP = {func.__name__: func for func in ALL_TOOLS}


class LLMClient:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        
        if provider == "openai":
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        elif provider == "anthropic":
            self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        elif provider == "gemini":
            self.client = genai.Client(api_key=GEMINI_API_KEY)

    def _extract_anthropic_text(self, response_message) -> str:
        text_parts = [
            block.text for block in response_message.content 
            if getattr(block, "type", None) == "text"
        ]
        return "\n".join(text_parts)

    def generate(
        self, 
        system_prompt: str, 
        messages: List[Dict[str, Any]], 
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        thinking: bool = False,
        thinking_budget: int = 1024
    ) -> str:

        if self.provider == "anthropic":
            model = model_name or "claude-haiku-4-5-20251001"
            working_messages = list(messages)

            while True:
                params: Dict[str, Any] = {
                    "model": model,
                    "max_tokens": 4000,
                    "system": system_prompt,
                    "messages": working_messages,
                    "temperature": temperature,
                    "tools": ALL_ANTHROPIC_TOOLS,
                }

                if thinking:
                    params["thinking"] = {
                        "type": "enabled",
                        "budget_tokens": thinking_budget,
                    }
                    params["temperature"] = 1.0

                response = self.client.messages.create(**params)

                log_raw_interaction(
                    provider="anthropic",
                    model=model,
                    request_data=params,
                    response_data=response
                )

                if response.stop_reason == "tool_use":
                    working_messages.append({"role": "assistant", "content": response.content})

                    tool_results = []
                    has_local_tool_calls = False

                    for block in response.content:
                        if block.type == "tool_use":
                            tool_name = block.name
                            tool_args = block.input
                            
                            if tool_name in TOOLS_MAP:
                                has_local_tool_calls = True
                                try:
                                    output = TOOLS_MAP[tool_name](**tool_args)
                                    is_error = False
                                except Exception as e:
                                    output = f"Execution error: {e}"
                                    is_error = True

                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": str(output),
                                    "is_error": is_error
                                })

                    if has_local_tool_calls:
                        working_messages.append({"role": "user", "content": tool_results})
                    else:
                        break
                else:
                    return self._extract_anthropic_text(response)

            return self._extract_anthropic_text(response)

        elif self.provider == "gemini":
            model = model_name or "gemini-2.0-flash"
            
            formatted_contents = []
            for m in messages:
                role = "user" if m["role"] == "user" else "model"
                formatted_contents.append({"role": role, "parts": [{"text": m["content"]}]})

            request_config = {
                "system_instruction": system_prompt,
                "temperature": temperature,
                "tools": ALL_TOOLS
            }

            response = self.client.models.generate_content(
                model=model,
                contents=formatted_contents,
                config=request_config
            )

            log_raw_interaction(
                provider="gemini",
                model=model,
                request_data={"contents": formatted_contents, "config": str(request_config)},
                response_data=response
            )

            if response.function_calls:
                results = []
                for call in response.function_calls:
                    fn_name = call.name
                    args = call.args
                    if fn_name in TOOLS_MAP:
                        res = TOOLS_MAP[fn_name](**args)
                        results.append(f"[Tool Executed: {fn_name}]\n{res}")
                    else:
                        results.append(f"[Tool Error]: Unknown function '{fn_name}'")
                return "\n\n".join(results)

            return response.text or "Done."

        elif self.provider == "openai":
            model = model_name or "gpt-4o"
            formatted_messages = [{"role": "system", "content": system_prompt}] + messages
            
            response = self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                temperature=temperature,
            )

            log_raw_interaction(
                provider="openai",
                model=model,
                request_data={"messages": formatted_messages},
                response_data=response
            )

            return response.choices[0].message.content or ""

        raise ValueError(f"Unsupported provider: {self.provider}")
