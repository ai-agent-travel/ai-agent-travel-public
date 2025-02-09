# tests/test_api.py

import unittest
import requests
import json
import uuid
from dotenv import load_dotenv
import os
load_dotenv()

class TestPhase1Flow(unittest.TestCase):
    BASE_URL = os.getenv("PROJECT_BACKEND_URL", "http://localhost:8083") # Flaskアプリが動いているURL

    def test_multi_turn_conversation(self):
        """マルチターン会話のテスト"""
        # 初回リクエスト
        initial_payload = {
            "current_phase": "phase1",
            "form_info": {
                "place": "北海道",
                "startDate": "2024/12/19",
                "endDate": "2024/12/21",
                "accomodationBudget": "10000円",
                "people": "2"
            }
        }
        
        print("\n=== 初回リクエスト ===")
        print("Payload:", json.dumps(initial_payload, indent=2, ensure_ascii=False))
        
        resp = requests.post(f"{self.BASE_URL}/agent", json=initial_payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        
        print("\n=== 初回レスポンス ===")
        print("Status Code:", resp.status_code)
        print("Messages:", json.dumps(data.get("messages", []), indent=2, ensure_ascii=False))
        print("Form Info:", json.dumps(data.get("form_info", {}), indent=2, ensure_ascii=False))
        print("Interrupt:", data.get("interrupt"))
        
        # 中断が返ってきた場合のループ処理
        thread_id = data.get("thread_id")
        max_turns = 10  # 最大ターン数
        turn = 0
        
        while turn < max_turns:
            print(f"\n=== ターン {turn + 1} ===")
            print("Current Messages:", json.dumps(data.get("messages", []), indent=2, ensure_ascii=False))
            
            if data.get("interrupt"):
                last_message = data.get("messages", [])[-1] if data.get("messages") else {"content": "No message"}
                print("\nAI応答:", last_message.get("content", ""))
                print("Message Details:", json.dumps(last_message, indent=2, ensure_ascii=False))
                
                # ユーザーからの入力を受け取る
                user_input = input("\nあなたの回答を入力してください: ")
                
                # 中断の場合、ユーザーの回答を送信
                next_payload = {
                    "thread_id": thread_id,
                    "user_message": user_input,
                    "current_phase": "phase1",
                    "form_info": data.get("form_info", {})
                }
                
                print("\n=== リクエスト ===")
                print("Payload:", json.dumps(next_payload, indent=2, ensure_ascii=False))
                
                resp = requests.post(f"{self.BASE_URL}/agent", json=next_payload)
                self.assertEqual(resp.status_code, 200)
                data = resp.json()
                
                print("\n=== レスポンス ===")
                print("Status Code:", resp.status_code)
                print("Messages:", json.dumps(data.get("messages", []), indent=2, ensure_ascii=False))
                print("Form Info:", json.dumps(data.get("form_info", {}), indent=2, ensure_ascii=False))
                print("Interrupt:", data.get("interrupt"))
                
                turn += 1
            else:
                # 正常終了
                print("\n=== 会話が完了しました ===")
                print("Final Messages:", json.dumps(data.get("messages", []), indent=2, ensure_ascii=False))
                print("Final Form Info:", json.dumps(data.get("form_info", {}), indent=2, ensure_ascii=False))
                print("Final State:", json.dumps(data, indent=2, ensure_ascii=False))
                break
        
        # 最大ターン数に達していないことを確認
        self.assertLess(turn, max_turns, "会話が最大ターン数を超えました")
        print("\n=== テスト終了 ===")

if __name__ == "__main__":
    unittest.main()
