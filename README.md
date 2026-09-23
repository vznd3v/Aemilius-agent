<div align="right">
   <img src="./Design%20sans%20titre%20(3).png" alt="Logo Aemilius Agent" width="72" style="border-radius: 10px;">
</div>

# Aemilius Agent

![banner](./Gemini_Generated_Image_gj2u77gj2u77gj2u.jpeg)

> **Explore unfamiliar codebases through a focused terminal assistant.**

[![Version](https://img.shields.io/badge/version-pre--alpha_v0.0.1-yellow.svg)](https://github.com/vznd3v/Aemilius-agent)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Aemilius Agent** is a Python terminal assistant for exploring unfamiliar codebases. It connects an LLM provider to a small set of filesystem tools and presents the result through a Rich-based interactive CLI.

## Features

- **Codebase exploration**: list directories and read file contents through agent tools.
- **Multi-provider gateway**: use local Ollama models or OpenAI-compatible APIs such as OpenRouter.
- **Streaming responses**: stream text, reasoning, tool results, and provider errors through one gateway interface.
- **Tool calling**: execute `listfiles`, `readfile`, and `quit` from model-generated tool calls.
- **Terminal Markdown**: render agent responses with Rich, including syntax-highlighted code blocks.
- **Token statistics**: show provider usage when available and a clearly marked estimate otherwise.
- **File references**: autocomplete files and directories after typing `@` in the prompt.
- **Tested core**: unit tests cover the gateway, tools, streaming, Markdown rendering, and completion.

## Architecture

```text
Aemilius-agent/
├── src/agent/
│   ├── cli/                # Terminal interface, Markdown renderer, prompt completion
│   ├── config/             # Provider configuration
│   ├── gateway/            # Provider calls, streaming, tool-call normalization
│   ├── tools/              # Filesystem and session tools
│   └── main.py             # CLI entry point
├── tests/                  # Unit and integration tests
├── pyproject.toml          # Python project and command configuration
└── README.md
```

The main boundaries are:

```text
CLI -> Gateway -> LLM provider
              -> Tools
```

The CLI owns presentation. The gateway owns provider communication, streaming, tool-call execution, errors, and usage extraction. Tools remain provider-independent.

## Getting Started

### Requirements

- Python `3.11` or newer;
- `uv`, recommended for dependency management;
- Ollama, only when using the local provider;
- an OpenRouter or other OpenAI-compatible API key, only when using an external provider.

### Installation

```bash
git clone https://github.com/vznd3v/Aemilius-agent.git
cd Aemilius-agent
uv sync
```

The package uses Maturin as its build backend because the repository still contains an experimental Rust module. The current CLI, gateway, and tools are implemented in Python.

### Provider configuration

The default provider and model are configured in `src/agent/config/config.json`.

For an external OpenAI-compatible provider, create a local `.env` file:

```dotenv
EXTERNAL_API_KEY=replace_with_your_api_key
```

`OPENAI_API_KEY` is also supported. `.env` is ignored by Git and must never be committed.

For Ollama, install the selected model and start the service:

```bash
ollama pull qwen3:4b
ollama serve
```

Start the CLI with:

```bash
uv run aemilius-agent
```

### Examples

```text
Aemilius > list the files in /path/to/project
Aemilius > read src/agent/main.py
Aemilius > what is inside @src/agent/gateway/gateway.py
```

Type `@` followed by a path fragment to autocomplete files and directories from the current working directory.

## Built-in tools

- `listfiles`: list entries in a directory.
- `readfile`: read and return the complete content of a file.
- `quit`: stop the interactive session.

Tool calls are exposed when the request concerns files or directories. The gateway normalizes streamed tool-call fragments from OpenAI-compatible providers before executing them.

## Roadmap

- [ ] Add architecture and dependency graph tools.
- [ ] Add flowchart generation and a graphical flowchart view.
- [ ] Add a CLI splash screen.
- [ ] Add a `/provider` command for changing providers during a session.

## Contributing

The project is in active **pre-alpha (`v0.0.1`)**. Bug reports, provider compatibility notes, tests, and focused improvements are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow.

## License

Distributed under the MIT License. See `LICENSE` for more information.
