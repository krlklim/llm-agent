import argparse
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from app.config import MEMORY_DIR, DEFAULT_PROVIDER
from app.context import build_system_prompt
from app.llm import LLMClient

console = Console()

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

    console.print(Panel.fit(
        f"[bold green]AI Assistant CLI Initialized[/bold green]\n"
        f"[bold yellow]Active Provider: {selected_provider.upper()}[/bold yellow]\n"
        "[dim]Tools: Web Search, Page Fetch, YouTube Transcript, File Manager, User Memory[/dim]",
        title="Agent Environment"
    ))
    
    system_prompt = build_system_prompt()
    console.print("[bold blue]System Prompt Loaded successfully![/bold blue]")
    console.print(f"Total system prompt length: [yellow]{len(system_prompt)}[/yellow] chars.\n")
    console.print(f"[yellow]I'm ready! :)[/yellow]\n")


    llm = LLMClient(provider=selected_provider)
    messages_history = []

    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("[bold red]Bye![/bold red]")
                break

            messages_history.append({"role": "user", "content": user_input})
            
            current_system_prompt = build_system_prompt()

            with console.status("[bold green]Agent is thinking & executing tools...[/bold green]"):
                response_text = llm.generate(
                    system_prompt=current_system_prompt, 
                    messages=messages_history
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