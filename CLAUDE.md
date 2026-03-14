# miniclaw — Claude용 프로젝트 요약

## 개요

텔레그램 봇 + OpenAI. 사용자 메시지를 프리셋(키→고정 답변) 또는 스킬 문서(.md)로 처리하고, 없으면 OpenAI로 응답합니다.

## 스택

- **Python 3.12**
- **python-telegram-bot** (봇)
- **openai** (채팅 완성)
- **python-dotenv** (`.env` 로드)
- **ruff** (린트/포맷), **pre-commit** (커밋 전 자동 실행)

## 규칙·관례

- **명령은 모두 `/` 로 시작**: `/help`, `/updatepreset`, `/skills`, `/addskills`, `/skill` 등.
- **설정·비밀**: `.env`에 `TELEGRAM_BOT_TOKEN`, `OPENAI_API_KEY`. `.env`는 `.gitignore`에 있음.
- **에셋**:
  - 프리셋: `asset/presets.json` + `asset/presets.py` (load/save/key_exists/add/overwrite).
  - 스킬: `asset/skills/` 아래 `.md` 파일 + `asset/skill_db.py` (list/get/add/remove).
- **명령 등록**: `telegram_ai_bot.py`의 `COMMANDS` 리스트에 `(명령어, 핸들러, 한줄설명, 상세설명)` 튜플 추가. `/help`는 여기서 자동 생성.

## 주요 파일

| 경로 | 역할 |
|------|------|
| `telegram_ai_bot.py` | 앱 생성, COMMANDS 등록, 메시지/명령 핸들러, OpenAI 호출 |
| `dummy_run.py` | Fake Update/Context로 같은 로직 테스트 (텔레그램 없이) |
| `asset/presets.py` | 프리셋 JSON DB (기본값·재귀 방지 주의) |
| `asset/skill_db.py` | `asset/skills/*.md` 읽기/쓰기, 슬러그 파일명 |
| `asset/skills/README.md` | `/skills` 호출 시 보여줄 기본 문서 |

## 플로우 요약

1. **일반 메시지**: addskill 대기 중이면 이름/설명 수집 후 .md 저장. 그다음 예/아니오(덮어쓰기) → 프리셋 매칭 → 없으면 OpenAI.
2. **`/updatepreset 키: 값`**: 키 없으면 추가, 있으면 예/아니오로 덮어쓰기.
3. **`/addskills`**: 다음 메시지 = 스킬 이름, 그다음 = 설명 → `asset/skills/<slug>.md` 생성.

수정 시: 명령 추가는 COMMANDS + 핸들러만 추가하면 되고, 프리셋/스킬 로직은 asset 쪽만 건드리면 됩니다.
