from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style

"""Prompting input component built with prompt-toolkit."""


class FileReferenceCompleter(Completer):
    """Complete file and directory references after an @ character."""

    def __init__(self, base_path: Path | None = None) -> None:
        self.base_path = (base_path or Path.cwd()).resolve()

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        at_position = text_before_cursor.rfind("@")
        if at_position == -1:
            return

        fragment = text_before_cursor[at_position + 1:]
        if any(character.isspace() for character in fragment):
            return

        path_fragment = Path(fragment).expanduser()
        if path_fragment.is_absolute():
            search_path = path_fragment
        else:
            search_path = self.base_path / path_fragment

        directory = search_path if search_path.is_dir() else search_path.parent
        name_prefix = "" if search_path.is_dir() else search_path.name
        if not directory.is_dir():
            return

        for candidate in sorted(directory.iterdir(), key=lambda path: (path.is_file(), path.name.lower())):
            if name_prefix and not candidate.name.lower().startswith(name_prefix.lower()):
                continue
            relative_candidate = candidate if path_fragment.is_absolute() else candidate.relative_to(self.base_path)
            completion = str(relative_candidate)
            if candidate.is_dir():
                completion += "/"
            yield Completion(
                completion,
                start_position=-len(fragment),
                display=candidate.name,
            )


class PromptArea:
    """Interactive prompting component powered by prompt-toolkit."""

    def __init__(self, prompt_symbol: str = "> ") -> None:
        self.prompt_symbol = prompt_symbol
        self.session: PromptSession[str] = PromptSession(
            history=InMemoryHistory(),
            completer=FileReferenceCompleter(),
            complete_while_typing=True,
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


def prompt_user(prompt_text: str = "> ") -> str | None:
    """Convenience helper to ask for a single input line."""
    session: PromptSession[str] = PromptSession(
        completer=FileReferenceCompleter(),
        complete_while_typing=True,
    )
    try:
        return session.prompt(prompt_text)
    except (KeyboardInterrupt, EOFError):
        return None
