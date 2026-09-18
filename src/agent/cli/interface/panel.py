from rich.console import Console
from rich.panel import Panel
from rich.text import Text

"""Fixed mini header panel for MeshOSS CLI interface."""


def get_panel() -> Panel:
    """Build and return the fixed mini header panel for MeshOSS."""
    content = Text()
    # Special character &#x25A6; (Unicode U+25A6: Square with orthogonal crosshatch)
    content.append("\u25a6 ", style="bold cyan")
    content.append("MeshOSS ", style="bold white")
    content.append("pre-alpha v0.0.1", style="dim yellow")

    return Panel(
        content,
        expand=False,
        border_style="cyan",
    )


def render_panel(console: Console | None = None) -> None:
    """Render the header panel to the console."""
    active_console = console or Console()
    active_console.print(get_panel())
