"""Basic message history manager for the agent CLI interface."""

from typing import Literal

from rich.console import Console
from rich.text import Text

RoleType = Literal["user", "assistant", "system"]

# Message type alias representing a dict compatible with LLMs (e.g. Ollama, OpenAI)
Message = dict[str, str]


class MessageHistory:
    """Manages and displays a basic message history using dictionaries."""

    def __init__(self) -> None:
        self.messages: list[dict[str, str]] = []

    def add_message(self, role: RoleType, content: str) -> dict[str, str]:
        """Add a generic message dict to the history."""
        msg: dict[str, str] = {"role": role, "content": content}
        self.messages.append(msg)
        return msg

    def add_user_message(self, content: str) -> dict[str, str]:
        """Add a user message dict to the history."""
        return self.add_message("user", content)

    def add_assistant_message(self, content: str) -> dict[str, str]:
        """Add an assistant message dict to the history."""
        return self.add_message("assistant", content)

    def add_system_message(self, content: str) -> dict[str, str]:
        """Add a system message dict to the history."""
        return self.add_message("system", content)

    def clear(self) -> None:
        """Clear all stored messages."""
        self.messages.clear()

    def get_messages(self) -> list[dict[str, str]]:
        """Return a copy of all stored message dicts."""
        return list(self.messages)

    def render(self, console: Console | None = None) -> None:
        """Render the full message history to the console."""
        active_console = console or Console()
        if not self.messages:
            active_console.print("[dim italic]No messages in history.[/dim italic]")
            return

        for msg in self.messages:
            prefix = Text()
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "user":
                prefix.append("You: ", style="bold green")
            elif role == "assistant":
                prefix.append("Agent: ", style="bold blue")
            else:
                prefix.append("System: ", style="bold yellow")

            active_console.print(prefix, end="")
            active_console.print(content)
