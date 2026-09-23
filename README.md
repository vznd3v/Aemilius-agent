# ▦ Aemilius Agent

![banner](./Gemini_Generated_Image_gj2u77gj2u77gj2u.jpeg)



> **Understand external codebases quickly, simply, and effortlessly.**

[![Version](https://img.shields.io/badge/version-pre--alpha_v0.0.1-yellow.svg)](https://github.com/vznd3v/Aemilius-agent)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Rust](https://img.shields.io/badge/rust-2021_edition-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Aemilius Agent** is a lightweight developer assistant designed to help you onboard into and explore unfamiliar codebases—whether it is a trending open-source repository on GitHub or an internal codebase at a new company.

It uses Python for agentic reasoning and LLM workflows, coupled with direct command-execution tools for flexible file and directory inspection.

---

## ✨ Features

- 🛠️ **Command-Driven Exploration**: Real-time filesystem and directory inspection powered by dedicated command tools (replacing the earlier obsolete Rust indexing prototype).
- 🖥️ **Minimalist & Beautiful CLI**: Built with `rich` and `prompt-toolkit`—clean, responsive, and lightweight without terminal bloat.
- 💬 **Interactive Agent Chat**: Conversational AI context (powered by Ollama with local models such as `llama3.2:1b`, and OpenAI/custom endpoints soon).
- 🧭 **Native Agent Inspection**: Built-in tools for listing files, exploring directory structures, and gathering codebase context.
- 🗺️ **Architecture Mapping *(Coming Soon)***: Automatic dependency graphing and visual architecture charts.
- 🔌 **Zero Config Friction**: Clone, run, and explore immediately.

---

## 🏗️ Architecture Overview

```
Aemilius-agent/
├── src/
│   ├── rust/               # Legacy / experimental Rust module (obsolete, replaced by tools)
│   │   ├── Cargo.toml
│   │   └── lib.rs
│   └── agent/              # Python CLI & Agent Core
│       ├── cli/            # Rich CLI interface (Panel, Prompt, Messages history)
│       └── tools/          # Command-based agent tools (file discovery, inspection)
├── tests/                  # Unit and integration test suite
└── pyproject.toml          # Project configuration (uv + maturin backend)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python**: `>= 3.11`
- **Rust toolchain**: `cargo` & `rustc` (optional if using pre-compiled wheels, required for development)
- **uv** (recommended package manager) or standard `pip`
- **Ollama**: running locally with your model of choice (e.g., `ollama run llama3.2:1b`)

### Installation & Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vznd3v/Aemilius-agent.git
   cd Aemilius-agent
   ```

2. **Sync dependencies and compile the Rust core:**
   ```bash
   uv sync
   uv run maturin develop
   ```

3. **Launch the CLI:**
   ```bash
   uv run aemilius-agent
   ```

---

## 🗺️ Roadmap

- [x] Basic CLI interface with session history and prompt-toolkit integration.
- [x] File inspection tools using command execution (replacing the obsolete Rust indexer).
- [x] Multi-provider LLM gateway (Ollama, OpenAI, and custom OpenAI-compatible endpoints).
- [ ] Tool calling engine for autonomous codebase navigation.
- [ ] Project architecture and dependency chart generation.

---

## 🤝 Contributing & Collaborating

We are currently in active **pre-alpha (v0.0.1)**. 

Official contributing guidelines, pull request templates, and branching conventions will be published once **v0.1** is released. 

If you would like to get involved early, share ideas, or collaborate, reach out directly on Discord: **`vzn.d3v`**.

See [contributing.md](contributing.md) for more details.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
