# 0005. 個人の情報の語は、リポジトリの外のリストで確かめる

- Status: Accepted
- Date: 2026-11-15

## Context

サンプルのワークスペースは、作者のワークスペースから個人の情報を外して写している（decisions/0002）。外し忘れがないかは、写すたびに手で `rg` して確かめていたが、手で忘れると止まらない。確かめたい語（住んでいる場所・手元のパス・人名など）は、そのリスト自体が個人の情報なので、リポジトリには置けない。

## Decision

語のリストはリポジトリの外に置き、足した行だけを `scripts/check_private_words.py` で確かめる。

- 置き場所: 手元は `~/.config/gtd-ai-partner/private-words.txt`（1行 1語）。CI は同じ中身を Secrets の `PRIVATE_WORDS` に登録する
- 見る範囲: 基準のコミット（PR の base、main への push では push の前）からの差分で足した行と、まだ追跡していないファイル。前からある行は見ない
- 一致したときの表示: ファイル名と行番号だけ。語と行の中身は出さない（複数行の Secrets は、行ごとにログで伏せられるとは限らないため）
- リストが空のとき: 手元はお知らせを出して通す（作者以外がクローンしても動くように）。CI では、Dependabot の PR だけ警告を出して通す（Actions の Secrets が渡らず、依存の更新だけなので個人の情報は入らない）。それ以外は落として、Secrets の登録漏れに気づけるようにする

## Consequences

- 写すときの手作業の `rg` は、`mise run check-private` に置き換えられる。CI でも止まる
- 語を足すときは、手元のファイルを直してから、Secrets にも入れ直す（`gh secret set PRIVATE_WORDS < ~/.config/gtd-ai-partner/private-words.txt`）。2か所がずれないように、手元のファイルを正にする
- 前からある行は見ないので、すでに入ってしまった語は見つけられない。語を足したときは、手元で `PRIVATE_WORDS_BASE` に空の木（`git hash-object -t tree /dev/null` の値）を渡すと、全部の行を確かめられる
- フォークからの PR には Secrets が渡らないので落ちる。作者ひとりのリポジトリなので、今は困らない
