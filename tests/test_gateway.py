"""Tests for Aemilius Agent gateway (provider calls + tool use loop)."""

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import agent.gateway.gateway as gateway_module
from agent.gateway import Gateway
from agent.gateway.gateway import SYSTEM_PROMPT, ModelResponse, StreamChunk
from agent.tools import QuitRequested, get_tools


def _ollama_message(content="", tool_calls=None, thinking=""):
    return {
        "message": {
            "role": "assistant",
            "content": content,
            "thinking": thinking,
            "tool_calls": tool_calls or [],
        }
    }


class TestGateway(unittest.TestCase):
    def setUp(self):
        self.gw = Gateway(tools=get_tools())
        self.gw.ollama_model = "test-model"

    @patch.object(gateway_module.ollama, "chat", return_value=_ollama_message("Hello there"))
    def test_direct_reply(self, mock_chat):
        response = self.gw.generate_text("Hi")
        self.assertIsInstance(response, ModelResponse)
        self.assertEqual(response.content, "Hello there")
        self.assertEqual(response.thinking, "")

    @patch.object(
        gateway_module.ollama,
        "chat",
        return_value=_ollama_message("Final answer", thinking="Let me think"),
    )
    def test_thinking_extracted(self, mock_chat):
        response = self.gw.generate_text("Why?")
        self.assertEqual(response.thinking, "Let me think")
        self.assertEqual(response.content, "Final answer")

    @patch.object(
        gateway_module.ollama,
        "chat",
        return_value=_ollama_message("Ok"),
    )
    def test_system_prompt_prepended(self, mock_chat):
        self.gw.generate_text("Hi", history=[{"role": "user", "content": "earlier"}])
        kwargs = mock_chat.call_args.kwargs
        self.assertEqual(kwargs["messages"][0]["role"], "system")
        self.assertEqual(kwargs["messages"][0]["content"], SYSTEM_PROMPT)

    @patch.object(
        gateway_module.ollama,
        "chat",
        return_value=_ollama_message("Bonjour !"),
    )
    def test_no_tools_for_greeting(self, mock_chat):
        self.gw.generate_text("bonjour ?")
        self.assertNotIn("tools", mock_chat.call_args.kwargs)

    @patch.object(
        gateway_module.ollama,
        "chat",
        return_value=_ollama_message("Ok"),
    )
    def test_tools_attached_when_keyword_present(self, mock_chat):
        self.gw.generate_text("liste les fichiers du dossier /tmp")
        self.assertIn("tools", mock_chat.call_args.kwargs)

    @patch.object(
        gateway_module.ollama,
        "chat",
        return_value=_ollama_message("Ok"),
    )
    def test_tools_attached_when_tool_name_present(self, mock_chat):
        self.gw.generate_text("quitte maintenant")
        self.assertIn("tools", mock_chat.call_args.kwargs)

    @patch.object(
        gateway_module.ollama,
        "chat",
        side_effect=[[_ollama_message(tool_calls=[
            {"function": {"name": "quit", "arguments": {}}}
        ])]],
    )
    def test_quit_tool_propagates_quit_requested(self, mock_chat):
        with self.assertRaises(QuitRequested):
            list(self.gw.stream_text("quitte maintenant"))

    def test_tool_use_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "report.txt").touch()
            tool_response = _ollama_message(tool_calls=[
                {"function": {"name": "listfiles", "arguments": {"path": tmp}}}
            ])
            final_response = _ollama_message("Here is the listing!")
            with patch.object(
                gateway_module.ollama,
                "chat",
                side_effect=[tool_response, final_response],
            ) as mock_chat:
                response = self.gw.generate_text("List the files")

        self.assertEqual(response.content, "Here is the listing!")
        called_messages = mock_chat.call_args_list[1].kwargs["messages"]
        self.assertTrue(any(
            msg["role"] == "tool" and "report.txt" in msg["content"]
            for msg in called_messages
        ))

    def test_tool_failure_fed_back(self):
        tool_response = _ollama_message(tool_calls=[
            {"function": {"name": "broken_tool", "arguments": {}}}
        ])
        final_response = _ollama_message("I ran into a problem.")
        with patch.object(
            gateway_module.ollama,
            "chat",
            side_effect=[tool_response, final_response],
        ) as mock_chat:
            response = self.gw.generate_text("Do something")

        self.assertEqual(response.content, "I ran into a problem.")
        called_messages = mock_chat.call_args_list[1].kwargs["messages"]
        self.assertTrue(any(
            msg["role"] == "tool" and "failed" in msg["content"]
            for msg in called_messages
        ))

    @patch.object(
        gateway_module.ollama,
        "chat",
        side_effect=lambda **kwargs: _ollama_message(tool_calls=[
            {"function": {"name": "listfiles", "arguments": {"path": "/"}}}
        ]),
    )
    def test_max_tool_iterations(self, mock_chat):
        response = self.gw.generate_text("Loop forever")
        self.assertEqual(response.content, "Maximum tool iterations reached.")

    def test_unknown_provider_raises(self):
        self.gw.default_provider = "mars_provider"
        with self.assertRaises(ValueError):
            self.gw.generate_text("Hi")

    def test_openai_tool_calls_normalized(self):
        message = SimpleNamespace(
            content="call me",
            thinking="reasoning here",
            tool_calls=[
                SimpleNamespace(
                    id="call_123",
                    function=SimpleNamespace(name="listfiles", arguments='{"path": "/"}'),
                )
            ],
        )
        response = SimpleNamespace(
            choices=[SimpleNamespace(message=message)]
        )
        fake_client = SimpleNamespace(
            chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs: response))
        )
        self.gw.default_provider = "external_api_openai_compatible"
        self.gw.openai_client = fake_client

        content, thinking, tool_calls = self.gw._call_openai([], None)
        self.assertEqual(content, "call me")
        self.assertEqual(thinking, "reasoning here")
        self.assertEqual(tool_calls[0]["id"], "call_123")
        self.assertEqual(tool_calls[0]["name"], "listfiles")
        self.assertEqual(tool_calls[0]["arguments"], {"path": "/"})


