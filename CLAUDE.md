# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリで作業する際のガイダンスを提供します。

## コマンド

```bash
# 依存ライブラリのインストール
pip install -r requirements.txt

# アプリの起動
streamlit run app.py
```

APIキーは `.env.example` をコピーして `.env` ファイルに `GEMINI_API_KEY=...` として設定する。
起動後にサイドバーから直接入力することも可能。

## アーキテクチャ

`app.py` が唯一のStreamlit UIファイルであり、レイアウトとルーティングをすべて担う。
サイドバーの `st.radio` でアクティブなツールを選択し、トップレベルの `if/elif` チェーンが対応するUIブロックを描画する。
各ブロックは入力を受け取り、`get_model()` で `genai.GenerativeModel` を生成したあと、`tools/` 配下の関数に処理を委譲する。

`tools/` はライティング機能ごとに1モジュール1関数の構成。各関数はPythonの値と設定済みモデルインスタンスを受け取り、日本語プロンプトを組み立て、`model.generate_content(prompt)` を呼び出して `response.text` を返す。

### ツール関数一覧

| モジュール | 関数名 | 主なパラメータ |
|---|---|---|
| `blog_writer.py` | `generate_blog_article` | topic, keywords, style, length |
| `email_reply.py` | `generate_email_reply` | received_email, reply_points, tone |
| `summarizer.py` | `summarize_text` | text, format, length |
| `proofreader.py` | `proofread_text` | text, focus（チェック項目のリスト）|
| `sns_post.py` | `generate_sns_post` | content, platform, tone, include_hashtags |
| `title_generator.py` | `generate_titles` | content, purpose, count |

## モデル設定

- 使用モデル: `gemini-2.5-flash`（`get_model()` 内でハードコード）
- 温度・`generation_config` などのパラメータは未設定（APIデフォルト値を使用）
- モデルを変更する場合は `app.py` の `get_model()` のみ修正すればよい

## プロンプト設計の方針

- すべてのプロンプトは**日本語**で記述し、出力も日本語を前提とする
- プロンプト末尾に「構成」「出力形式」「条件」セクションを設けて出力の形を明示する
- ユーザー入力はf文字列でプロンプトに直接埋め込む（サニタイズ不要、個人用ツールのため）
- 選択肢ラベル（スタイル・トーン等）を辞書でプロンプト用自然言語に変換してから埋め込む

## UIの設計規則

- レイアウト: `st.columns([2, 1])` または `st.columns([3, 1])` の2カラム構成（左に入力、右にオプション）
- 生成ボタンは `type="primary"` で統一
- AI呼び出し中は `st.spinner(...)` でラップする
- 生成結果は `st.markdown(result)` で表示し、直後に `st.download_button` を配置する
- バリデーションエラーは `st.warning`、APIキー未設定は `st.error` を使う

## 状態管理

`st.session_state` は使用していない。ボタンを押すたびに独立したAPI呼び出しが発生する。
生成結果はStreamlitのリランによってリセットされるため、結果を保持したい場合は `st.session_state` への保存が必要になる。

## 新しいツールの追加手順

1. `tools/my_tool.py` を作成し、`def my_tool(..., model: genai.GenerativeModel) -> str` を1つ実装する
2. `app.py` でインポートし、サイドバーの `st.radio` の `options` リストにツール名を追加する
3. `app.py` に `elif` ブロックを追加してUIを描画し、作成した関数を呼び出す
