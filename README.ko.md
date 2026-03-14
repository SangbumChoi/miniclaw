[한국어](README.ko.md) · [English](README.md) · [中文](README.zh.md)

---

# miniclaw

텔레그램 AI 봇. OpenAI로 일반 답변, 프리셋(키워드→고정 답변), 스킬 문서(.md)를 지원합니다.

## 요구 사항

- Python 3.12+
- `.env`에 `TELEGRAM_BOT_TOKEN`, `OPENAI_API_KEY` 설정

## 설치

```bash
pip install -r requirements.txt
cp .env.example .env   # 실제 토큰/키 입력
```

개발 시 (pre-commit, ruff, 커밋 규칙):

```bash
pip install -r requirements-dev.txt
pre-commit install
```

커밋 메시지는 [Conventional Commits](https://www.conventionalcommits.org/) 형식 ([docs/COMMIT_CONVENTION.md](docs/COMMIT_CONVENTION.md)), 예: `feat(bot): 명령 추가`, `fix: 재귀 방지`.

## 실행

- **텔레그램 봇**: `python telegram_ai_bot.py`
- **더미 모드** (텔레그램 없이 터미널에서 테스트): `python dummy_run.py`

## 명령어 (모두 `/` 로 시작)

| 명령 | 설명 |
|------|------|
| `/help` | 명령 목록 |
| `/help 명령이름` | 해당 명령 상세 사용법 |
| `/updatepreset 키: 값` | 프리셋 추가·덮어쓰기 (키 있으면 예/아니오) |
| `/skills` | 스킬 사용법 문서 보기 |
| `/skills 이름` | 해당 스킬 .md 내용 보기 |
| `/addskills` | 새 스킬 추가 (이후 채팅으로 이름 → 설명 입력) |
| `/skill list` | 스킬 목록 |
| `/skill remove 이름` | 스킬 삭제 |

일반 메시지는 프리셋에 있으면 그대로 답하고, 없으면 OpenAI로 답합니다.

## 디렉터리 구조

```
miniclaw/
  telegram_ai_bot.py   # 봇 진입점
  dummy_run.py         # 텔레그램 없이 입력→응답 테스트
  asset/
    presets.py         # 프리셋 DB (JSON)
    presets.json
    skill_db.py        # 스킬 .md 읽기/쓰기
    skills/            # 스킬 마크다운 문서
      README.md        # /skills 시 표시
  .env.example
  requirements.txt
  ruff.toml, .pre-commit-config.yaml
```

## 라이선스

LICENSE 파일 참고.
