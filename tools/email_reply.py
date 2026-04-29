import google.generativeai as genai


def generate_email_reply(
    received_email: str,
    reply_points: str,
    tone: str,
    model: genai.GenerativeModel,
) -> str:
    tone_map = {
        "丁寧・ビジネス": "丁寧なビジネスメールの文体で、敬語を正しく使って",
        "カジュアル": "親しみやすいカジュアルな文体で",
        "簡潔": "要点だけを短くまとめた、簡潔な文体で",
    }
    tone_instruction = tone_map.get(tone, "丁寧な文体で")

    points_instruction = f"\n返信で伝えたい要点:\n{reply_points}" if reply_points.strip() else ""

    prompt = f"""以下のメールへの返信文を日本語で作成してください。

【受信したメール】
{received_email}
{points_instruction}

条件:
- {tone_instruction}書いてください
- 件名（Re:〜）も含めてください
- 宛名・署名の部分は「[宛名]」「[署名]」のようにプレースホルダーで示してください
- 自然で読みやすい返信文にしてください"""

    response = model.generate_content(prompt)
    return response.text
