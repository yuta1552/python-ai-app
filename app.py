import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

from tools.blog_writer import generate_blog_article
from tools.email_reply import generate_email_reply
from tools.summarizer import summarize_text
from tools.proofreader import proofread_text
from tools.sns_post import generate_sns_post
from tools.title_generator import generate_titles

load_dotenv()

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
)

st.markdown("""
<style>
    .tool-header { font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem; }
    .result-box { background-color: #f8f9fa; border-left: 4px solid #4CAF50;
                  padding: 1rem; border-radius: 0.25rem; margin-top: 1rem; }
    .stButton > button { width: 100%; }
</style>
""", unsafe_allow_html=True)


def get_model() -> genai.GenerativeModel | None:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        st.error("Gemini APIキーが設定されていません。サイドバーでAPIキーを入力してください。")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def copy_button(text: str, key: str):
    st.code(text, language="markdown")


# --- Sidebar ---
with st.sidebar:
    st.title("✍️ AI ライティングツール")
    st.markdown("---")

    api_key_input = st.text_input(
        "Gemini APIキー",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help=".envファイルに GEMINI_API_KEY=... と記載するか、ここに直接入力してください",
    )
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input

    st.markdown("---")
    st.markdown("**ツールを選択**")

    tool = st.radio(
        "",
        options=[
            "ブログ記事執筆",
            "メール返信文作成",
            "文章要約",
            "文章校正・改善",
            "SNS投稿文作成",
            "タイトル・見出し生成",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("Powered by Gemini API")


# =====================
# ブログ記事執筆
# =====================
if tool == "ブログ記事執筆":
    st.markdown('<div class="tool-header">ブログ記事執筆</div>', unsafe_allow_html=True)
    st.caption("テーマを入力するだけで、読み応えのあるブログ記事を自動生成します。")

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_area("記事のテーマ・内容", placeholder="例: 初心者向けPythonプログラミングの始め方", height=100)
        keywords = st.text_input("含めたいキーワード（カンマ区切り、任意）", placeholder="例: Python, プログラミング, 入門")
    with col2:
        style = st.selectbox("文体スタイル", ["カジュアル", "フォーマル", "SEO重視"])
        length = st.selectbox("文字数", ["短め（500字程度）", "標準（1000字程度）", "長め（2000字程度）"])

    if st.button("記事を生成する", type="primary"):
        if not topic.strip():
            st.warning("記事のテーマを入力してください。")
        else:
            model = get_model()
            if model:
                with st.spinner("記事を生成中..."):
                    result = generate_blog_article(topic, keywords, style, length, model)
                st.markdown("### 生成された記事")
                st.markdown(result)
                st.download_button("テキストとしてダウンロード", result, file_name="blog_article.txt", mime="text/plain")


# =====================
# メール返信文作成
# =====================
elif tool == "メール返信文作成":
    st.markdown('<div class="tool-header">メール返信文作成</div>', unsafe_allow_html=True)
    st.caption("受信したメールを貼り付けると、適切な返信文を作成します。")

    col1, col2 = st.columns([2, 1])
    with col1:
        received_email = st.text_area("受信したメールの内容", placeholder="ここに受信メールの本文を貼り付けてください...", height=200)
        reply_points = st.text_area("返信で伝えたい要点（任意）", placeholder="例: 来週火曜日に打ち合わせ可能、資料は金曜日までに送付", height=80)
    with col2:
        tone = st.selectbox("返信のトーン", ["丁寧・ビジネス", "カジュアル", "簡潔"])

    if st.button("返信文を生成する", type="primary"):
        if not received_email.strip():
            st.warning("受信したメールの内容を入力してください。")
        else:
            model = get_model()
            if model:
                with st.spinner("返信文を生成中..."):
                    result = generate_email_reply(received_email, reply_points, tone, model)
                st.markdown("### 生成された返信文")
                st.markdown(result)
                st.download_button("テキストとしてダウンロード", result, file_name="email_reply.txt", mime="text/plain")


# =====================
# 文章要約
# =====================
elif tool == "文章要約":
    st.markdown('<div class="tool-header">文章要約</div>', unsafe_allow_html=True)
    st.caption("長い文章を指定した形式・長さで要約します。")

    col1, col2 = st.columns([3, 1])
    with col1:
        text_input = st.text_area("要約したいテキスト", placeholder="ここに要約したい文章を貼り付けてください...", height=250)
    with col2:
        fmt = st.selectbox("出力形式", ["箇条書き", "文章"])
        length = st.selectbox("要約の長さ", ["短め（3〜5行）", "標準（10行程度）", "詳細（20行程度）"])

    if st.button("要約する", type="primary"):
        if not text_input.strip():
            st.warning("要約したいテキストを入力してください。")
        else:
            model = get_model()
            if model:
                with st.spinner("要約中..."):
                    result = summarize_text(text_input, fmt, length, model)
                st.markdown("### 要約結果")
                st.markdown(result)
                st.download_button("テキストとしてダウンロード", result, file_name="summary.txt", mime="text/plain")


# =====================
# 文章校正・改善
# =====================
elif tool == "文章校正・改善":
    st.markdown('<div class="tool-header">文章校正・改善</div>', unsafe_allow_html=True)
    st.caption("文章の誤字・脱字、文法、読みやすさをチェックして改善案を提示します。")

    col1, col2 = st.columns([3, 1])
    with col1:
        text_input = st.text_area("校正したいテキスト", placeholder="ここに校正したい文章を貼り付けてください...", height=250)
    with col2:
        focus = st.multiselect(
            "チェック項目",
            ["誤字・脱字", "文法・表現", "文体の統一", "読みやすさ"],
            default=["誤字・脱字", "文法・表現"],
        )

    if st.button("校正する", type="primary"):
        if not text_input.strip():
            st.warning("校正したいテキストを入力してください。")
        elif not focus:
            st.warning("チェック項目を一つ以上選択してください。")
        else:
            model = get_model()
            if model:
                with st.spinner("校正中..."):
                    result = proofread_text(text_input, focus, model)
                st.markdown("### 校正結果")
                st.markdown(result)
                st.download_button("テキストとしてダウンロード", result, file_name="proofread.txt", mime="text/plain")


# =====================
# SNS投稿文作成
# =====================
elif tool == "SNS投稿文作成":
    st.markdown('<div class="tool-header">SNS投稿文作成</div>', unsafe_allow_html=True)
    st.caption("内容を入力するだけで、各SNSに最適化した投稿文案を3パターン作成します。")

    col1, col2 = st.columns([2, 1])
    with col1:
        content = st.text_area("投稿したい内容・伝えたいこと", placeholder="例: 新しいカフェをオープンしました。手作りスイーツとこだわりのコーヒーが楽しめます。", height=150)
    with col2:
        platform = st.selectbox("プラットフォーム", ["X (Twitter)", "Instagram", "LinkedIn", "Facebook", "note"])
        tone = st.selectbox("投稿のトーン", ["カジュアル", "プロフェッショナル", "エモーショナル", "ユーモア"])
        include_hashtags = st.checkbox("ハッシュタグを含める", value=True)

    if st.button("投稿文を生成する", type="primary"):
        if not content.strip():
            st.warning("投稿したい内容を入力してください。")
        else:
            model = get_model()
            if model:
                with st.spinner("投稿文を生成中..."):
                    result = generate_sns_post(content, platform, tone, include_hashtags, model)
                st.markdown("### 生成された投稿文案")
                st.markdown(result)
                st.download_button("テキストとしてダウンロード", result, file_name="sns_post.txt", mime="text/plain")


# =====================
# タイトル・見出し生成
# =====================
elif tool == "タイトル・見出し生成":
    st.markdown('<div class="tool-header">タイトル・見出し生成</div>', unsafe_allow_html=True)
    st.caption("内容に合った魅力的なタイトルや見出しを複数パターン提案します。")

    col1, col2 = st.columns([2, 1])
    with col1:
        content = st.text_area("内容・テーマ", placeholder="例: 副業で月10万円稼ぐためのフリーランスエンジニアの始め方", height=150)
    with col2:
        purpose = st.selectbox("用途", ["ブログ記事", "メール件名", "SNS投稿", "プレゼン・資料", "YouTube動画"])
        count = st.slider("生成する数", min_value=3, max_value=10, value=5)

    if st.button("タイトルを生成する", type="primary"):
        if not content.strip():
            st.warning("内容・テーマを入力してください。")
        else:
            model = get_model()
            if model:
                with st.spinner("タイトルを生成中..."):
                    result = generate_titles(content, purpose, count, model)
                st.markdown("### 生成されたタイトル案")
                st.markdown(result)
                st.download_button("テキストとしてダウンロード", result, file_name="titles.txt", mime="text/plain")
