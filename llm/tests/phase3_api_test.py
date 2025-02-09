import requests
import json
import unittest
import os
from dotenv import load_dotenv
load_dotenv()

class TestPhase3Flow(unittest.TestCase):
    # Flaskアプリが動いているURLを指定
    BASE_URL = os.getenv("PROJECT_BACKEND_URL", "http://localhost:8083") # Flaskアプリが動いているURL


    def test_phase3_flow(self):
        """
        phase3（プラン修正）のテスト
        ・既存のプラン、ヒアリング結果、ユーザFBK、チーム計画が状態に含まれている状態をシミュレーション
        ・phase3の処理では、ユーザFBKや既存プランを基に、修正版のプランを生成することが求められる
        """
        payload = {
            "current_phase": "phase3",
            "form_info": {
                "place": "沖縄",
                "startDate": "2025/04/01",
                "endDate": "2025/04/03",
                "accomodationBudget": "8000円",
                "people": "2"
            },
            # messages内には、ヒアリング結果（user_summary）、
            # ユーザFBKのサマリー（user_fbk_summary）、
            # チームの計画（team_planning）を含む
            "messages": [
                {
                    "role": "assistant",
                    "content": "ヒアリング結果: 静かで落ち着いたホテルを希望。観光は歴史的なスポットが良い。",
                    "type": "user_summary"
                },
                {
                    "role": "assistant",
                    "content": "FBKサマリー: 予算内で、もっとアクセスの良いホテルを希望。観光スポットは充実させること。",
                    "type": "user_fbk_summary"
                },
                {
                    "role": "assistant",
                    "content": "チームの計画: プラン修正により、1日目と2日目を重点に、最終日は宿泊無しにする。",
                    "type": "team_planning"
                },
                {
                    "role": "assistant",
                    "content": "チームの計画: プラン修正により、1日目と2日目を重点に、最終日は宿泊無しにする。",
                    "type": "team_planning"
                }
            ],
            # ユーザからの詳細なFBK
            "user_fbk": "沖縄ではないところがある。沖縄県のスポット、ご飯場所にして。美ら海も行きたい",
            # 以前提供したプラン（phase2で生成されたものを想定）
            "plans": [
                {
                    "dayPlans": [
                        {
                            "accommodation": {
                                "access": "ニライカナイ橋から車で10分",
                                "address": "沖縄県南城市玉城前川",
                                "dp_plan_list_url": "",
                                "fax_no": "098-123-4568",
                                "hotel_image_url": "",
                                "hotel_information_url": "",
                                "hotel_kana": "ビジネスホテルオキナワナンブ",
                                "hotel_map_image_url": "",
                                "hotel_no": 1,
                                "hotel_rating_info": None,
                                "hotel_special": "無料Wi-Fi、朝食付き",
                                "hotel_thumbnail_url": "",
                                "id": "hotel1",
                                "latitude": 26.123456,
                                "longitude": 127.123456,
                                "name": "ビジネスホテル沖縄南部",
                                "parking_information": "無料駐車場あり",
                                "plan_list_url": "",
                                "postal_code": "901-1400",
                                "price": 8000,
                                "rating": 4,
                                "review_average": 4,
                                "review_count": 100,
                                "review_url": "",
                                "room_image_url": None,
                                "telephone_no": "098-123-4567",
                                "thumbnail": "",
                                "user_review": "清潔で快適なビジネスホテルです。"
                            },
                            "day": 1,
                            "dinner": [
                                {
                                    "address": "東京都港区麻布台３丁目３−１９",
                                    "description": "沖縄料理を堪能できる人気店。",
                                    "id": "restaurant2",
                                    "name": "沖縄料理 MAMI-ANA 麻布十番",
                                    "opening_hours": [
                                        "18:00-0:00"
                                    ],
                                    "rating": 4.5,
                                    "related_url": "https://mamiana-okinawa.com/",
                                    "thumbnail": ""
                                }
                            ],
                            "id": "day1",
                            "lunch": [
                                {
                                    "address": "埼玉県さいたま市中央区大戸２丁目２３−６",
                                    "description": "本格的な沖縄料理を楽しめるレストラン。",
                                    "id": "restaurant1",
                                    "name": "沖縄料理なわげん",
                                    "opening_hours": [
                                        "12:00-14:00",
                                        "17:00-23:00"
                                    ],
                                    "rating": 4.2,
                                    "related_url": "https://maps.google.com/?cid=2551176633669738286",
                                    "thumbnail": ""
                                }
                            ],
                            "spots": [
                                {
                                    "address": "沖縄県南城市玉城前川",
                                    "description": "美しい景色が広がる橋。",
                                    "id": "spot1",
                                    "name": "ニライカナイ橋",
                                    "opening_hours": [
                                        "24時間"
                                    ],
                                    "rating": 4.5,
                                    "related_url": "",
                                    "thumbnail": ""
                                }
                            ]
                        },
                        {
                            "accommodation": {
                                "access": "ニライカナイ橋から車で10分",
                                "address": "沖縄県南城市玉城前川",
                                "dp_plan_list_url": "",
                                "fax_no": "098-123-4568",
                                "hotel_image_url": "",
                                "hotel_information_url": "",
                                "hotel_kana": "ビジネスホテルオキナワナンブ",
                                "hotel_map_image_url": "",
                                "hotel_no": 2,
                                "hotel_rating_info": None,
                                "hotel_special": "無料Wi-Fi、朝食付き",
                                "hotel_thumbnail_url": "",
                                "id": "hotel2",
                                "latitude": 26.123456,
                                "longitude": 127.123456,
                                "name": "ビジネスホテル沖縄南部",
                                "parking_information": "無料駐車場あり",
                                "plan_list_url": "",
                                "postal_code": "901-1400",
                                "price": 8000,
                                "rating": 4,
                                "review_average": 4,
                                "review_count": 100,
                                "review_url": "",
                                "room_image_url": None,
                                "telephone_no": "098-123-4567",
                                "thumbnail": "",
                                "user_review": "清潔で快適なビジネスホテルです。"
                            },
                            "day": 2,
                            "dinner": [
                                {
                                    "address": "埼玉県富士見市上南畑５３６−１",
                                    "description": "沖縄の伝統料理を提供するレストラン。",
                                    "id": "restaurant4",
                                    "name": "沖縄料理家 屋いち 埼玉本舗",
                                    "opening_hours": [
                                        "11:30-14:00",
                                        "17:00-21:00"
                                    ],
                                    "rating": 3.9,
                                    "related_url": "https://maps.google.com/?cid=13867528783375801586",
                                    "thumbnail": ""
                                }
                            ],
                            "id": "day2",
                            "lunch": [
                                {
                                    "address": "埼玉県新座市東北２丁目３２−３ コープ野村志木 １０１",
                                    "description": "沖縄の家庭料理を楽しめるお店。",
                                    "id": "restaurant3",
                                    "name": "島想い",
                                    "opening_hours": [
                                        "11:30-13:45",
                                        "17:00-22:30"
                                    ],
                                    "rating": 4,
                                    "related_url": "https://shimaomoi.gorp.jp/",
                                    "thumbnail": ""
                                }
                            ],
                            "spots": [
                                {
                                    "address": "沖縄県南城市玉城前川２０２",
                                    "description": "自然豊かな谷でリラックス。",
                                    "id": "spot2",
                                    "name": "ガンガラーの谷",
                                    "opening_hours": [
                                        "9:00-18:00"
                                    ],
                                    "rating": 4.4,
                                    "related_url": "https://gangala.com/?utm_source=googlemybusiness",
                                    "thumbnail": ""
                                }
                            ]
                        },
                        {
                            "accommodation": {
                                "access": "",
                                "address": "",
                                "dp_plan_list_url": "",
                                "fax_no": "",
                                "hotel_image_url": "",
                                "hotel_information_url": "",
                                "hotel_kana": "",
                                "hotel_map_image_url": "",
                                "hotel_no": 0,
                                "hotel_rating_info": None,
                                "hotel_special": "",
                                "hotel_thumbnail_url": "",
                                "id": "",
                                "latitude": None,
                                "longitude": None,
                                "name": "",
                                "parking_information": "",
                                "plan_list_url": "",
                                "postal_code": "",
                                "price": 0,
                                "rating": 0,
                                "review_average": 0,
                                "review_count": 0,
                                "review_url": "",
                                "room_image_url": None,
                                "telephone_no": "",
                                "thumbnail": "",
                                "user_review": ""
                            },
                            "day": 3,
                            "dinner": [],
                            "id": "day3",
                            "lunch": [
                                {
                                    "address": "埼玉県さいたま市中央区大戸２丁目２３−６",
                                    "description": "本格的な沖縄料理を楽しめるレストラン。",
                                    "id": "restaurant5",
                                    "name": "沖縄料理なわげん",
                                    "opening_hours": [
                                        "12:00-14:00",
                                        "17:00-23:00"
                                    ],
                                    "rating": 4.2,
                                    "related_url": "https://maps.google.com/?cid=2551176633669738286",
                                    "thumbnail": ""
                                }
                            ],
                            "spots": [
                                {
                                    "address": "沖縄県うるま市石川嘉手苅４７９−１",
                                    "description": "神秘的な鍾乳洞を探検。",
                                    "id": "spot3",
                                    "name": "CAVE OKINAWA【鍾乳洞】",
                                    "opening_hours": [
                                        "9:00-17:00"
                                    ],
                                    "rating": 4.3,
                                    "related_url": "https://www.cave.okinawa/",
                                    "thumbnail": ""
                                }
                            ]
                        }
                    ],
                    "id": "trip-okinawa-2025",
                    "title": "沖縄県南部でのゆったり旅行プラン"
                }
            ],
            "thread_id": "test-thread-phase3"
        }

        print("\n=== Phase3テスト リクエスト ===")
        print("Payload:", json.dumps(payload, indent=2, ensure_ascii=False))
        
        # /agent エンドポイントにPOSTリクエストを送信
        resp = requests.post(f"{self.BASE_URL}/agent", json=payload)
        self.assertEqual(resp.status_code, 200)

        data = resp.json()
        print("\n=== Phase3テスト レスポンス ===")
        print("Status Code:", resp.status_code)
        print("Messages:", json.dumps(data.get("messages", []), indent=2, ensure_ascii=False))
        print("Form Info:", json.dumps(data.get("form_info", {}), indent=2, ensure_ascii=False))
        print("Plans:", json.dumps(data.get("plans", []), indent=2, ensure_ascii=False))
        print("Interrupt:", data.get("interrupt", False))
        
        # 生成された新しいプランが保存されていることを検証
        self.assertIn("plans", data)
        self.assertGreater(len(data.get("plans", [])), 0, "新しいプランが生成されていません")

if __name__ == "__main__":
    unittest.main() 