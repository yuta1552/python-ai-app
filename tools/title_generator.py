import google.generativeai as genai


def generate_titles(
    content: str,
    purpose: str,
    count: int,
    model: genai.GenerativeModel,
) -> str:
    purpose_map = {
        "ブログ記事": "読者がクリックしたくなる、SEOも意識した",
        "メール件名": "受信者が開封したくなる、簡潔で内容が伝わる",
        "SNS投稿": "スクロールが止まる、インパクトのある",
        "プレゼン・資料": "聴衆の興味を引く、内容を的確に表す",
        "YouTube動画": "視聴者がクリックしたくなる、検索にも強い",
    }

    purpose_instruction = purpose_map.get(purpose, "魅力的な")

    prompt = f"""以下の内容に対して、{purpose}用のタイトルを{count}個作成してください。

【内容・テーマ】
{content}

条件:
- {purpose_instruction}タイトルにしてください
- 各タイトルは異なるアプローチ（数字を使う、疑問形、インパクト重視など）で作成してください
- 日本語で作成してください

出力形式:
番号付きリストでタイトルを列挙し、各タイトルに一行でそのポイント（なぜ効果的か）を添えてください。"""

    response = model.generate_content(prompt)
    return response.text
