import os

from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from asset.presets import add_preset, key_exists, load_presets, overwrite_preset
from asset.skill_db import (
    add_skill_doc,
    get_main_doc,
    get_skill_content,
    list_skill_names,
    remove_skill_doc,
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(TELEGRAM_TOKEN)
print(OPENAI_API_KEY)

client = OpenAI(api_key=OPENAI_API_KEY)

# 명령 레지스트리: (명령어, 핸들러, 한줄 설명, 상세설명 또는 None)
COMMANDS: list[tuple[str, callable, str, str | None]] = []


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    # /help 또는 /help 명령어
    args = text.replace("/help", "", 1).strip().split()
    if args:
        cmd = args[0].lower()
        for c, _, short, detail in COMMANDS:
            if c == cmd:
                msg = f"/{c} - {short}"
                if detail:
                    msg += f"\n\n{detail}"
                await update.message.reply_text(msg)
                return
        await update.message.reply_text(f"'{cmd}' 명령은 없어요. /help 로 목록을 보세요.")
        return
    lines = ["아래 명령어를 사용할 수 있어요.", ""]
    for c, _, short, _ in COMMANDS:
        lines.append(f"/{c} - {short}")
    lines.append("")
    lines.append("자세한 사용법: /help 명령이름")
    await update.message.reply_text("\n".join(lines))


async def handle_updatepreset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """예: /updatepreset 안녕: 반가워요  또는  /updatepreset key: value"""
    text = (update.message.text or "").strip()
    args = text.replace("/updatepreset", "", 1).strip()
    if ":" not in args:
        await update.message.reply_text(
            "사용법: /updatepreset 키: 값\n예: /updatepreset 안녕: 반가워요"
        )
        return

    key_part, _, value_part = args.partition(":")
    key = key_part.strip().lower()
    value = value_part.strip()
    if not key or not value:
        await update.message.reply_text("키와 값 모두 입력해 주세요.")
        return

    if key_exists(key):
        context.user_data["pending_preset"] = {"key": key, "value": value}
        await update.message.reply_text(
            f"이미 '{key}' 키가 있습니다. 덮어쓸까요? (예/아니오)"
        )
        return

    add_preset(key, value)
    await update.message.reply_text(f"추가했습니다: '{key}' → '{value}'")


async def handle_skills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """예: /skills → 사용법 문서, /skills <이름> → 해당 스킬 .md 내용"""
    text = (update.message.text or "").strip()
    args = text.replace("/skills", "", 1).strip().split(maxsplit=1)
    name = args[1].strip() if len(args) > 1 else ""

    if not name:
        content = get_main_doc()
        await update.message.reply_text(content)
        return
    doc = get_skill_content(name)
    if doc is None:
        await update.message.reply_text(f"'{name}' 스킬 문서가 없어요. /skill list 로 목록을 보세요.")
        return
    await update.message.reply_text(doc)


async def handle_addskills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/addskills → 이후 채팅으로 이름·설명 받아 .md 저장"""
    context.user_data["addskill_step"] = "name"
    await update.message.reply_text("새 스킬의 **이름**(파일명에 쓸 이름)을 한 줄로 보내주세요.")


async def handle_skill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """예: /skill list, /skill remove 이름 (스킬 목록·삭제, 추가는 /addskills)"""
    text = (update.message.text or "").strip()
    args = text.replace("/skill", "", 1).strip().split(maxsplit=1)
    sub = args[0].lower() if args else ""
    rest = args[1].strip() if len(args) > 1 else ""

    if sub == "list":
        names = list_skill_names()
        if not names:
            await update.message.reply_text("등록된 스킬이 없어요. /addskills 로 추가하세요.")
            return
        lines = ["등록된 스킬 (문서 이름):", ""] + [f"• {n}" for n in names]
        await update.message.reply_text("\n".join(lines))
        return

    if sub == "remove":
        if not rest:
            await update.message.reply_text("사용법: /skill remove 이름")
            return
        if remove_skill_doc(rest):
            await update.message.reply_text(f"'{rest}' 스킬 문서를 삭제했어요.")
        else:
            await update.message.reply_text(f"'{rest}' 스킬은 없어요.")
        return

    await update.message.reply_text(
        "사용법:\n"
        "/skill list - 스킬 목록\n"
        "/skill remove 이름 - 스킬 삭제\n"
        "스킬 추가: /addskills 후 채팅으로 이름·설명 입력"
    )


# 레지스트리: (명령어, 핸들러, /help 한줄 설명[, 상세설명])
COMMANDS: list[tuple[str, callable, str, str | None]] = []
COMMANDS.extend([
    ("help", handle_help, "이 명령 목록 보기", "/help [명령] — 해당 명령 사용법"),
    (
        "updatepreset",
        handle_updatepreset,
        "키:값 으로 프리셋 추가·덮어쓰기",
        "예: /updatepreset 안녕: 반가워요. 키 있으면 예/아니오로 덮어쓸지 묻습니다.",
    ),
    (
        "skills",
        handle_skills,
        "스킬 사용법 문서 보기 (또는 /skills 이름)",
        "예: /skills → 사용법, /skills 날씨 → 날씨.md 내용",
    ),
    (
        "addskills",
        handle_addskills,
        "새 스킬 추가 (이후 채팅으로 이름·설명 → .md 저장)",
        "예: /addskills 후 이름 보내기, 이어서 설명 보내기",
    ),
    ("skill", handle_skill, "스킬 목록·삭제 (list / remove)", "예: /skill list, /skill remove 이름"),
])


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = (update.message.text or "").strip()
    key = user_text.lower()

    # /addskills 플로우: 이름 → 설명 순서로 받아 .md 저장
    addskill_step = context.user_data.get("addskill_step")
    if addskill_step == "name":
        context.user_data["addskill_name"] = user_text
        context.user_data["addskill_step"] = "content"
        await update.message.reply_text("이제 이 스킬에 대한 **설명**을 채팅으로 보내주세요. 여러 줄 가능해요.")
        return
    if addskill_step == "content":
        name = context.user_data.pop("addskill_name", "unnamed")
        context.user_data.pop("addskill_step", None)
        slug = add_skill_doc(name, user_text)
        await update.message.reply_text(f"스킬 문서를 저장했어요: `{slug}.md`")
        return

    # 예/아니오 대기 중이면 프리셋 덮어쓰기 분기 처리
    pending = context.user_data.get("pending_preset")
    if pending:
        if key in ("예", "yes", "y"):
            overwrite_preset(pending["key"], pending["value"])
            context.user_data.pop("pending_preset", None)
            await update.message.reply_text("덮어썼습니다.")
            return
        if key in ("아니오", "no", "n"):
            context.user_data.pop("pending_preset", None)
            await update.message.reply_text("취소했습니다.")
            return
        await update.message.reply_text("예 또는 아니오로 답해 주세요.")
        return

    presets = load_presets()
    if key in presets:
        await update.message.reply_text(presets[key])
        return

    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {"role": "user", "content": user_text}
        ]
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

for cmd, handler, *_ in COMMANDS:
    app.add_handler(CommandHandler(cmd, handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


def _run_as_bot():
    app.run_polling()


if __name__ == "__main__":
    _run_as_bot()
