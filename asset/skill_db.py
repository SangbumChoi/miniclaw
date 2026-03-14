# 스킬을 asset/skills/ 폴더의 .md 파일로 관리

import re
from pathlib import Path

_ASSET_DIR = Path(__file__).resolve().parent
SKILLS_DIR = _ASSET_DIR / "skills"
MAIN_DOC = "README.md"


def _ensure_skills_dir() -> None:
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)


def _slug(name: str) -> str:
    """파일명에 쓸 수 있는 문자열로 변환."""
    s = name.strip().lower()
    s = re.sub(r"[^\w\u3131-\u318e\uac00-\ud7a3\-]+", "_", s)
    return s or "unnamed"


def list_skill_names() -> list[str]:
    """skills 폴더 내 .md 파일명(확장자 제외) 목록. README 제외."""
    _ensure_skills_dir()
    names = []
    for p in SKILLS_DIR.glob("*.md"):
        if p.name.lower() != MAIN_DOC.lower():
            names.append(p.stem)
    return sorted(names)


def get_skill_content(name: str) -> str | None:
    """해당 이름의 .md 내용. 없으면 None."""
    _ensure_skills_dir()
    slug = _slug(name)
    path = SKILLS_DIR / f"{slug}.md"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def get_main_doc() -> str:
    """README.md 내용. 없으면 기본 문구 반환."""
    _ensure_skills_dir()
    path = SKILLS_DIR / MAIN_DOC
    if path.exists():
        return path.read_text(encoding="utf-8")
    return (
        "# Skills\n\n"
        "`/skills` — 이 문서\n"
        "`/skills <이름>` — 해당 스킬 문서 보기\n"
        "`/addskills` — 새 스킬 추가 (채팅으로 이름·설명 입력)\n"
        "`/skill list` — 스킬 목록\n"
        "`/skill remove <이름>` — 스킬 삭제"
    )


def add_skill_doc(name: str, content: str) -> str:
    """스킬 .md 추가. 실제 사용된 파일명(슬러그) 반환."""
    _ensure_skills_dir()
    slug = _slug(name)
    path = SKILLS_DIR / f"{slug}.md"
    path.write_text(content.strip(), encoding="utf-8")
    return slug


def remove_skill_doc(name: str) -> bool:
    """해당 스킬 .md 삭제. 성공 시 True."""
    _ensure_skills_dir()
    slug = _slug(name)
    path = SKILLS_DIR / f"{slug}.md"
    if not path.exists():
        return False
    path.unlink()
    return True


def skill_doc_exists(name: str) -> bool:
    return get_skill_content(name) is not None
