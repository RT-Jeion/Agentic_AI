# Agentic_AI — Telegram RAG Bot

Project Agentic_AI is a Telegram chat bot that stores data in MongoDB and provides retrieval-augmented generation (RAG) helpers. It supports two RAG modes:

- Static Book RAG: answers queries using a pre-ingested book/knowledge base (local/static embeddings).
- Live Web RAG: fetches and indexes web content on demand to answer questions using fresh web sources.

Key features

- Telegram chat interface for conversational queries.
- Message, user and vector data persisted in MongoDB.
- Two RAG systems: static (book) and live (web) for flexible QA.
- Modular code: embedding, DB, bot, and helper utilities separated into files.

Repository layout

- [admin.py](admin.py) — Admin utilities and maintenance commands.
- [app.py](app.py) — (If present) small web or helper app entrypoint.
- [db_handle.py](db_handle.py) — MongoDB interaction helpers.
- [tele_bot.py](tele_bot.py) — Main Telegram bot implementation and handlers.
- [vector_embed.py](vector_embed.py) — Vector embedding and retrieval helpers (used by RAG systems).
- [user_tools.py](user_tools.py) — Utilities for user data management.
- [requirements.txt](requirements.txt) — Python dependencies.
- [users.json](users.json) — Example or cached user data.

Environment & configuration

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Required environment variables (example names; adjust to match your code):

- `MONGO_URI` — MongoDB connection URI.
- `TELEGRAM_BOT_TOKEN` — Telegram bot token for the bot in `tele_bot.py`.

If your project expects different names, pass them or set them in your environment before running.

Running the bot

Start the Telegram bot (example):

```bash
export MONGO_URI="mongodb://localhost:27017/yourdb"
export TELEGRAM_BOT_TOKEN="<your-bot-token>"
python tele_bot.py
```

RAG systems overview

- Static Book RAG: ingest a book or corpus into the vector store (via `vector_embed.py`) and persist vectors. The bot queries that vector store to produce context for generation.
- Live Web RAG: on user request the bot fetches web content, converts it to text, creates embeddings, and queries the vector store to produce up-to-date context.

Data storage

The bot stores user info, messages, and vector metadata in MongoDB. Backups and indexes are recommended for production workloads.

Notes & next steps

- Verify the exact environment variable names in `db_handle.py` and `tele_bot.py` and update the example commands accordingly.
- If you want, I can add a small ingestion script for the static book RAG and a sample `.env` file.

Contributing

Open an issue or send a pull request with improvements. For quick changes, run tests (if any) and ensure linting/formatting matches the project.

License

Add a license if you plan to publish this project (e.g., MIT).
