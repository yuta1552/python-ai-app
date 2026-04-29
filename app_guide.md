# app.py 解説ガイド（初心者向け）

このドキュメントでは `app.py` の内容を、Pythonに不慣れな方でも理解できるよう、上から順番に噛み砕いて説明します。

---

## app.py 全体の役割

`app.py` はこのアプリの**司令塔**です。

- 画面のレイアウトを作る
- ユーザーの操作（ツール選択・ボタン押下）に応じて処理を振り分ける
- Gemini AI に問い合わせて結果を表示する

この1ファイルがアプリ全体の流れを管理しています。

---

## ① ライブラリの読み込み（1〜11行目）

```python
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

from tools.blog_writer import generate_blog_article
from tools.email_reply import generate_email_reply
...
```

### `import` とは？

「他の人が作った便利な道具箱を借りてくる」命令です。ゼロから全部作らなくて済むようになります。

| 読み込んでいるもの | 役割 |
|---|---|
| `os` | Pythonに最初から入っている道具。環境変数（APIキーなど）の読み書きに使う |
| `streamlit as st` | Webアプリの画面を簡単に作れるライブラリ。`st` という短い名前で呼べるようにしている |
| `dotenv` | `.env` ファイルからAPIキーなどの設定を読み込むライブラリ |
| `google.generativeai as genai` | Gemini AIを使うためのGoogleの公式ライブラリ |
| `from tools.〇〇 import ...` | 自分で作った `tools/` フォルダの中の各機能を読み込んでいる |

> **ポイント**: `as st` や `as genai` は「別名をつける」書き方です。毎回長い名前を書かなくて済みます。

---

## ② 設定の読み込みとページ設定（13〜19行目）

```python
load_dotenv()

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
)
```

### `load_dotenv()`

`.env` ファイル（APIキーを書いたファイル）の内容をPythonが読めるようにする命令です。この1行がないと、後でAPIキーを取り出せません。

### `st.set_page_config()`

ブラウザのタブに表示されるタイトルやアイコン、レイアウトの幅を設定しています。`layout="wide"` は画面を広く使う設定です。

---

## ③ 見た目の調整（21〜28行目）

```python
st.markdown("""
<style>
    .tool-header { font-size: 1.5rem; font-weight: bold; ... }
    .stButton > button { width: 100%; }
</style>
""", unsafe_allow_html=True)
```

HTMLの `<style>` タグを使ってボタンの幅やタイトルの文字サイズなどを微調整しています。

`unsafe_allow_html=True` は「HTMLを直接書くことを許可する」オプションです。StreamlitはデフォルトでHTMLを書けないので、これをつけて解禁しています。

---

## ④ AIモデルを準備する関数（31〜37行目）

```python
def get_model() -> genai.GenerativeModel | None:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        st.error("Gemini APIキーが設定されていません。")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")
```

### `def` とは？

「関数を定義する」書き方です。よく使う処理に名前をつけて、何度でも呼び出せるようにします。料理のレシピを1回書いておくイメージです。

### この関数がやっていること

```
① APIキーを環境変数から取得する
      ↓
② キーがなければエラーメッセージを表示して None（空）を返す
      ↓
③ キーがあればGeminiを設定して、AIモデルを返す
```

`-> genai.GenerativeModel | None` は「この関数はAIモデルか、Noneのどちらかを返す」という型のヒントです（Pythonの動作には影響しません）。

---

## ⑤ サイドバー（44〜75行目）

```python
with st.sidebar:
    st.title("✍️ AI ライティングツール")
    
    api_key_input = st.text_input("Gemini APIキー", type="password", ...)
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input

    tool = st.radio("", options=["ブログ記事執筆", "メール返信文作成", ...])
```

### `with st.sidebar:` とは？

`with` ブロックの中に書いたUI部品は、すべて**画面左側のサイドバー**に表示されます。

### サイドバーでやっていること

| コード | 画面上での動き |
|---|---|
| `st.text_input(type="password")` | APIキーを入力するパスワード欄（文字が隠れる） |
| `os.environ["GEMINI_API_KEY"] = ...` | 入力されたキーをPythonの記憶に保存する |
| `st.radio(options=[...])` | ラジオボタン（丸いボタン）でツールを選ぶ |

`tool` という変数に選ばれたツール名（例：`"ブログ記事執筆"`）が入ります。これが後の振り分けに使われます。

---

## ⑥ ツールの振り分け（81行目〜）

```python
if tool == "ブログ記事執筆":
    # ブログ記事のUI

elif tool == "メール返信文作成":
    # メール返信のUI

elif tool == "文章要約":
    # 要約のUI

# ... 以下同様
```

