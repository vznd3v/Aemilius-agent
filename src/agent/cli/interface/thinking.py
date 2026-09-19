from enum import Enum

from rich.console import Console

DEFAULT_MAX_LENGTH = 200


class ThinkingMode(Enum):
    SHORT = "short"
    FULL = "full"
    OFF = "off"


def render_thinking(console: Console, content: str, mode: ThinkingMode = ThinkingMode.SHORT) -> None:
    """Render the model's thinking, either truncated (SHORT) or complete (FULL)."""
    if mode is ThinkingMode.OFF or not content:
        return

    if mode is ThinkingMode.FULL:
        console.print(f"[dim italic]Thinking: {content}[/dim italic]")
        return

    truncated = content[:DEFAULT_MAX_LENGTH]
    suffix = "..." if len(content) > DEFAULT_MAX_LENGTH else ""
    hint = " (type /thinking full to expand)" if suffix else ""
    console.print(f"[dim italic]Thinking: {truncated}{suffix}{hint}[/dim italic]")


class ThinkingStreamer:
    """Streams thinking tokens into their own separate thinking section."""

    def __init__(
        self,
        console: Console,
        mode: ThinkingMode = ThinkingMode.SHORT,
        max_length: int = DEFAULT_MAX_LENGTH,
    ) -> None:
        self.console = console
        self.mode = mode
        self.max_length = max_length
        self.shown_length = 0
        self.truncated = False
        self._started = False

    def feed(self, text: str) -> None:
        """Feed a streaming thinking chunk into its dedicated section."""
        if self.mode is ThinkingMode.OFF or not text:
            return

        if not self._started:
            self.console.print("[dim italic]Thinking:[/dim italic] ", end="")
            self._started = True

        if self.mode is ThinkingMode.FULL:
            self.console.print(text, style="dim italic", end="")
            return

        if self.shown_length < self.max_length:
            piece = text[: self.max_length - self.shown_length]
            self.console.print(piece, style="dim italic", end="")
            self.shown_length += len(piece)
            if len(text) > len(piece):
                self.truncated = True

    def finish(self) -> None:
        """Close the thinking section (truncation hint + newline) if it was shown."""
        if not self._started:
            return
        if self.truncated:
            self.console.print(" [dim italic](... type /thinking full to expand)[/dim italic]", end="")
        self.console.print()