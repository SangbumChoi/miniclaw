[한국어](README.ko.md) · [English](README.md) · [中文](README.zh.md)

---

# miniclaw

Telegram AI 机器人。支持 OpenAI 通用回复、预设（关键词→固定回复）和技能文档（.md）。

## 要求

- Python 3.12+
- 在 `.env` 中配置 `TELEGRAM_BOT_TOKEN`、`OPENAI_API_KEY`

## 安装

```bash
pip install -r requirements.txt
cp .env.example .env   # 填入实际 token/key
```

开发环境（pre-commit、ruff、提交信息规范）：

```bash
pip install -r requirements-dev.txt
pre-commit install
```

提交信息须符合 [Conventional Commits](https://www.conventionalcommits.org/)（见 [docs/COMMIT_CONVENTION.md](docs/COMMIT_CONVENTION.md)），例如 `feat(bot): add command`、`fix: avoid recursion`。

## 运行

- **Telegram 机器人**：`python telegram_ai_bot.py`
- **模拟模式**（无需 Telegram，在终端测试）：`python dummy_run.py`

## 命令（均以 `/` 开头）

| 命令 | 说明 |
|------|------|
| `/help` | 命令列表 |
| `/help 命令名` | 该命令详细用法 |
| `/updatepreset 键: 值` | 添加/覆盖预设（键存在时询问是否覆盖） |
| `/skills` | 查看技能使用说明 |
| `/skills 名称` | 查看该技能 .md 内容 |
| `/addskills` | 添加新技能（随后在聊天中发送 名称 → 说明） |
| `/skill list` | 技能列表 |
| `/skill remove 名称` | 删除技能 |

普通消息先匹配预设回复，无匹配时由 OpenAI 回复。

## 目录结构

```
miniclaw/
  telegram_ai_bot.py   # 机器人入口
  dummy_run.py         # 无 Telegram 时的输入→回复测试
  asset/
    presets.py         # 预设 DB (JSON)
    presets.json
    skill_db.py        # 技能 .md 读写
    skills/            # 技能 Markdown 文档
      README.md        # /skills 时显示
  .env.example
  requirements.txt
  ruff.toml, .pre-commit-config.yaml
```

## 许可证

见 LICENSE 文件。
