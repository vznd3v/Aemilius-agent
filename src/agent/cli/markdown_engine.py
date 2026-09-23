from rich.console import Console
from rich.markdown import Markdown


def render_markdown(console: Console, content: str) -> None:
	"""Render an agent response as Markdown in the terminal."""
	if content:
		console.print(Markdown(content, code_theme="github-dark"))
