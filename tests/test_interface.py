"""Tests for MeshOSS CLI interface components."""

import unittest

from rich.console import Console

from agent.cli.interface.messages import MessageHistory
from agent.cli.interface.panel import get_panel, render_panel
from agent.cli.interface.prompt import PromptArea


class TestInterface(unittest.TestCase):
    def test_panel_content(self):
        """Verify that the panel contains the required character and version info."""
        panel = get_panel()
        self.assertIsNotNone(panel)

        console = Console(record=True, width=80)
        render_panel(console)
        output = console.export_text()

        self.assertIn("\u25a6", output)
        self.assertIn("MeshOSS", output)
        self.assertIn("pre-alpha v0.0.1", output)

    def test_message_history(self):
        """Verify message history operations (add, clear, get)."""
        history = MessageHistory()
        self.assertEqual(len(history.get_messages()), 0)

        history.add_user_message("Hello world")
        history.add_assistant_message("How can I assist you?")
        history.add_system_message("System initiated")

        messages = history.get_messages()
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[0]["content"], "Hello world")
        self.assertEqual(messages[1]["role"], "assistant")
        self.assertEqual(messages[2]["role"], "system")

        console = Console(record=True, width=80)
        history.render(console)
        rendered = console.export_text()
        self.assertIn("Hello world", rendered)
        self.assertIn("How can I assist you?", rendered)

        history.clear()
        self.assertEqual(len(history.get_messages()), 0)

    def test_prompt_area_init(self):
        """Verify PromptArea initialization."""
        prompt_area = PromptArea(prompt_symbol="Test > ")
        self.assertEqual(prompt_area.prompt_symbol, "Test > ")
        self.assertIsNotNone(prompt_area.session)


if __name__ == "__main__":
    unittest.main()

