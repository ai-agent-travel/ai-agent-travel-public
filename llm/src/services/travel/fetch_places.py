import googlemaps
import time
import re
import os
import numpy as np
from scipy import stats
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

# APIキーを設定
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
GMAPS_CLIENT = googlemaps.Client(key=API_KEY)

def get_place_details(place_id):
    """指定されたplace_idの詳細情報を取得する関数"""
    fields = ['name', 'formatted_address', 'formatted_phone_number', 'rating', 'user_ratings_total', 'opening_hours', 'website', 'url']
    place_details = GMAPS_CLIENT.place(place_id=place_id, fields=fields, language='ja')
    return place_details.get('result')

def clean_address(address):
    """住所から「日本」および郵便番号を削除する関数"""
    address = re.sub(r'日本、', '', address)
    address = re.sub(r'〒\d{3}-\d{4}', '', address)
    return address.strip()

def wilson_score(positive, n, confidence=0.95):
    if n == 0:
        return 0
    
    z = stats.norm.ppf(1 - (1 - confidence) / 2)  # 両側信頼区間のz値
    phat = float(positive) / n  # 肯定的な評価の割合
    
    # ウィルソンスコアの計算式
    denominator = 1 + z * z / n
    centre_adjusted_probability = phat + z * z / (2 * n)
    adjusted_standard_deviation = z * np.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)
    
    # 信頼区間の下限を返す
    return (centre_adjusted_probability - adjusted_standard_deviation) / denominator

# 使用例
def calculate_wilson_score_for_rating(rating, review_count, max_rating=5):
    # 評価を0-1のスケールに変換
    if rating is None or review_count == 0:
        return 0
    positive = (rating / max_rating) * review_count
    return wilson_score(positive, review_count)


def search_places(query, max_places=1) -> list[dict]:
    """指定されたクエリで店舗を検索し、各店舗の詳細情報を取得する関数"""
    places_details = []
    next_page_token = None  # 次のページがあれば、そのトークンを格納する変数
    place_count = 0
    while place_count < max_places:
        if next_page_token:
            places_result = GMAPS_CLIENT.places(query=query, page_token=next_page_token)
        else:
            places_result = GMAPS_CLIENT.places(query=query)

        for place in places_result.get('results', []):
            if place_count > max_places:
                break
            place_id = place['place_id']
            details = get_place_details(place_id)
            if details.get('formatted_phone_number'):
                user_ratings_total = details.get('user_ratings_total', 0)
                # if 10 <= user_ratings_total <= 49:  # 口コミ数が10以上49以下の場合
                opening_hours = details.get('opening_hours', {}).get('weekday_text', '営業時間情報なし')
                places_details.append({
                    'name': details.get('name'),
                    'address': clean_address(details.get('formatted_address', '')),
                    'phone_number': details.get('formatted_phone_number'),
                    'rating': details.get('rating'),
                    'user_ratings_total': user_ratings_total,
                    'wilson_score': calculate_wilson_score_for_rating(details.get('rating'), user_ratings_total),
                    'opening_hours': '\n'.join(opening_hours) if isinstance(opening_hours, list) else opening_hours,
                    'search_query': query,
                    'related_url': details.get('website') or details.get('url')
                })
            place_count += 1

        next_page_token = places_result.get('next_page_token')
        if not next_page_token:
            break
        time.sleep(0.2)
        
    sorted_by_wilson_score = sorted(places_details, key=lambda x: x['wilson_score'], reverse=True)

    return sorted_by_wilson_score

# EXAMPLE OF USAGE
def main():
    # 結構簡単に API RATE RIMIT ERROR になるので多用できなそう
    all_places = []
    queries = ["群馬 観光地"]
    for query in queries:
        places = search_places(query, max_places=5)
        all_places.extend(places)
    
    pprint(all_places)

if __name__ == "__main__":
    main()
