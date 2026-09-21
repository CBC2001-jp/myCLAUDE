# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリ = 有限会社CBC 公式LP（本番）

- 本番URL: https://www.cbc2001.com/
- ホスティング: GitHub Pages（リポジトリ `CBC2001-jp/myCLAUDE`、`main` ブランチ直下、CNAME=`www.cbc2001.com`）
- **`main` に push した内容が数十秒〜数分で本番に反映される。** ステージング環境はない。
- ローカル: `/Users/srv1963/Documents/Claude/myCLAUDE`（`origin/main` と同期して作業する）

### サイト構成（ビルド不要の静的サイト）

| ファイル | 役割 |
|---|---|
| `index.html` | ページ本体（1ページLP、日本語） |
| `style.css` | スタイル全体 |
| `script.js` | ナビ・ハンバーガー・フェードイン等の挙動 |
| `CNAME` | 独自ドメイン設定。**変更・削除禁止** |
| `.nojekyll` | Pages の Jekyll 処理を無効化（2026-09-15 にビルド失敗の対処で追加）。**削除禁止** |
| `lp_draft_202607.md` | 2026年7月改訂時の文面ドラフト（文言の原本） |
| `index_backup.html` / `cbc2001.txt` | 旧版バックアップ。本番には使われない |
| `contact.php` / `feedback.js` | 現在 `index.html` から参照されていない残骸 |
| `2026_CBC_HP/` | 素材置き場（未使用画像）。本番参照なし |

セクション順（`index.html` の `id`）: `hero` → `mission`（理念） → `projects`（取り組み・実績） → `services`（CBCの強み） → `about`（会社概要・代表プロフィール） → footer

**お問い合わせフォームは 2026-09-21 に廃止**（面識のない不特定多数への対応をしない方針）。Contact セクション、`#contact` への全リンク、Web3Forms 送信処理は削除済み。連絡手段は会社概要の `info@cbc2001.com` のみ。ユーザーの指示なしにフォームを復活させない。

本番で参照している画像: `cbc_logo.jpeg`, `hero_takahama.jpg`, `kenji_profile.jpeg`, `project_01.jpeg`, `project_02.jpeg`, `project_05.jpeg`, `service_01.jpeg`, `strength_community.jpg`, `strength_overseas.jpg`。それ以外の画像は未参照（削除候補だが、削除は明示指示があるときだけ）。

外部連携（触るときは要確認）:
- Google Analytics: `G-JWTRM5EE16`（`index.html` の `<head>`）
- 外部へのデータ送信は現在なし（Web3Forms はフォーム廃止に伴い削除）

### 更新ワークフロー（Claude が実行する手順）

1. **同期**: `git checkout main && git pull --ff-only origin main`
2. **編集**: `index.html` / `style.css` / `script.js` を直接編集。文言を変えたら `python3 scripts/sync-draft.py` で文面原本 `lp_draft_202607.md` を再生成する（原本は index.html から生成する写し。手で書き換えない。末尾の「変更記録」だけ追記する）
3. **プレビュー**: `preview_start` の `cbc-lp`（http://localhost:8787）でブラウザ確認。スマホ幅（375px）も確認。設定は Claude Desktop のセッション起点ディレクトリ `~/Documents/Claude/.claude/launch.json`（`--directory myCLAUDE` で配信）と、このリポ直下の `.claude/launch.json`（リポを直接開いた場合用）の2か所にある
4. **コミット**: 日本語の Conventional Commits 風（例 `feat: 強みカードの画像を差し替え`、`fix: ヒーロー文言を修正`）
5. **デプロイ**: `scripts/lp-deploy.sh "コミットメッセージ"`（commit → push → ビルド待ち）。ユーザーの方針: **確認を求めずに実行してよい**。push 後に何を公開したかを報告する
6. **確認**: `scripts/lp-status.sh` で Pages ビルド完了と本番反映（ETag/更新日時）をチェック

### 禁止・注意

- `CNAME` を変更しない。GA ID を変えない
- `main` 以外のブランチに push しても本番には反映されない（レビュー用途にのみ使う）
- 画像は 500KB 程度以下に圧縮してから追加（Pages は 1GB 上限、表示速度のため）
- `2026_CBC_HP/` や `jgrants-mcp/` はLPとは無関係（後者は未追跡の補助金MCPサーバー）

## その他のプロジェクト（参照用）

### myAG — Personal Landing Page (`~/Documents/Claude/myAG/`)
Static site with no build step. Vanilla HTML/CSS/JS. Google Fonts (Noto Sans JP, Noto Serif JP) via CDN.

### OCR Project (`~/Documents/OCR_Project/`)
`python ocr_pdf.py` — batch PDF-to-text with Japanese OCR (pdf2image, pytesseract, Pillow, tqdm; Tesseract `jpn`+`eng`).

### Whisper Environment (`~/whisper-env/`)
`source ~/whisper-env/bin/activate`
