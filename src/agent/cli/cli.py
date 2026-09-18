from ollama import chat
from rich.console import Console

from .interface import MessageHistory, prompt_user, render_panel


def run_cli() -> None:
    console = Console()
    render_panel(console)
    history = MessageHistory()

    while True:
        user_input = prompt_user()
        if user_input is None or user_input in ("quit", "q"):
            console.print("Exiting... Goodbye !")
            break

        if not user_input.strip():
            continue

        history.add_user_message(user_input)
        response = chat(model="llama3.2:1b", messages=history.get_messages())
        assistant_reply = response.message.content
        history.add_assistant_message(assistant_reply)
        console.print(f"[bold blue]Agent:[/bold blue] {assistant_reply}")