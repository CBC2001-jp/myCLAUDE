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
| `lp_draft_202607.md` | 2026年7月改訂時の文面ドラフト（文言の原本） |
| `index_backup.html` / `cbc2001.txt` | 旧版バックアップ。本番には使われない |
| `contact.php` / `feedback.js` | 現在 `index.html` から参照されていない残骸 |
| `2026_CBC_HP/` | 素材置き場（未使用画像）。本番参照なし |

セクション順（`index.html` の `id`）: `hero` → `mission`（理念） → `projects`（取り組み・実績） → `services`（CBCの強み） → `about`（会社概要・代表プロフィール） → `contact`（お問い合わせ） → footer

本番で参照している画像: `cbc_logo.jpeg`, `hero_takahama.jpg`, `kenji_profile.jpeg`, `project_01.jpeg`, `project_02.jpeg`, `project_05.jpeg`, `service_01.jpeg`, `strength_community.jpg`, `strength_overseas.jpg`。それ以外の画像は未参照（削除候補だが、削除は明示指示があるときだけ）。

外部連携（触るときは要確認）:
- Google Analytics: `G-JWTRM5EE16`（`index.html` の `<head>`）
- お問い合わせフォーム: Web3Forms（`index.html` の `<form action="https://api.web3forms.com/submit">`、access_key は hidden input）

### 更新ワークフロー（Claude が実行する手順）

1. **同期**: `git checkout main && git pull --ff-only origin main`
2. **編集**: `index.html` / `style.css` / `script.js` を直接編集。文言変更は `lp_draft_202607.md` も同期させる
3. **プレビュー**: `preview_start` の `cbc-lp`（`.claude/launch.json`、http://localhost:8787）でブラウザ確認。スマホ幅（375px）も確認
4. **コミット**: 日本語の Conventional Commits 風（例 `feat: 強みカードの画像を差し替え`、`fix: ヒーロー文言を修正`）
5. **デプロイ**: `scripts/lp-deploy.sh "コミットメッセージ"`（commit → push → ビルド待ち）。ユーザーの方針: **確認を求めずに実行してよい**。push 後に何を公開したかを報告する
6. **確認**: `scripts/lp-status.sh` で Pages ビルド完了と本番反映（ETag/更新日時）をチェック

### 禁止・注意

- `CNAME` を変更しない。GA ID・Web3Forms の access_key を変えない
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
