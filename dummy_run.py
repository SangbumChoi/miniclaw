"""
텔레그램 없이 봇 로직을 테스트하는 더미 러너.
터미널에서 입력하면 봇이 답할 내용을 그대로 출력합니다.
실제 API 호출(OpenAI)은 그대로 이루어지므로 .env 의 OPENAI_API_KEY 가 필요합니다.
"""
import asyncio

# app.run_polling()이 import 시 실행되지 않도록 telegram_ai_bot을 먼저 로드
from telegram_ai_bot import COMMANDS, handle_message


class FakeMessage:
    def __init__(self, text: str):
        self.text = text
        self._replies: list[str] = []

    async def reply_text(self, text: str, **kwargs) -> None:
        self._replies.append(text)

    def get_reply(self) -> str:
        return self._replies[-1] if self._replies else ""


class FakeUpdate:
    def __init__(self, text: str):
        self.message = FakeMessage(text)


class FakeContext:
    def __init__(self, user_data: dict | None = None):
        self.user_data = user_data or {}


async def process_input(text: str, user_data: dict) -> str:
    """한 줄 입력에 대해 봇 응답 문자열을 반환. user_data는 세션 상태(예: 예/아니오 대기) 유지용."""
    text = (text or "").strip()
    if not text:
        return "(빈 입력)"

    update = FakeUpdate(text)
    context = FakeContext(user_data)

    # 명령 라우팅: /로 시작하면 해당 명령 핸들러 실행
    if text.startswith("/"):
        parts = text.lstrip("/").split(maxsplit=1)
        cmd = parts[0].lower()
        for command_name, handler, *_ in COMMANDS:
            if command_name == cmd:
                await handler(update, context)
                return update.message.get_reply()
        # 명령이지만 등록된 명령이 아니면 일반 메시지로 처리 (handle_message가 /help 등 처리하지는 않음)
        await handle_message(update, context)
        return update.message.get_reply()

    await handle_message(update, context)
    return update.message.get_reply()


def main():
    print("봇 더미 모드 (텔레그램 대신 여기서 입력하면 봇 응답을 볼 수 있어요)")
    print("종료: Ctrl+C 또는 빈 줄에서 Enter\n")
    user_data = {}
    while True:
        try:
            line = input("You> ").strip()
        except EOFError:
            break
        if not line:
            continue
        reply = asyncio.run(process_input(line, user_data))
        # process_input 내부에서 context.user_data를 수정하므로 FakeContext.user_data와 user_data가 같은 객체여야 함
        # FakeContext(user_data)로 넘겼으므로 동일 참조. 다음 입력 시 그대로 유지됨.
        print("Bot>", reply, "\n")


if __name__ == "__main__":
    main()
