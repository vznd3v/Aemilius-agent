"""Tests for Aemilius Agent tools registry and dispatch."""

import tempfile
import unittest
from pathlib import Path

from agent.tools import TOOLS, QuitRequested, execute_tool, get_tools, to_schemas


class TestTools(unittest.TestCase):
    def test_get_tools_registers_listfiles(self):
        names = [tool["function"]["name"] for tool in get_tools()]
        self.assertIn("listfiles", names)

    def test_get_tools_registers_quit(self):
        names = [tool["function"]["name"] for tool in get_tools()]
        self.assertIn("quit", names)

    def test_quit_tool_raises_quit_requested(self):
        with self.assertRaises(QuitRequested):
            execute_tool(get_tools(), "quit", {})

    def test_get_tools_returns_registry(self):
        self.assertEqual(get_tools(), TOOLS)

    def test_to_schemas_strips_call_key(self):
        schemas = to_schemas(get_tools())
        for schema in schemas:
            self.assertNotIn("call", schema)
            self.assertEqual(schema["type"], "function")
            self.assertIn("function", schema)
        names = [schema["function"]["name"] for schema in schemas]
        self.assertIn("listfiles", names)

    def test_execute_tool_lists_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "hello.txt").touch()
            output = execute_tool(get_tools(), "listfiles", {"path": tmp})
            self.assertIn("hello.txt", output)

    def test_execute_tool_raises_on_unknown(self):
        with self.assertRaises(KeyError):
            execute_tool(get_tools(), "no_such_tool", {})


if __name__ == "__main__":
    unittest.main()