# #1 作者の Vault 固有のものの洗い出し（2026-11-01）

スキル 4つ（daily-review・morning-brief・weekly-review・inbox-triage）と、その付属ファイル（`daily-review/calendar.md`・`weekly-review/template.md`）、`AGENTS.md` を `rg` で調べた。

写す前に洗い出したのは、そのまま写してコミットすると、カレンダーの ID などが git の履歴に残り、Public にしたときに見えてしまうため。**作者の Vault のファイルを、そのままこのリポジトリにコミットしない。**

## 洗い出した結果

| 種類 | 例 | どこに | 件数の目安 |
| --- | --- | --- | --- |
| A. Vault のファイルのパス（番号付きの名前） | `gtd/004_todo.md`、`gtd/003_done_YYYY-MM.md`、`reviews/01_daily/YYYY/YYYY-MM.md`、`gtd/005_rules/…` | 4つとも | 多い |
| B. 作者のプロジェクトのファイル | AIパートナーの memo（トレーナーの物差し・朝のニュースの形）、助言の評価のチェックリスト、定番のご飯のリスト、期限と誕生日の表 | morning-brief・weekly-review | 6か所ほど |
| C. Vault の外の場所 | 外出先のポスト（別リポジトリ）、garmin-log の置き場所 | morning-brief・weekly-review・inbox-triage | 4か所 |
| D. アカウント・ID | Google カレンダーの ID、GitHub のアカウント名 | `daily-review/calendar.md`、`AGENTS.md` | 3か所 |
| E. 作者の決めごと・数値 | ジョグの曜日、BB最大の目安、週の 10km 超えの上限、囚人トレーニングの種目、苦手な食べ物、ゴミの日 | daily-review・morning-brief・weekly-review | 多い |
| F. 経緯の日付 | 「2026-10-25 決定」など | daily-review 5・morning-brief 10・weekly-review 4・calendar.md 1 | 20か所 |
| G. v0.2 に回す機能 | Google カレンダーへの写し、朝のニュース、garmin-log の実行 | daily-review・morning-brief・weekly-review | 各 1〜3か所 |
| H. `AGENTS.md` の作者固有の部分 | git の構成（3つのリポジトリ）、要確認の領域のパス、外出先のポスト | `AGENTS.md` | 節ごと |

## 直し方の案（決める前）

- A: サンプル Vault を作者と同じフォルダの形にすれば、パスは変えずに済む
- B: 決めごとは、サンプル Vault の決まった場所の参照ファイルに出し、スキルからはそこを読む
- C: 外出先のポストは任意の機能にする。garmin-log は v0.2 に回すので外す
- D: カレンダーへの写しは v0.2 に回すので、`calendar.md` ごと v0.1 に入れない。`AGENTS.md` はひな形に書き直す
- E: 数値や曜日はスキルに書かず、サンプル Vault の `me/` や物差しのファイル（B）に置く。スキルには「物差しの数値をそのまま使う」だけを書く
- F: 経緯の日付は外す（経緯は作者の Vault に残る）。ただし「なぜそうするか」の理由は残す
- G: v0.1 のスキルからは外す
- H: `AGENTS.md` はひな形として書き直す（読み取りポリシーの考え方は残し、パスは例にする）
