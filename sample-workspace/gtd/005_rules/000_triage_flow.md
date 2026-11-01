---
tags:
  - gtd/rules
---

# 振り分けフロー概要

Inboxの項目がどこに流れていくかの全体像。詳細な判定ルールは各リンク先を参照。

## 1次振り分け（Inbox → GTD）

`001_inbox.md` の項目は、まず通常のGTDフローで振り分ける。

- 不要か（もう意味がない・やらないと決めた）→ 削除
- その場で実行できるか（2分以内）→ その場で実行
- Next Actionか → `004_todo.md`（`009_task_add_checklist.md` 参照）
- 複数ステップ必要なプロジェクトか → `002_project/`
- 資料・知識か → `004_document/`（`010_document_add_checklist.md` 参照）
- 誰かの返答待ちか → `007_waiting_for.md`
- いつかやるかもか → `006_someday_maybe.md`
- 判断できないか → `[要確認]` を付けて `001_inbox.md` に残し、次回処理時に確認する

この時点ではZettelkastenへの分岐は判定しない。

## 2次振り分け（document/project → Zettelkasten）

`004_document` や `002_project` を見返す中で、自分の考え・解釈が練れてきたものがあれば、Permanent Noteへの昇格を検討する（`zettelkasten/000_rules.md` 参照）。

## 全体像

```
Inbox
 ├─ 削除（不要）
 ├─ その場で実行
 ├─ 004_todo.md
 ├─ 002_project/ ──(完了・見返した時に考えが練れたら)──> zettelkasten/permanent/
 ├─ 004_document/ ──(見返した時に考えが練れたら)────────> zettelkasten/permanent/
 ├─ 007_waiting_for.md
 ├─ 006_someday_maybe.md
 └─ [要確認] として Inbox に残す
```
