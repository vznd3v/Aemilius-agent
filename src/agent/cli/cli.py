from rich.console import Console
from rich.panel import Panel

from ..gateway import Gateway
from ..tools import QuitRequested, get_tools
from .interface import (
    MessageHistory,
    ThinkingMode,
    ThinkingStreamer,
    prompt_user,
    render_panel,
)
from .markdown_engine import render_markdown

THINKING_USAGE = "/thinking <short|full|off>"


def _handle_thinking_command(console: Console, thinking_mode: ThinkingMode, arg: str) -> ThinkingMode:
    if not arg:
        console.print(f"[cyan]Usage: {THINKING_USAGE}[/cyan]")
        console.print(f"[cyan]Current mode: {thinking_mode.value}[/cyan]")
        return thinking_mode
    try:
        return ThinkingMode(arg)
    except ValueError:
        console.print(f"[cyan]Unknown mode: {arg}. {THINKING_USAGE}[/cyan]")
        return thinking_mode


def run_cli() -> None:
    console = Console()
    render_panel(console)
    history = MessageHistory()
    thinking_mode = ThinkingMode.SHORT

    while True:
        user_input = prompt_user()
        if user_input is None or user_input in ("quit", "q"):
            console.print("Exiting... Goodbye !")
            break

        if not user_input.strip():
            continue

        if user_input.startswith("/thinking"):
            arg = user_input[len("/thinking"):].strip()
            thinking_mode = _handle_thinking_command(console, thinking_mode, arg)
            continue

        history.add_user_message(user_input)
        gateway = Gateway(tools=get_tools())
        content_parts: list[str] = []
        usage: dict[str, int] | None = None
        thinking_stream = ThinkingStreamer(console, mode=thinking_mode)
        content_started = False

        try:
            for chunk in gateway.stream_text(user_input, history.get_messages()):
                if chunk.type == "thinking":
                    thinking_stream.feed(chunk.text)
                elif chunk.type == "content":
                    content_started = True
                    content_parts.append(chunk.text)
                elif chunk.type == "tool_result":
                    console.print(f"[dim](tool: {chunk.text.strip()[:60]})[/dim] ", end="")
                elif chunk.type == "usage":
                    usage = chunk.usage
                elif chunk.type == "error":
                    console.print(f"[bold red]{chunk.text}[/bold red]", end="")
        except QuitRequested:
            if not content_started:
                thinking_stream.finish()
            console.print()
            console.print("Goodbye !")
            break
        if not content_started:
            thinking_stream.finish()
        else:
            thinking_stream.finish()
            console.print("[bold blue]Agent:[/bold blue]")
            render_markdown(console, "".join(content_parts))
        console.print()
        if content_parts:
            output_text = "".join(content_parts)
            input_tokens = (usage or {}).get("prompt_tokens", max(1, len(user_input) // 4))
            output_tokens = (usage or {}).get("completion_tokens", max(1, len(output_text) // 4))
            total_tokens = (usage or {}).get("total_tokens", input_tokens + output_tokens)
            source = "provider usage" if usage else "estimated"
            console.print(Panel(
                f"Input tokens ({source}): {input_tokens}\n"
                f"Output tokens ({source}): {output_tokens}\n"
                f"Total tokens ({source}): {total_tokens}",
                title="Usage",
                border_style="dim",
                expand=False,
            ))
        history.add_assistant_message("".join(content_parts))