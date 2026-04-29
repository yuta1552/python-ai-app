import google.generativeai as genai


def generate_blog_article(
    topic: str,
    keywords: str,
    style: str,
    length: str,
    model: genai.GenerativeModel,
) -> str:
    length_map = {"短め（500字程度）": 500, "標準（1000字程度）": 1000, "長め（2000字程度）": 2000}
    target_length = length_map.get(length, 1000)

    style_map = {
        "カジュアル": "読みやすくフレンドリーな口調で、親しみやすい表現を使って",
        "フォーマル": "丁寧でプロフェッショナルな文体で、敬語を適切に使って",
        "SEO重視": "SEOを意識し、見出しにキーワードを自然に含めながら",
    }
    style_instruction = style_map.get(style, "読みやすい文体で")

    keywords_instruction = f"キーワード「{keywords}」を自然な形で含めて、" if keywords.strip() else ""

    prompt = f"""以下の条件でブログ記事を日本語で執筆してください。

テーマ: {topic}
{keywords_instruction}
文体: {style_instruction}書いてください。
文字数: 約{target_length}字

構成:
- 魅力的なタイトル
- 導入文（読者の興味を引く）
- 本文（見出しを使って整理する）
- まとめ

読者が最後まで読みたくなるような、価値のある内容にしてください。"""

    response = model.generate_content(prompt)
    return response.text
