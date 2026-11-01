---
name: weekly-review
description: GTDの週次レビューの下書きを作る。「週次レビューして」「今週の振り返りを作って」のように依頼されたときに使う。
---

# Weekly Review

ワークスペースの現状から週次レビューの下書きを作り、`template.md` の形式でユーザーに提示する。GTD の週次レビュー（Get Clear / Get Current / Get Creative）に沿う。

## 対象期間

- 週に1回、決まった曜日の朝にやる（`gtd/002_todo.md` のルーティン）。決めたことをその日のうちに動かせるよう、夜より朝がよい
- 対象は、前回の週次レビューの翌日から実行した時点まで
- 見出しの週番号は、実行日を含む ISO 週にする
- ユーザーが期間を指定したらそれに従う
- 月末に近い週次レビューの日は、続けて月次レビューをする（手順は `reviews/00_trigger_list/003_月次レビュー.md`）。報告でそう伝える

## 手順

1. 材料を集める（読むだけで、この段階ではどのファイルも変更しない）
  - 今週やったこと: `gtd/007_done_YYYY-MM.md`（月をまたぐ週は両方）
  - 気づき: `reviews/01_daily/YYYY/YYYY-MM.md` の `Y` / `W`
  - 体: `logs/logs_YYYY.md` と `logs/training_YYYY.jsonl`（筋トレ）。物差しは `gtd/006_document/ai-partner/trainer.md` の数値をそのまま使う（言い換えない）。月の累計距離などは月初からの合計を出す
    - 筋トレは、形式と進め方の決まり（次のステップに進む目安、まだやらない種目など）が `logs/training.md` にある。種目ごとの偏りと進み具合を見る。目安がまだ書かれていない種目は「目安が未記入」と書く
  - 変更の流れ: `git log --since=<週の開始日> --stat`（Inbox に何が入り何が処理されたかの補助）
  - Inbox: `gtd/001_inbox.md` の残件数
  - カレンダー・Todo: `gtd/002_todo.md`
    - 「動いていない」の判定は `git log -S '<タスク文言>' -- gtd/002_todo.md` で追加日を見る
  - Waiting For: `gtd/004_waiting_for.md`
  - Someday/Maybe: `gtd/005_someday_maybe.md`
  - プロジェクト: `gtd/003_project/` のフォルダ（`00000000_archive` と、`gtd/005_someday_maybe.md` の「止めているプロジェクト」に載っているものは除く）。各プロジェクト名で `gtd/002_todo.md` に Next Action（`プロジェクト名:` で始まるタスク）があるか照合する
  - AI の助言の確認: 今週の日次レビュー・朝の秘書・やりとりで AI が出した助言と作業の報告（「確かめた」「直した」など）を、`gtd/006_document/ai-partner/advice-checklist.md`（共通の項目は `AGENTS.md` にもある）と物差しに突き合わせる
    - ずれごとに当たる項目（C1・T2 など）を書き、ずれの数を先週と並べる（点数は数だけ）
    - ずれていたものは、そのスキルの Gotchas と、チェックリストの「もとにしたずれ」に足したかも確かめる。どの項目にも当たらないずれは、新しい項目の候補として「提案」に挙げる
  - AI に任せてよかったこと: 今週の done・日次レビューの Y から、AI がやった作業（スキルの手順、調べもの、まとめなど）を拾い、候補として一言ずつ挙げる。時間は測らない
  - Zettelkasten 昇格候補: 今週更新された `gtd/006_document/` と `gtd/003_project/` から、`zettelkasten/000_rules.md` の昇格基準に合いそうなもの
2. `template.md` の形式で下書きを作る
  - 見出しは `## YYYY-Www (MM/DD〜MM/DD)`
  - 「頭の中の気になること」「来週のフォーカス」はユーザーが書く欄なので空のまま残す
  - 該当なしの項目は「なし」と書く（項目自体は消さない）
  - 箇条書きのインデントはスペース2個
3. 下書きをユーザーに提示し、`reviews/02_weekly/YYYY.md` の先頭（frontmatter とタイトルの直後）に追記する。ファイルがなければ下記の frontmatter で作る
4. 「提案（未適用）」に挙げた変更（todo の整理、waiting_for の催促、プロジェクトのアーカイブなど）は、ユーザーが承認したものだけ各ファイルに反映する
  - todo に追加するタスクは `gtd/008_rules/009_task_add_checklist.md` に従う
  - 完了扱いにしたものは `gtd/007_done_YYYY-MM.md` に記録する

## 新規ファイルの frontmatter

```markdown
---
tags:
  - gtd/reviews
---

# 週次レビュー YYYY
```

## 完了後の報告

- 下書きの保存先（またはチャットに出したこと）
- ユーザーに記入してほしい欄
- 承認待ちの提案の件数

## Gotchas

（まだ記録なし。実際に誤判定・想定外の入力などに遭遇したら、ここに追記していく）
