# 🦉 Athena — Personal AI Operating System

> A local-first, privacy-preserving AI assistant that runs entirely on your laptop.  
> Athena orchestrates agents, manages tasks, learns from your behaviour, and keeps your data on-device.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Athena](#running-athena)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Athena is a modular, agent-driven Personal AI Operating System built with:

| Layer | Technology |
|---|---|
| UI | PySide6 (Qt 6) + qasync |
| AI / LLM | Ollama (local inference) |
| Database | SQLAlchemy 2 + aiosqlite (SQLite WAL) |
| Scheduling | Custom asyncio-based persistent scheduler |
| Agents | Plugin-style agent architecture |
| Prompt Layer | Jinja2-rendered YAML prompt templates |

Athena runs **entirely offline** — no data leaves your machine unless you explicitly enable optional cloud integrations (GitHub, Telegram).

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                   PySide6 UI Layer                    │
│  (AthenaMainWindow, Chat, Task Board, Goal Tracker)  │
└────────────────────────┬─────────────────────────────┘
                         │  Events / Signals
┌────────────────────────▼─────────────────────────────┐
│                  Use-Case Layer                       │
│  AgentCoordinator · Planner · Memory · Telemetry     │
└────────────────────────┬─────────────────────────────┘
                         │  Abstractions (ABCs)
┌────────────────────────▼─────────────────────────────┐
│                  Domain Layer                         │
│  Entities: Task, Goal, Memory, Event, UserState      │
└────────────────────────┬─────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────┐
│               Infrastructure Layer                    │
│  SQLAlchemy · EventBroker · Scheduler · OllamaClient │
└──────────────────────────────────────────────────────┘
```

Athena follows **Clean Architecture** principles:

- **Domain** — pure Python entities, zero external dependencies.
- **Use Cases** — orchestration logic, depends only on domain abstractions.
- **Adapters** — concrete implementations (SQLite repos, Ollama client, Qt views).
- **Infrastructure** — cross-cutting concerns: DB session, event broker, scheduler.

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.11+ | Required for modern type hints |
| [Ollama](https://ollama.com) | Latest | Local LLM inference engine |
| Recommended model | `qwen2.5:7b` | `ollama pull qwen2.5:7b` |
| Fast/light model | `qwen2.5:1.5b` | `ollama pull qwen2.5:1.5b` |
| Git | Any | For cloning |

> **Note:** Ollama must be running (`ollama serve`) before launching Athena.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/project-athena.git
cd project-athena
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Edit `.env` and set your values (Ollama URL, optional tokens, etc.).

### 5. Pull required Ollama models

```bash
ollama pull qwen2.5:7b
ollama pull qwen2.5:1.5b
```

### 6. Initialize the database

The database is created automatically on first run at `data/athena.db`.

---

## Running Athena

```bash
# From the project root, with your virtual environment active:
python -m athena.main
```

Or if using the `src/` layout with `PYTHONPATH`:

```bash
# Windows
set PYTHONPATH=src
python -m athena.main

# macOS / Linux
PYTHONPATH=src python -m athena.main
```

---

## Project Structure

```
Project Athena/
├── src/
│   └── athena/
│       ├── main.py                  # Application entry point
│       ├── domain/                  # Pure entities & repository ABCs
│       │   ├── entities/            # Task, Goal, Memory, UserState, ...
│       │   └── repositories/        # Abstract repository interfaces
│       ├── usecases/                # Business logic, no framework imports
│       │   ├── agent/               # AgentCoordinator, BaseAgent
│       │   ├── planner/             # DailyPlanner, WeeklyPlanner
│       │   ├── memory/              # MemoryConsolidation, WorkingMemory
│       │   ├── tasks/               # TaskManager
│       │   ├── goals/               # GoalManager
│       │   ├── feature_flags/       # FeatureFlagManager
│       │   ├── user_state/          # UserStateManager
│       │   ├── resource/            # ResourceManager
│       │   ├── security/            # SecurityManager
│       │   └── telemetry/           # TelemetrySubsystem
│       ├── adapters/                # Concrete implementations
│       │   ├── ui/                  # PySide6 views, widgets, models
│       │   ├── db/                  # SQLAlchemy ORM models & repos
│       │   ├── llm/                 # OllamaClient, PromptRenderer
│       │   └── agents/              # Concrete agents (email, github, ...)
│       ├── infrastructure/          # Cross-cutting concerns
│       │   ├── db_session.py        # SQLAlchemy engine & session factory
│       │   ├── event_broker.py      # Async pub-sub broker
│       │   ├── scheduler.py         # Persistent cron scheduler
│       │   └── qt_bridge.py         # asyncio ↔ Qt signal bridge
│       └── prompts/                 # Jinja2 YAML prompt templates
│           └── v1/                  # Versioned prompt set
├── config/
│   ├── settings.yaml                # System-wide configuration
│   ├── flags.json                   # Feature flag toggles
│   └── security_policy.json         # Security constraints
├── data/                            # Runtime data (gitignored)
│   └── athena.db                    # SQLite database
├── logs/                            # Log files (gitignored)
├── tests/
│   ├── unit/                        # Fast, isolated unit tests
│   └── integration/                 # Tests requiring DB / Ollama
├── .env                             # Local environment (gitignored)
├── .env.example                     # Environment template
├── requirements.txt                 # Python dependencies
└── README.md
```

---

## Configuration

### Environment Variables (`.env`)

| Variable | Default | Description |
|---|---|---|
| `ATHENA_OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `ATHENA_OLLAMA_DEFAULT_MODEL` | `qwen2.5:7b` | Primary LLM model |
| `ATHENA_OLLAMA_FAST_MODEL` | `qwen2.5:1.5b` | Fast/cheap model for classification |
| `ATHENA_DB_PATH` | `data/athena.db` | SQLite database path |
| `ATHENA_LOG_LEVEL` | `INFO` | Logging verbosity |
| `ATHENA_GITHUB_TOKEN` | *(empty)* | Optional: GitHub personal access token |
| `ATHENA_TELEGRAM_BOT_TOKEN` | *(empty)* | Optional: Telegram bot token |
| `ATHENA_TELEGRAM_CHAT_ID` | *(empty)* | Optional: Telegram chat ID |

### System Config (`config/settings.yaml`)

Fine-grained control over scheduler intervals, agent polling rates, memory consolidation, resource thresholds, and notification settings.

### Feature Flags (`config/flags.json`)

Toggle features without code changes. Set any flag to `true` or `false`.

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository and create a feature branch: `git checkout -b feat/my-feature`
2. **Follow Clean Architecture** — domain entities must have zero external imports.
3. **Add type hints** on all functions and class attributes (Python 3.11+ style).
4. **Write tests** — place unit tests in `tests/unit/` and integration tests in `tests/integration/`.
5. **Run tests** before submitting: `pytest tests/`
6. **Docstrings** — every public class and method must have a docstring.
7. **Commit style** — use conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`.
8. Open a **Pull Request** against `main` with a clear description of your changes.

### Code Style

- Formatter: `black` (line length 100)
- Linter: `ruff`
- Type checker: `mypy --strict`

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built with ❤️ as a local-first alternative to cloud AI assistants.*
