---
name: inbox-triage
description: GTDのInbox(`gtd/001_inbox.md`)を一次振り分けする。「inboxを整理して」「inbox処理して」のように依頼されたときに使う。
---

# Inbox Triage

`gtd/001_inbox.md` の各項目を、`gtd/008_rules/000_triage_flow.md` の1次振り分けフローに従って処理する。

## 手順

1. `gtd/008_rules/000_triage_flow.md` を読み、1次振り分けの分岐を確認する
2. `gtd/001_inbox.md` を読む。`[要確認]` が付いた項目（前回保留したもの）があれば、まずその判断をユーザーに質問する
3. 項目を1つずつ処理する
  - 不要なもの → 削除する（報告に件名を載せる）
  - その場で実行できるもの → 実行し、`gtd/007_done_YYYY-MM.md` に記録
  - Next Action → `gtd/002_todo.md`（`gtd/008_rules/009_task_add_checklist.md` 参照）
  - 複数ステップ必要なプロジェクト → `gtd/003_project/` に新規作成、または既存プロジェクトに追記
  - 資料・知識 → `gtd/006_document/`（`gtd/008_rules/010_document_add_checklist.md` 参照）
  - 誰かの返答待ち → `gtd/004_waiting_for.md`
  - いつかやるかも → `gtd/005_someday_maybe.md`
4. 処理済みの項目（`[要確認]` を付けたものを除く）は `gtd/001_inbox.md` から削除する
5. 判断に迷う項目は処理せず、行頭に `[要確認]` を付けて `gtd/001_inbox.md` に残し、迷った理由を子項目に書いたうえで質問としてユーザーに提示する

## 完了後の報告

- 何件をどこに振り分けたか
- 削除した項目（件名）
- `[要確認]` として保留にした項目と質問（あれば）

## Gotchas

（まだ記録なし。実際に誤判定・想定外の入力などに遭遇したら、ここに追記していく）
