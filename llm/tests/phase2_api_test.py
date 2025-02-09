import requests
import json
import unittest
import os
from dotenv import load_dotenv
load_dotenv()

class TestPhase2Flow(unittest.TestCase):
    BASE_URL = os.getenv("PROJECT_BACKEND_URL", "http://localhost:8083") # Flaskアプリが動いているURL

    def test_phase2_flow(self):
        """フェーズ2のテスト"""
        ## フェーズ1のレスポンスデータ
        # response_parameters = {
        #     "form_info": {
        #         "place": "北海道",
        #         "startDate": "2025/2/19",
        #         "endDate": "2025/2/21",
        #         "accomodationBudget": "10000円",
        #         "people": "2"
        #     },
        #     "current_phase": "phase2",
        #     "thread_id": "生成されたthread_id",
        #     "messages": [
        #         {
        #         "content": "北海道旅行、楽しみですね！😊 2泊されるんですね。宿泊はホテルと旅館、どちらがお好みですか？✨ \n",
        #         "order": 1,
        #         "role": "assistant",
        #         "selector": [
        #             "",
        #             ""
        #         ]
        #         },
        #         {
        #         "content": "ホテル",
        #         "order": 2,
        #         "role": "human"
        #         },
        #         {
        #         "content": "なるほど、ホテル派ですね！🏢✨  どんな雰囲気のホテルがお好きですか？ 例えば、モダン、ラグジュアリー、それともアットホームな感じ？ 😊 \n",
        #         "order": 3,
        #         "role": "assistant",
        #         "selector": [
        #             "",
        #             ""
        #         ]
        #         },
        #         {
        #         "content": "モダン",
        #         "order": 4,
        #         "role": "human"
        #         },
        #         {
        #         "content": "いいですね！モダンなホテルで過ごす北海道、素敵ですね！✨  観光は、人気の定番スポットを巡りたい気分ですか？ それとも、何かテーマを決めて旅したい気分ですか？ 😊 \n",
        #         "order": 5,
        #         "role": "assistant",
        #         "selector": [
        #             "",
        #             ""
        #         ]
        #         },
        #         {
        #         "content": "定番スポット",
        #         "order": 6,
        #         "role": "human"
        #         },
        #         {
        #         "content": "AI: 定番スポット巡り、いいですね！✨  北海道には美味しいものがたくさんありますが、特に何か食べたいものはありますか？ 😊  \n",
        #         "order": 7,
        #         "role": "assistant",
        #         "selector": [
        #             "",
        #             ""
        #         ]
        #         },
        #         {
        #         "content": "おすすめで",
        #         "order": 8,
        #         "role": "human"
        #         },
        #         {
        #         "content": "AI: 北海道の定番グルメ、堪能しちゃいましょう！😊  2日間で、どんな風に過ごしたい気分ですか？ アクティブに動く？ ゆったり過ごす？  \n",
        #         "order": 9,
        #         "role": "assistant",
        #         "selector": [
        #             "",
        #             ""
        #         ]
        #         },
        #         {
        #         "content": "のんびり",
        #         "order": 10,
        #         "role": "human"
        #         },
        #         {
        #         "content": "これで必要な情報が揃いました 😊 \n",
        #         "order": 11,
        #         "role": "assistant",
        #         "selector": [
        #             "",
        #             ""
        #         ]
        #         }
        #     ],
        #     "user_input_message": "",
        #     "plans": [],
        #     "interrupt": False
        # }

        response_parameters = {
            "form_info": {
                "place": "宮城県",
                "startDate": "2025/2/19",
                "endDate": "2025/2/21",
                "accomodationBudget": "10000円",
                "people": "2"
            },
            "current_phase": "phase2",
            "thread_id": "",
            "messages": [
                {'content': 'わくわくしますね！宮城県には素敵な観光地がたくさんありますよね。どんな旅にしたい気分ですか？😊 \n', 'order': 1, 'role': 'assistant', 'selector': ['', '']}, {'content': 'グルメ', 'order': 2, 'role': 'human'}, {'content': ' なるほど！食がテーマの旅ですね！😋 具体的に何か食べたいものはありますか？🍲🍣  \n', 'order': 3, 'role': 'assistant', 'selector': ['', '']}, {'content': '魚', 'order': 4, 'role': 'human'}, {'content': '魚料理ですか！いいですね〜！宮城は新鮮な魚介類が有名ですよね。 🐟 \n具体的にどんな魚料理がお好きですか？ 例えば、お寿司、海鮮丼、それともお刺身定食など…？ 😊 \n', 'order': 5, 'role': 'assistant', 'selector': ['', '']}, {'content': '寿司', 'order': 6, 'role': 'human'}, {'content': 'お寿司！いいですね！🍣✨ \n宮城はおいしいお寿司屋さんがたくさんありますよ！ \nちなみに、お寿司以外に食べてみたいものはありますか？😋 \n', 'order': 7, 'role': 'assistant', 'selector': ['', '']}, {'content': '海鮮丼', 'order': 8, 'role': 'human'}, {'content': '海鮮丼も食べたいんですね！🍣🍚  \n宿泊場所ですが、海の近くがいいですか？それとも仙台市内などが良いですか？ 😊 \n', 'order': 9, 'role': 'assistant', 'selector': ['', '']}, {'content': '海', 'order': 10, 'role': 'human'}, {'content': 'これで必要な情報が揃いました \n', 'order': 11, 'role': 'assistant', 'selector': ['', '']}
            ],
            "user_input_message": "",
            "plans": [],
            "interrupt": False
        }

        ## フェーズ2のリクエストデータ
        requests_data = response_parameters

        ## フェーズ2のリクエスト
        resp = requests.post(f"{self.BASE_URL}/agent", json=requests_data)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        print("\n=== フェーズ2のレスポンス ===")
        print("Status Code:", resp.status_code)
        print("data:", json.dumps(data, indent=2, ensure_ascii=False))
        print("plans:", json.dumps(data.get("plans", []), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    unittest.main()
