import google.generativeai as genai


def proofread_text(
    text: str,
    focus: list[str],
    model: genai.GenerativeModel,
) -> str:
    focus_map = {
        "誤字・脱字": "誤字・脱字・誤変換",
        "文法・表現": "文法的な誤りや不自然な表現",
        "文体の統一": "文体（です・ます調 / だ・である調）の統一",
        "読みやすさ": "文章の読みやすさ・流れの改善",
    }

    focus_items = [focus_map[f] for f in focus if f in focus_map]
    focus_instruction = "、".join(focus_items) if focus_items else "全般的な品質"

    prompt = f"""以下の文章を校正・改善してください。

【校正対象テキスト】
{text}

チェック項目: {focus_instruction}

出力形式:
1. **校正済みテキスト**（修正後の完全な文章）
2. **修正箇所の説明**（何をどう修正したか、箇条書きで）
3. **改善アドバイス**（さらに良くするための提案があれば）"""

    response = model.generate_content(prompt)
    return response.text