class TestStream(unittest.TestCase):
    def setUp(self):
        self.gw = Gateway(tools=get_tools())
        self.gw.ollama_model = "test-model"

    @patch.object(
        gateway_module.ollama,
        "chat",
        return_value=[
            _ollama_message(content="Hel"),
            _ollama_message(content="lo there"),
        ],
    )
    def test_stream_content(self, mock_chat):
        chunks = list(self.gw.stream_text("Hi"))
        self.assertEqual(chunks, [
            StreamChunk("content", "Hel"),
            StreamChunk("content", "lo there"),
        ])

    @patch.object(
        gateway_module.ollama,
        "chat",
        return_value=[
            _ollama_message(thinking="I think"),
            _ollama_message(content="Answer"),
        ],
    )
    def test_stream_thinking_and_content(self, mock_chat):
        chunks = list(self.gw.stream_text("Why?"))
        self.assertEqual(chunks, [
            StreamChunk("thinking", "I think"),
            StreamChunk("content", "Answer"),
        ])

    def test_stream_tool_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "data.txt").touch()
            first_turn = [
                {"message": {"role": "assistant", "content": "", "thinking": "", "tool_calls": [
                    {"function": {"name": "listfiles", "arguments": {"path": tmp}}}
                ]}}
            ]
            second_turn = [_ollama_message(content="Here is the list.")]
            with patch.object(
                gateway_module.ollama,
                "chat",
                side_effect=[first_turn, second_turn],
            ) as mock_chat:
                chunks = list(self.gw.stream_text("List the files"))

        types = [chunk.type for chunk in chunks]
        self.assertIn("tool_result", types)
        self.assertEqual(chunks[-1], StreamChunk("content", "Here is the list."))
        self.assertEqual(mock_chat.call_count, 2)

    @patch.object(
        gateway_module.ollama,
        "chat",
        side_effect=lambda **kwargs: [{"message": {"role": "assistant", "content": "", "thinking": "", "tool_calls": [
            {"function": {"name": "broken_tool", "arguments": {}}}
        ]}}],
    )
    def test_stream_max_iterations(self, mock_chat):
        chunks = list(self.gw.stream_text("Loop"))
        self.assertEqual(chunks[-1], StreamChunk("error", "Maximum tool iterations reached."))


if __name__ == "__main__":
    unittest.main()