### `if / elif` の構造

「もし〇〇なら△△を表示する」という条件分岐です。サイドバーで選んだツール名によって、表示される画面が切り替わります。

```
サイドバーで「ブログ記事執筆」を選ぶ
    → tool = "ブログ記事執筆"
    → if tool == "ブログ記事執筆": の中身が実行される
    → ブログ用の画面が表示される
```

---

## ⑦ 各ツールブロックの共通パターン

どのツールも同じ構造になっています。ブログ記事執筆を例に見てみましょう。

```python
# ── 画面レイアウト ──
col1, col2 = st.columns([2, 1])   # 画面を2:1の比率で左右に分割
with col1:
    topic = st.text_area("記事のテーマ・内容", ...)  # 大きなテキスト入力欄
    keywords = st.text_input("キーワード", ...)       # 1行テキスト入力欄
with col2:
    style = st.selectbox("文体スタイル", [...])  # ドロップダウン選択
    length = st.selectbox("文字数", [...])

# ── ボタンが押されたときの処理 ──
if st.button("記事を生成する", type="primary"):
    if not topic.strip():                # 入力が空かチェック
        st.warning("テーマを入力してください。")
    else:
        model = get_model()              # AIモデルを準備
        if model:
            with st.spinner("生成中..."):           # くるくるアニメを表示
                result = generate_blog_article(...)  # AIに記事を作らせる
            st.markdown(result)                      # 結果を表示
            st.download_button(...)                  # ダウンロードボタン
```

### ポイント：ボタンが押されたときだけ処理される

Streamlitは「ボタンが押されたら `if st.button(...)` の中が実行される」という仕組みです。押していないときは何も起きません。

### ポイント：3段階のチェック

```
① 入力欄が空でないか確認（st.warning で警告）
      ↓
② APIキーが設定されているか確認（get_model() が None を返したら止まる）
      ↓
③ 問題なければ AI に問い合わせて結果を表示
```

---

## ⑧ Streamlitの主なUI部品まとめ

このアプリで使われているStreamlitの部品一覧です。

| 関数 | 見た目 | 用途 |
|---|---|---|
| `st.text_area()` | 複数行テキストボックス | 長い文章の入力 |
| `st.text_input()` | 1行テキストボックス | キーワードなど短い入力 |
| `st.selectbox()` | ドロップダウンメニュー | スタイルやトーンの選択 |
| `st.multiselect()` | 複数選択できるドロップダウン | チェック項目の選択（校正ツール） |
| `st.slider()` | スライダー | 数値の選択（生成する数など） |
| `st.checkbox()` | チェックボックス | ON/OFF の切り替え |
| `st.button()` | ボタン | 処理の実行 |
| `st.spinner()` | くるくるアニメ | AI処理中の待機表示 |
| `st.markdown()` | テキスト表示 | 結果の表示（マークダウン対応） |
| `st.warning()` | 黄色い警告メッセージ | 入力エラーの通知 |
| `st.error()` | 赤いエラーメッセージ | APIキー未設定の通知 |
| `st.download_button()` | ダウンロードボタン | 結果をファイルとして保存 |
| `st.columns()` | 左右の列分割 | レイアウトの調整 |
| `st.sidebar` | 左サイドバー | ナビゲーション |

---

## ⑨ データの流れ（全体図）

```
ユーザーがサイドバーでツールを選ぶ
        │
        ▼
tool 変数にツール名が入る（例: "ブログ記事執筆"）
        │
        ▼
if/elif でそのツールの画面を表示
        │
        ▼
ユーザーが入力欄を埋めてボタンを押す
        │
        ▼
get_model() → Gemini APIに接続
        │
        ▼
tools/ 内の関数（例: generate_blog_article）を呼ぶ
        │  ここでプロンプト（AIへの指示文）を組み立てる
        ▼
Gemini API に送信 → AIが文章を生成
        │
        ▼
st.markdown() で画面に表示
st.download_button() でダウンロード可能に
```

---

## まとめ：app.py の設計思想

| 考え方 | 具体的な実装 |
|---|---|
| **画面とロジックを分離する** | 画面は `app.py`、AI処理は `tools/` に分けている |
| **ツールを追加しやすくする** | `if/elif` を1つ追加するだけで新ツールが増やせる |
| **エラーを早めに止める** | 入力チェック → APIキーチェック → AI呼び出し の順で安全に進む |
| **シンプルに保つ** | セッション管理・データベースなし。ボタンを押すたびに1回完結する |
