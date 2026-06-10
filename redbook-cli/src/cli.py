import argparse
import json
import os
import sys

import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.prompt import REDBOOK_SYSTEM_PROMPT

console = Console()

CONFIG_DIR = os.path.expanduser("~/.redbook")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_API_URL = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-chat"


def ensure_config_dir():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_api_key():
    config = load_config()
    api_key = config.get("api_key", "")
    if not api_key:
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        console.print(
            Panel.fit(
                "[bold red]API Key not configured![/bold red]\n\n"
                "Set it with:\n"
                "  [cyan]redbook config --api-key YOUR_KEY[/cyan]\n\n"
                "Or set the environment variable:\n"
                "  [cyan]export DEEPSEEK_API_KEY=YOUR_KEY[/cyan]",
                title="Configuration Error",
                border_style="red",
            )
        )
        sys.exit(1)
    return api_key


def call_deepseek(system_prompt, user_message, api_key, model=None, api_url=None):
    if model is None:
        model = load_config().get("model", DEFAULT_MODEL)
    if api_url is None:
        api_url = load_config().get("api_url", DEFAULT_API_URL)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.3,
        "max_tokens": 4096,
    }

    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        console.print("[red]Request timed out. Please try again.[/red]")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        console.print(f"[red]API request failed: {e}[/red]")
        if hasattr(e, "response") and e.response is not None:
            console.print(f"[dim]Response: {e.response.text[:500]}[/dim]")
        sys.exit(1)


def print_redbook_header():
    header = r"""
  ██████╗ ███████╗██████╗ ██████╗  ██████╗  ██████╗ ██╗  ██╗
  ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝
  ██████╔╝█████╗  ██║  ██║██║  ██║██║   ██║██║   ██║█████╔╝
  ██╔══██╗██╔══╝  ██║  ██║██║  ██║██║   ██║██║   ██║██╔═██╗
  ██║  ██║███████╗██████╔╝██████╔╝╚██████╔╝╚██████╔╝██║  ██╗
  ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
"""
    console.print(header, style="bold red")


def cmd_analyze(args):
    print_redbook_header()
    api_key = get_api_key()

    user_msg = f"Analyze this problem: {args.problem}"
    with console.status("[bold red]Analyzing the contradiction...[/bold red]", spinner="dots"):
        response = call_deepseek(REDBOOK_SYSTEM_PROMPT, user_msg, api_key)

    console.print()
    console.print(
        Panel(
            Markdown(response),
            title="[bold]红宝书 Analysis[/bold]",
            border_style="red",
            title_align="left",
        )
    )


def cmd_guide(args):
    print_redbook_header()
    api_key = get_api_key()

    user_msg = f"I have no idea how to solve this problem: {args.problem}"
    with console.status("[bold red]Guiding through contradiction...[/bold red]", spinner="dots"):
        response = call_deepseek(REDBOOK_SYSTEM_PROMPT, user_msg, api_key)

    console.print()
    console.print(
        Panel(
            Markdown(response),
            title="[bold]红宝书 Guidance[/bold]",
            border_style="yellow",
            title_align="left",
        )
    )


def cmd_diagnose(args):
    print_redbook_header()
    api_key = get_api_key()

    user_msg = f"Diagnose this code:\n\n```\n{args.code}\n```"
    with console.status("[bold red]Diagnosing code contradictions...[/bold red]", spinner="dots"):
        response = call_deepseek(REDBOOK_SYSTEM_PROMPT, user_msg, api_key)

    console.print()
    console.print(
        Panel(
            Markdown(response),
            title="[bold]红宝书 Diagnosis[/bold]",
            border_style="magenta",
            title_align="left",
        )
    )


def cmd_config(args):
    print_redbook_header()
    config = load_config()

    changed = False

    if args.api_key is not None:
        config["api_key"] = args.api_key
        changed = True
        console.print("[green]✓ API key updated.[/green]")

    if args.model is not None:
        config["model"] = args.model
        changed = True
        console.print(f"[green]✓ Model updated to: {args.model}[/green]")

    if args.api_url is not None:
        config["api_url"] = args.api_url
        changed = True
        console.print(f"[green]✓ API URL updated to: {args.api_url}[/green]")

    if changed:
        save_config(config)
        console.print("[green]Configuration saved to ~/.redbook/config.json[/green]")
    else:
        table = Table(title="Current Configuration", border_style="red")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")

        masked_key = "********" if config.get("api_key") else "(not set)"
        api_key_display = masked_key[-8:] if len(masked_key) > 8 else masked_key

        table.add_row("API Key", api_key_display)
        table.add_row("Model", config.get("model", DEFAULT_MODEL))
        table.add_row("API URL", config.get("api_url", DEFAULT_API_URL))
        table.add_row("Config File", CONFIG_FILE)

        console.print(table)

        if not config.get("api_key"):
            console.print()
            console.print(
                "[yellow]⚠ API Key not configured. Set it with:[/yellow]\n"
                "  [cyan]redbook config --api-key YOUR_KEY[/cyan]"
            )


def cmd_philosophy(args):
    print_redbook_header()
    api_key = get_api_key()

    user_msg = f"Explain the philosophical concept: {args.concept}"
    with console.status("[bold red]Consulting the Red Book...[/bold red]", spinner="dots"):
        response = call_deepseek(REDBOOK_SYSTEM_PROMPT, user_msg, api_key)

    console.print()
    console.print(
        Panel(
            Markdown(response),
            title="[bold]红宝书 Philosophy[/bold]",
            border_style="red",
            title_align="left",
        )
    )


def main():
    parser = argparse.ArgumentParser(
        prog="redbook",
        description="红宝书 (Redbook) CLI - Algorithm analysis with contradiction methodology",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    parser_analyze = subparsers.add_parser("analyze", help="Analyze an algorithm problem")
    parser_analyze.add_argument("problem", type=str, help="The problem description to analyze")
    parser_analyze.set_defaults(func=cmd_analyze)

    parser_guide = subparsers.add_parser("guide", help="Guide when stuck on a problem")
    parser_guide.add_argument("problem", type=str, help="The problem you're stuck on")
    parser_guide.set_defaults(func=cmd_guide)

    parser_diagnose = subparsers.add_parser("diagnose", help="Diagnose buggy code")
    parser_diagnose.add_argument("code", type=str, help="The code to diagnose")
    parser_diagnose.set_defaults(func=cmd_diagnose)

    parser_config = subparsers.add_parser("config", help="Configure API key and settings")
    parser_config.add_argument("--api-key", type=str, help="DeepSeek API key")
    parser_config.add_argument("--model", type=str, help="Model name (default: deepseek-chat)")
    parser_config.add_argument("--api-url", type=str, help="API endpoint URL")
    parser_config.set_defaults(func=cmd_config)

    parser_philosophy = subparsers.add_parser("philosophy", help="Query philosophical concepts")
    parser_philosophy.add_argument("concept", type=str, help="The concept to explore (e.g., On Contradiction, On Practice)")
    parser_philosophy.set_defaults(func=cmd_philosophy)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
