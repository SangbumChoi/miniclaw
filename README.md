[한국어](README.ko.md) · [English](README.md) · [中文](README.zh.md)

---

# miniclaw

A Telegram AI bot. It uses OpenAI for general replies, presets (keyword → fixed reply), and skill docs (.md).

## Requirements

- Python 3.12+
- Set `TELEGRAM_BOT_TOKEN` and `OPENAI_API_KEY` in `.env`

## Install

```bash
pip install -r requirements.txt
cp .env.example .env   # Fill in your tokens/keys
```

For development (pre-commit, ruff, commit message convention):

```bash
pip install -r requirements-dev.txt
pre-commit install
```

Commits must follow [Conventional Commits](https://www.conventionalcommits.org/) (see [docs/COMMIT_CONVENTION.md](docs/COMMIT_CONVENTION.md)), e.g. `feat(bot): add command`, `fix: avoid recursion`.

## Run

- **Telegram bot**: `python telegram_ai_bot.py`
- **Dummy mode** (test in terminal without Telegram): `python dummy_run.py`

## Commands (all start with `/`)

| Command | Description |
|---------|-------------|
| `/help` | List commands |
| `/help command` | Detailed usage for that command |
| `/updatepreset key: value` | Add or overwrite preset (prompts yes/no if key exists) |
| `/skills` | Show skills usage doc |
| `/skills name` | Show content of that skill .md |
| `/addskills` | Add new skill (then send name → description in chat) |
| `/skill list` | List skills |
| `/skill remove name` | Remove skill |

Regular messages are answered from presets when matched; otherwise the bot uses OpenAI.

## Directory structure

```
miniclaw/
  telegram_ai_bot.py   # Bot entrypoint
  dummy_run.py         # Input→reply test without Telegram
  asset/
    presets.py         # Preset DB (JSON)
    presets.json
    skill_db.py        # Skill .md read/write
    skills/            # Skill markdown docs
      README.md        # Shown for /skills
  .env.example
  requirements.txt
  ruff.toml, .pre-commit-config.yaml
```

## License

See LICENSE file.
