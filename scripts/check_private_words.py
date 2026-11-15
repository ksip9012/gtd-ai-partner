"""足した行に、個人の情報の語が入っていないかを確かめる.

- 基準のコミットからの差分で足した行と、まだ追跡していないファイルの行を見る
- 基準のコミットから今までのコミット（マージを除く）の、作者・記録者の名前と
  メールアドレス、コミットメッセージも見る（ファイルの外の情報なので、差分には
  出てこない）
- 語のリストは、環境変数 `PRIVATE_WORDS`（1行 1語）か、
  `$XDG_CONFIG_HOME/gtd-ai-partner/private-words.txt`（既定は `~/.config/...`）から読む。
  空行と `#` で始まる行は飛ばす。大文字・小文字は区別しない
- 語のリストそのものが個人の情報なので、一致したときもファイル名と行番号
  （コミットなら短い ID と、作者・記録者・メッセージのどこか）だけを出す
  （decisions/0005）

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


# コミットの情報のうち見るもの（`git log` の書式と、出すときの名前）
COMMIT_FIELDS = (
    ("%an", "作者の名前"),
    ("%ae", "作者のメールアドレス"),
    ("%cn", "記録者の名前"),
    ("%ce", "記録者のメールアドレス"),
    ("%B", "コミットメッセージ"),
)
RECORD_END = "\x1e"
FIELD_END = "\x1f"


def commit_fields(base: str) -> list[tuple[str, str, str]]:
    """基準のコミットから今までのコミットの情報を (短い ID, どこか, 中身) で返す.

    マージのコミットは外す（PR の CI では、GitHub が作るマージのコミットが HEAD
    になるため）。
    """
    fmt = FIELD_END.join(["%h", *(f for f, _ in COMMIT_FIELDS)]) + RECORD_END
    # 基準が空の木（全部を確かめるとき）なら、全部のコミットを見る
    is_tree = git("cat-file", "-t", base).strip() == "tree"
    span = "HEAD" if is_tree else f"{base}..HEAD"
    out = git("log", "--no-merges", f"--format={fmt}", span)
    fields = []
    for record in out.split(RECORD_END):
        parts = record.strip("\n").split(FIELD_END)
        if len(parts) != len(COMMIT_FIELDS) + 1:
            continue
        short, *values = parts
        for (_, name), value in zip(COMMIT_FIELDS, values, strict=True):
            fields.append((short, name, value))
    return fields


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

    def hit(text: str) -> bool:
        return any(word in text.casefold() for word in words)

    base = base_commit()
    found = [
        f"{path}:{number}"
        for path, number, text in added_lines(base)
        if hit(text)
    ]
    found += [
        f"コミット {short} の{name}"
        for short, name, value in commit_fields(base)
        if hit(value)
    ]
    if found:
        print("個人の情報の語を含む場所がある（語と中身は出さない）:")
        for place in found:
            print(f"  {place}")
        return 1
    print(
        f"足した行とコミットの情報に、語のリストの語はなかった（{len(words)} 語）"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
