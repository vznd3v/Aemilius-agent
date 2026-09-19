from rich.console import Console

from ..gateway import Gateway
from ..tools import QuitRequested, get_tools
from .interface import (
    MessageHistory,
    ThinkingMode,
    ThinkingStreamer,
    prompt_user,
    render_panel,
)

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
        thinking_stream = ThinkingStreamer(console, mode=thinking_mode)
        content_started = False

        try:
            for chunk in gateway.stream_text(user_input, history.get_messages()):
                if chunk.type == "thinking":
                    thinking_stream.feed(chunk.text)
                elif chunk.type == "content":
                    if not content_started:
                        thinking_stream.finish()
                        console.print("[bold blue]Agent:[/bold blue] ", end="")
                        content_started = True
                    console.print(chunk.text, end="")
                    content_parts.append(chunk.text)
                elif chunk.type == "tool_result":
                    console.print(f"[dim](tool: {chunk.text.strip()[:60]})[/dim] ", end="")
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
        console.print()
        history.add_assistant_message("".join(content_parts))