"""サンプルのワークスペースの決まった形を確かめる.

- スキル・AGENTS.md などに `` ` `` で囲んで書いたワークスペースのパスが、実際にあるか
- 各スキルの SKILL.md の frontmatter に name と description があり、name がフォルダ名と同じか

見つかった問題を表示し、1つでもあれば終了コード 1 で終わる。
"""

import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent / "sample-workspace"

# ワークスペースのパスとして扱う書き出し（これ以外の `...` はコマンドや語なので見ない）
PATH_PREFIXES = ("gtd/", "me/", "logs/", "reviews/", "zettelkasten/", ".claude/")
ROOT_FILES = ("AGENTS.md", "CLAUDE.md")

# 日付や番号を当てはめるパターン（`logs/logs_YYYY.md`・`<タスク文言>` など）は見ない
PLACEHOLDER = re.compile(r"YYYY|MM|DD|HHmm|<|>|\*")

# ないのが正しいもの（例として書いたパス）。足すときは理由も書く
ALLOWED_MISSING = {
    # AGENTS.md の読み取りポリシーで、要確認の領域の例として書いている
    "gtd/006_document/life/money/",
}

CODE_SPAN = re.compile(r"`([^`\n]+)`")


def is_workspace_path(text: str) -> bool:
    """`...` の中身が、ワークスペースのパスとして書かれたものか."""
    if " " in text:
        return False
    return text.startswith(PATH_PREFIXES) or text in ROOT_FILES


def check_paths() -> list[str]:
    """Markdown に書かれたパスが、ワークスペースにあるかを確かめる."""
    problems = []
    for md in sorted(WORKSPACE.rglob("*.md")):
        if ".obsidian" in md.parts:
            continue
        lines = md.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, start=1):
            for text in CODE_SPAN.findall(line):
                if not is_workspace_path(text) or PLACEHOLDER.search(text):
                    continue
                if text in ALLOWED_MISSING or (WORKSPACE / text).exists():
                    continue
                where = md.relative_to(WORKSPACE.parent)
                problems.append(f"{where}:{lineno}: `{text}` がない")
    return problems


def read_frontmatter(path: Path) -> dict[str, str] | None:
    """先頭の --- で囲まれた frontmatter を、key: value の辞書にする."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None
    fields = {}
    for line in lines[1:]:
        if line == "---":
            return fields
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return None


def check_skills() -> list[str]:
    """各スキルの SKILL.md の frontmatter を確かめる."""
    problems = []
    skills_dir = WORKSPACE / ".claude" / "skills"
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        where = skill_md.relative_to(WORKSPACE.parent)
        if not skill_md.exists():
            problems.append(f"{where}: SKILL.md がない")
            continue
        fields = read_frontmatter(skill_md)
        if fields is None:
            problems.append(f"{where}: frontmatter（先頭の --- の囲み）がない")
            continue
        for key in ("name", "description"):
            if not fields.get(key):
                problems.append(f"{where}: frontmatter に {key} がない")
        if fields.get("name") and fields["name"] != skill_dir.name:
            problems.append(
                f"{where}: name（{fields['name']}）がフォルダ名（{skill_dir.name}）と違う"
            )
    return problems


def main() -> int:
    problems = check_paths() + check_skills()
    for problem in problems:
        print(problem)
    if problems:
        print(f"問題が {len(problems)} 件ある")
        return 1
    print("ワークスペースのパスと SKILL.md の frontmatter に問題はない")
    return 0


if __name__ == "__main__":
    sys.exit(main())
