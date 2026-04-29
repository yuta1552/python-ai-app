import google.generativeai as genai


def generate_sns_post(
    content: str,
    platform: str,
    tone: str,
    include_hashtags: bool,
    model: genai.GenerativeModel,
) -> str:
    platform_rules = {
        "X (Twitter)": "140字以内（日本語）に収める。簡潔でインパクトのある表現を使う。",
        "Instagram": "改行を活用して読みやすくする。絵文字を適度に使ってもよい。",
        "LinkedIn": "プロフェッショナルな内容で、ビジネス価値を伝える。200〜300字程度。",
        "Facebook": "読者が共有したくなるような内容にする。300字程度。",
        "note": "ブログ風の導入文として使えるような、読み応えのある内容にする。",
    }

    tone_map = {
        "カジュアル": "親しみやすくフレンドリーな口調で",
        "プロフェッショナル": "ビジネスライクでプロフェッショナルな文体で",
        "エモーショナル": "感情に訴えかける、共感を呼ぶ表現で",
        "ユーモア": "ユーモアを交えた楽しい表現で",
    }

    platform_rule = platform_rules.get(platform, "適切な長さで")
    tone_instruction = tone_map.get(tone, "読みやすい文体で")
    hashtag_instruction = "\n- 投稿に合ったハッシュタグを5〜8個追加してください" if include_hashtags else ""

    prompt = f"""以下の内容をもとに、{platform}用の投稿文を日本語で作成してください。

【投稿したい内容】
{content}

条件:
- プラットフォーム: {platform}（{platform_rule}）
- 文体: {tone_instruction}書いてください{hashtag_instruction}
- 読者が「いいね」や「シェア」したくなるような魅力的な投稿にしてください

投稿文案を3パターン作成してください。"""

    response = model.generate_content(prompt)
    return response.text
