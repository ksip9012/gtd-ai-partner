"""足した行に、個人の情報の語が入っていないかを確かめる.

- 基準のコミットからの差分で足した行と、まだ追跡していないファイルの行を見る
- 語のリストは、環境変数 `PRIVATE_WORDS`（1行 1語）か、
  `$XDG_CONFIG_HOME/gtd-ai-partner/private-words.txt`（既定は `~/.config/...`）から読む。
  空行と `#` で始まる行は飛ばす。大文字・小文字は区別しない
- 語のリストそのものが個人の情報なので、一致したときもファイル名と行番号だけを出す（decisions/0005）

基準のコミットは、環境変数 `PRIVATE_WORDS_BASE` か、なければ `origin/main` との分かれ目。
見つかったら終了コード 1 で終わる。
"""

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
NO_COMMIT = "0" * 40


def git(*args: str) -> str:
    """リポジトリの中で git を動かし、標準出力を返す（日本語のファイル名も、そのままの形で受け取る）."""
    return subprocess.run(
        ["git", "-c", "core.quotePath=false", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def load_words() -> list[str]:
    """語のリストを読む。どこにもなければ空のリストを返す."""
    text = os.environ.get("PRIVATE_WORDS", "")
    if not text.strip():
        config = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
        path = config / "gtd-ai-partner" / "private-words.txt"
        if path.is_file():
            text = path.read_text(encoding="utf-8")
    words = []
    for line in text.splitlines():
        word = line.strip()
        if word and not word.startswith("#"):
            words.append(word.casefold())
    return words


def base_commit() -> str:
    """足した行を比べる基準のコミット."""
    base = os.environ.get("PRIVATE_WORDS_BASE", "").strip()
    if base and base != NO_COMMIT:
        return base
    return git("merge-base", "HEAD", "origin/main").strip()


def added_lines(base: str) -> list[tuple[str, int, str]]:
    """基準のコミットから足した行を (ファイル名, 行番号, 中身) で返す."""
    lines = []
    path = ""
    number = 0
    for line in git("diff", "-U0", "--no-color", base, "--").splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else ""
        elif match := HUNK.match(line):
            number = int(match.group(1))
        elif line.startswith("+") and path:
            lines.append((path, number, line[1:]))
            number += 1
    for path in git("ls-files", "--others", "--exclude-standard").splitlines():
        try:
            text = (ROOT / path).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            lines.append((path, number, line))
    return lines


def main() -> int:
    """足した行を語のリストと比べ、見つかった場所を出す."""
    words = load_words()
    if not words:
        if os.environ.get("CI") != "true":
            print("語のリストがないので、確かめなかった（手元では通す）")
            return 0
        if os.environ.get("GITHUB_ACTOR") == "dependabot[bot]":
            print("::warning::Dependabot の PR には Secrets が渡らないので、確かめなかった")
            return 0
        print("::error::Secrets の PRIVATE_WORDS が空。語のリストを登録する（README の「開発」）")
        return 1

    found = [
        f"{path}:{number}"
        for path, number, text in added_lines(base_commit())
        if any(word in text.casefold() for word in words)
    ]
    if found:
        print("個人の情報の語を含む行がある（語と行の中身は出さない）:")
        for place in found:
            print(f"  {place}")
        return 1
    print(f"足した行に、語のリストの語はなかった（{len(words)} 語）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
