"""Tests for CLI rendering and file reference completion."""

import tempfile
import unittest
from pathlib import Path

from prompt_toolkit.document import Document
from rich.console import Console

from agent.cli.interface.prompt import FileReferenceCompleter
from agent.cli.markdown_engine import render_markdown


class TestMarkdownEngine(unittest.TestCase):
    def test_render_markdown_renders_code_block(self):
        console = Console(record=True, width=80)

        render_markdown(console, "```python\nprint('hello')\n```")

        output = console.export_text()
        self.assertIn("print('hello')", output)


class TestFileReferenceCompleter(unittest.TestCase):
    def test_completes_file_after_at_symbol(self):
        with tempfile.TemporaryDirectory() as tmp:
            base_path = Path(tmp)
            (base_path / "chatbot.py").write_text("print('hello')")
            completer = FileReferenceCompleter(base_path)

            completions = list(completer.get_completions(
                Document("Read @chat"),
                complete_event=None,
            ))

            self.assertEqual([completion.text for completion in completions], ["chatbot.py"])

    def test_completes_directory_after_at_symbol(self):
        with tempfile.TemporaryDirectory() as tmp:
            base_path = Path(tmp)
            (base_path / "src").mkdir()
            completer = FileReferenceCompleter(base_path)

            completions = list(completer.get_completions(
                Document("Inspect @s"),
                complete_event=None,
            ))

            self.assertEqual([completion.text for completion in completions], ["src/"])


if __name__ == "__main__":
    unittest.main()