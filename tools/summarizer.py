import google.generativeai as genai


def summarize_text(
    text: str,
    format: str,
    length: str,
    model: genai.GenerativeModel,
) -> str:
    length_map = {
        "短め（3〜5行）": "3〜5行程度",
        "標準（10行程度）": "10行程度",
        "詳細（20行程度）": "20行程度",
    }
    target_length = length_map.get(length, "10行程度")

    if format == "箇条書き":
        format_instruction = "箇条書き（・）で重要なポイントをリストアップしてください"
    else:
        format_instruction = "自然な文章でまとめてください"

    prompt = f"""以下のテキストを日本語で要約してください。

【要約対象テキスト】
{text}

条件:
- {format_instruction}
- 長さ: {target_length}
- 重要な情報・キーポイントを漏らさず、読んでいない人にも内容が伝わるようにまとめてください"""

    response = model.generate_content(prompt)
    return response.text
