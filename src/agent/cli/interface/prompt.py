from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style

"""Prompting input component built with prompt-toolkit."""


class PromptArea:
    """Interactive prompting component powered by prompt-toolkit."""

    def __init__(self, prompt_symbol: str = "Aemilius > ") -> None:
        self.prompt_symbol = prompt_symbol
        self.session: PromptSession[str] = PromptSession(
            history=InMemoryHistory(),
            style=Style.from_dict({
                "prompt": "bold cyan",
            }),
        )

    def ask(self, custom_prompt: str | None = None) -> str | None:
        """Prompt the user for input in the terminal.

        Returns:
            The input string, or None if the user cancelled (Ctrl+C, Ctrl+D).
        """
        prompt_text = custom_prompt if custom_prompt is not None else self.prompt_symbol
        try:
            return self.session.prompt(HTML(f"<prompt>{prompt_text}</prompt>"))
        except (KeyboardInterrupt, EOFError):
            return None


def prompt_user(prompt_text: str = "Aemilius > ") -> str | None:
    """Convenience helper to ask for a single input line."""
    session: PromptSession[str] = PromptSession()
    try:
        return session.prompt(prompt_text)
    except (KeyboardInterrupt, EOFError):
        return None
