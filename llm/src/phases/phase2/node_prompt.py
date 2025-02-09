def create_planning_prompt(form_info: dict, phase1_messages: list) -> str:
    """プランニング用のプロンプトを生成"""
    return f"""
    あなたは旅行プランナーです。
    以下の情報から旅行の好みを分析し、必ず指定されたJSON形式で出力してください。
    マークダウンの装飾（```json等）は不要です。JSONのみを出力してください。

    出力形式：
    {{
        "accommodation": {{
            "type": "宿泊施設のタイプ",
            "style": "宿泊施設のスタイル",
            "must_have": ["必須の設備1", "必須の設備2"]
        }},
        "sightseeing": {{
            "style": "観光スタイル",
            "pace": "観光のペース",
            "interests": ["興味1", "興味2"]
        }},
        "dining": {{
            "style": "食事のスタイル",
            "cuisine_types": ["料理ジャンル1", "料理ジャンル2"],
            "price_level": "予算レベル"
        }}
    }}

    フォーム情報：
    {form_info}

    会話履歴：
    {phase1_messages}
    """

def create_task_prompt(preferences: dict) -> str:
    """タスク生成用のプロンプトを生成"""
    return [
        {
            "role": "system",
            "content": """
            あなたは旅行プランナーです。
            与えられた好みに基づいて、具体的な検索タスクを生成してください。
            各タスクには検索条件と優先度を含めてください。

            出力形式：
            {
                "accommodation_tasks": [
                    {
                        "type": "検索タイプ",
                        "conditions": {"条件キー": "条件値"},
                        "priority": 1-5
                    }
                ],
                "sightseeing_tasks": [
                    {
                        "type": "検索タイプ",
                        "conditions": {"条件キー": "条件値"},
                        "priority": 1-5
                    }
                ],
                "dining_tasks": [
                    {
                        "type": "検索タイプ",
                        "conditions": {"条件キー": "条件値"},
                        "priority": 1-5
                    }
                ]
            }
            """
        },
        {
            "role": "user",
            "content": f"以下の好みに基づいて検索タスクを生成してください：\n{preferences}"
        }
    ]