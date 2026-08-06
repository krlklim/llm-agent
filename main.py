import argparse
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from textwrap import dedent

from app.config import MEMORY_DIR, DEFAULT_PROVIDER
from app.context import build_system_prompt
from app.llm import LLMClient

console = Console()
input_history = InMemoryHistory()

DEFAULT_MODELS = {
    "anthropic": "claude-haiku-4-5-20251001",
    "gemini": "gemini-2.0-flash",
    "openai": "gpt-4o",
}

def append_to_daily_log(user_msg: str, agent_msg: str):
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_file = MEMORY_DIR / f"{today_str}.md"
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"\n### [{timestamp}]\n**User**: {user_msg}\n\n**Agent**: {agent_msg}\n"
    
    if not log_file.exists():
        log_file.write_text(f"# Memory Log ({today_str})\n" + entry, encoding="utf-8")
    else:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry)

def parse_args():
    parser = argparse.ArgumentParser(description="CLI AI Agent")
    parser.add_argument(
        "--provider", "-p",
        type=str,
        choices=["gemini", "anthropic", "openai"],
        default=DEFAULT_PROVIDER,
        help="LLM's: (gemini | anthropic | openai)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    selected_provider = args.provider
    current_model = DEFAULT_MODELS.get(selected_provider, "claude-haiku-4-5-20251001")

    # TODO: console.clear() if u need to clean console

    console.print(Panel.fit(
        f"[bold green]AI Assistant CLI Initialized[/bold green]\n"
        f"[bold yellow]Active Provider: {selected_provider.upper()}[/bold yellow]\n"
        f"[bold cyan]Active Model: {current_model}[/bold cyan]\n"
        "[dim]Tools: Web Search, Page Fetch, YouTube Transcript, File Manager, User Memory, Emailing etc.[/dim]",
        title="Agent Environment"
    ))
    
    system_prompt = build_system_prompt()
    console.print("[bold blue]System Prompt Loaded successfully![/bold blue]")
    console.print(f"Total system prompt length: [yellow]{len(system_prompt)}[/yellow] chars.\n")
    console.print("[bold blue]For help type /help or /h[/bold blue]")
    console.print(f"[yellow]I'm ready! :)[/yellow]\n")


    llm = LLMClient(provider=selected_provider)
    messages_history = []

    while True:
        try:
            user_input = prompt(
                HTML("<cyan><b>You</b></cyan>: "), 
                history=input_history
            ).strip()

            if not user_input:
                continue

            if not user_input:
                continue

            if user_input.lower() in ["/exit", "/quit", "/q"]:
                console.print("[bold red]Bye![/bold red]")
                break

            if user_input.lower() in ["/help", "/h"]:
                console.print(dedent("""
            [bold cyan]📖 Help & Available Commands:[/bold cyan]

            [green]/exit, /quit, /q or Ctrl+C[/green]
            Exit the application.

            [green]/tools, /t[/green]
            Show available agent tools and capabilities.

            [green]/set_provider <gemini | anthropic | openai>[/green]
            Change the active LLM provider.

            [green]/set_model <model_name>[/green]
            Change the active LLM model.

            [green]/information, /info, /current_model, /model, /current_provider, /provider[/green]
            Show active provider and model.

            [green]/help, /h[/green]
            Show this help message.
            """))
                continue

            if user_input.lower() in ["/tools", "/t"]:
                console.print(dedent("""
            [bold cyan]🛠️  Available Agent Tools & Capabilities:[/bold cyan]

            [bold yellow]1. Web Search & Scraping[/bold yellow]
               [green]google_web_search / duckduckgo_web_search / anthropic_web_search[/green]: Search for up-to-date information and news online.
               [green]fetch_web_page[/green]: Read and extract clean content from web pages by URL.
               [green]get_youtube_transcript[/green]: Fetch available subtitles/transcripts from YouTube videos.

            [bold yellow]2. File Operations & Code Management[/bold yellow]
               [green]read_file[/green]: Read source code, documentation, and configuration files within the project.
               [green]write_file[/green]: Create new files or update existing ones.

            [bold yellow]3. Email Dispatch[/bold yellow]
               [green]send_email[/green]: Compose and send emails via SMTP (supports plain text and responsive HTML).

            [bold yellow]4. Memory & Knowledge Base[/bold yellow]
               • [green]update_user_profile[/green]: Automatically record new facts, preferences, and tech stack in `USER.md`.
               • [green]Memory Logging[/green]: Log context, active tasks, and decisions into daily memory files.
            """))
                continue

            if user_input.lower() in ["/model", 
                                      "/current_model", 
                                      "/information", 
                                      "/info", 
                                      "/current_model", 
                                      "/model", 
                                      "/current_provider", 
                                      "/provider"]:
                console.print(
                    f"[bold yellow]Provider:[/bold yellow] {selected_provider.upper()} | "
                    f"[bold cyan]Model:[/bold cyan] {current_model}"
                )
                continue

            if user_input.lower().startswith("/set_provider"):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1 and parts[1].strip():
                    new_provider = parts[1].strip().lower().strip('"\'')
                    if new_provider in DEFAULT_MODELS:
                        selected_provider = new_provider
                        current_model = DEFAULT_MODELS[selected_provider]
                        llm = LLMClient(provider=selected_provider)
                        console.print(
                            f"[bold green]Provider changed to:[/bold green] [yellow]{selected_provider.upper()}[/yellow]\n"
                            f"[bold green]Model set to default:[/bold green] [cyan]{current_model}[/cyan]"
                        )
                    else:
                        valid_providers = ", ".join(DEFAULT_MODELS.keys())
                        console.print(f"[bold red]Unknown provider.[/bold red] Available options: [yellow]{valid_providers}[/yellow]")
                else:
                    console.print("[bold red]Usage:[/bold red] /set_provider <gemini | anthropic | openai>")
                continue

            if user_input.lower().startswith("/set_model"):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1 and parts[1].strip():
                    raw_model = parts[1].strip()
                    current_model = raw_model.strip('"\'')
                    console.print(f"[bold green]Model successfully changed to:[/bold green] [yellow]{current_model}[/yellow]")
                else:
                    console.print("[bold red]Usage:[/bold red] /set_model <model_name>")
                continue

            messages_history.append({"role": "user", "content": user_input})
            
            current_system_prompt = build_system_prompt()

            with console.status("[bold green]Agent is thinking & executing tools...[/bold green]"):
                response_text = llm.generate(
                    system_prompt=current_system_prompt, 
                    messages=messages_history,
                    model_name=current_model
                )

            console.print("\n[bold green]Agent[/bold green]:")
            console.print(Markdown(response_text))
            
            messages_history.append({"role": "assistant", "content": response_text})
            append_to_daily_log(user_input, response_text)

        except KeyboardInterrupt:
            console.print("\n[bold red]Exit.[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()