# 프리셋 답변을 JSON 파일로 DB처럼 관리 (키는 소문자로 저장)
# 명령은 모두 / 로 시작: /updatepreset 키:값 등. 일반 메시지는 프리셋 매칭 후 없으면 AI.

import json
from pathlib import Path

_ASSET_DIR = Path(__file__).resolve().parent
DB_PATH = _ASSET_DIR / "presets.json"

DEFAULT_PRESETS = {
    "안녕": "안녕하세요! 무엇을 도와드릴까요?",
    "hello": "Hello! How can I help you?",
    "뭐해": "저는 여기서 대기 중이에요. 편하게 말씀해 주세요!",
    "도움말": "저에게 아무 말이나 보내주시면 AI가 답변해 드려요. '안녕', '뭐해' 같은 말도 해보세요.",
}


def _ensure_db() -> None:
    """DB 파일이 없으면 기본값으로 한 번만 생성 (재귀 방지: save_presets 호출 안 함)."""
    if not DB_PATH.exists():
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_PRESETS.copy(), f, ensure_ascii=False, indent=2)


def load_presets() -> dict[str, str]:
    _ensure_db()
    with open(DB_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_presets(data: dict[str, str]) -> None:
    _ensure_db()
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def key_exists(key: str) -> bool:
    presets = load_presets()
    return key.strip().lower() in presets


def add_preset(key: str, value: str) -> None:
    """키가 없을 때만 추가. 이미 있으면 예외/False 대신 호출부에서 예/아니오 처리."""
    data = load_presets()
    k = key.strip().lower()
    data[k] = value.strip()
    save_presets(data)


def overwrite_preset(key: str, value: str) -> None:
    data = load_presets()
    data[key.strip().lower()] = value.strip()
    save_presets(data)
