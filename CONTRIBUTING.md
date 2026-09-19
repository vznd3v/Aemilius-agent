# Collaborating on Aemilius Agent

Thank you for your interest in **Aemilius Agent**!

## 🚧 Current Status: Pre-Alpha (v0.0.1)

The project is currently under active foundational development. Because core architectures, APIs, and project layouts are evolving rapidly, formal contribution rules (such as strict branching strategies, pull request templates, and issue labeling) are temporarily on hold.

**A comprehensive contribution guideline and formal PR process will be established once we reach version `v0.1`.**

---

## 💬 Want to collaborate early?

If you are genuinely interested in contributing, brainstorming features, or testing early builds before the v0.1 release:

1. **Reach out on Discord:** Send a direct message to **`vzn.d3v`**.
2. Let's discuss what you would like to work on and coordinate together!

---

## 🛠️ Development Setup

If you want to run and experiment with the project locally:

```bash
# Clone the repository
git clone https://github.com/vznd3v/Aemilius-agent.git
cd Aemilius-agent

# Install dependencies using uv
uv sync

# Compile the Rust core module
uv run maturin develop

# Run the CLI
uv run aemilius-agent

# Run linter & tests
uv run ruff check .
uv run python -m unittest tests/test_interface.py
```

Stay tuned for our upcoming `v0.1` milestone!
