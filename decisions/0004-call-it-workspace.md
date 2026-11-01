# 0004. 「Vault」ではなく「ワークスペース」と呼び、サンプルは `sample-workspace/` に置く

- Status: Accepted
- Date: 2026-11-01

## Context
0001〜0003 では、Markdown のファイルを集めたフォルダを「Vault」と呼んでいた。「Vault」は Obsidian の用語で、このリポジトリは Obsidian がなくても、Markdown のファイルと AI エージェントだけで動く。Obsidian を使っていない人には伝わりにくい。

候補は 3つあった。

- ワークスペース（`sample-workspace/`）: AI エージェントが作業する1つのフォルダという意味で通じやすい。VSCode のワークスペースと言葉がかぶる
- ナレッジベース（`sample-knowledge-base/`）: `AGENTS.md` の「AI向けのパーソナルナレッジベース」と揃うが、todo やログまで入る場所としては大げさ
- ノートのフォルダ（`sample-notes/`）: いちばん平易だが、自分用のメモの置き場 `notes/` と紛らわしい

## Decision
「ワークスペース」と呼ぶ。サンプルのフォルダは `sample-vault/` から `sample-workspace/` に名前を変える。作者自身のフォルダも「作者のワークスペース」と呼ぶ。

0001〜0003 は、決めたときの記録としてそのまま残す（本文の「Vault」と、0003 の `sample-vault/` は、この ADR で読み替える）。

## Consequences
- Obsidian を使っていない人にも、何のフォルダかが伝わる
- 0001〜0003 と、ほかのファイルで言葉が違う。0001〜0003 を読む人のために、この ADR で読み替えを示した
- 作者自身も、自分のフォルダの呼び方を少しずつ「Vault」から移していく（このリポジトリとは別に進める）
