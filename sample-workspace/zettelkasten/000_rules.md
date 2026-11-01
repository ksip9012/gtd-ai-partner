---
tags:
  - zettelkasten/rules
---

# Zettelkasten 運用ルール

`gtd/006_document/`（type: knowledge）との役割分担と、昇格基準をまとめる。

## `006_document`（knowledge型）との違い

- `006_document`（knowledge型）: 単なる事実・資料。分野で引く「読めば分かる」参考資料
- `zettelkasten`: 自分の考え・解釈が乗っていて、既存の別ノート（Permanent Note）と最低1つリンクできるもの

判断に迷ったら「これは他のどのノートの考えと繋がるか」を自問する。繋がらなければ`006_document`（knowledge型）に留める。無理にリンクを作ってZettelkasten側に置かない。

## ノートの種類

- **Fleeting Note**: `gtd/001_inbox.md` がこれを兼ねる。専用フォルダは持たない
- **Permanent Note** (`permanent/`): 1議題のみを扱う。他のPermanent Noteと最低1つリンクしている
  - ファイル名: `YYYYMMDDHHmm_タイトル.md`（作成日時を ID にする）。リンクは `[[YYYYMMDDHHmm_タイトル]]` の形で張る

## Permanent Noteへの昇格手順

1. `006_document`（knowledge型）のノートを読み返しているとき、または`003_project`が完了してアーカイブするときに、自分の考え・解釈が練れてきたものがないか確認する
2. それが既存のPermanent Noteと最低1つリンクできるなら `permanent/` に新規ノートを作成し、双方向にリンクする
3. まだどのノートともリンクできない場合は、無理に昇格させず元の場所に留める
