import requests
import json
import time
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

current_path = Path(__file__).parent
parent_path = current_path.parent.parent.parent

RAKUTEN_URL = "https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426"
RAKUTEN_APPLICATION_ID = os.getenv("RAKUTEN_APPLICATION_ID")
RAKUTEN_CODES_PATH = parent_path / "src/rakuten_codes.json"
logger.info(RAKUTEN_CODES_PATH)

def fetch_codes():
    """
    楽天のエリアクラスを json で取得する
    """
    CODES_URL = "https://app.rakuten.co.jp/services/api/Travel/GetAreaClass/20131024?"
    CODES_PARAMS = {
        "format": "json",
        "applicationId": RAKUTEN_APPLICATION_ID,
    }
    response = requests.get(CODES_URL, params=CODES_PARAMS)
    return response.json()


def load_middle_classes() -> list:
    with open(RAKUTEN_CODES_PATH, "r") as f:
        return json.load(f)["areaClasses"]["largeClasses"][0]["largeClass"][1]["middleClasses"]

    
def get_subclasses_by_middle_class(middle_class_code: str) -> dict:
    """
    input:
        middle_class_code: 都道府県レベルのコード
    output:
        small_class_info: 小エリアレベルのコードと名前
        各市町村のコードと名前、(存在すれば)詳細エリア情報を含んだ item のリスト
    """
    # middleClassを検索
    for item in load_middle_classes():
        middle_class_info = item['middleClass'][0]
        if middle_class_info['middleClassCode'] == middle_class_code:
            result = {
                'middleClass': {
                    'code': middle_class_info['middleClassCode'],
                    'name': middle_class_info['middleClassName']
                },
                'smallClasses': []
            }
            
            # smallClassesの処理
            small_classes = item['middleClass'][1]['smallClasses']
            for small_class_group in small_classes:
                for small_class in small_class_group['smallClass']:
                    if "smallClassName" in small_class:
                        small_class_info = {
                            'smallClassCode': small_class['smallClassCode'],
                            'smallClassName': small_class['smallClassName'],
                            'detailClasses': []
                        }
                    
                    # detailClassesが存在する場合の処理
                    if 'detailClasses' in small_class:
                        for detail_class_group in small_class['detailClasses']:
                            detail_class = detail_class_group['detailClass']
                            small_class_info['detailClasses'].append({
                                'detailClassCode': detail_class['detailClassCode'],
                                'detailClassName': detail_class['detailClassName']
                            })
                    
                    result['smallClasses'].append(small_class_info)
            
            return result
    
    return None


def fetch_hotels_by_class_code(
        middle_class_code: str,
        small_class_code: str | None=None,
        detail_class_code: str | None=None,
        checkin: str="2025-04-01",
        checkout: str="2025-04-02",
        num_adult: int=2,
        max_charge: int=10000,
        hits: int=2,
        keyword: str | None="温泉",
    ) -> list[dict]:
    RAKUTEN_PARAMS = {
        "format": "json",
        "largeClassCode": "japan",
        "middleClassCode": middle_class_code,
        "smallClassCode": small_class_code,
        "checkinDate": checkin,
        "checkoutDate": checkout,
        "adultNum": num_adult,
        "maxCharge": max_charge,
        "hits": hits,
        "keyword": keyword,
        "applicationId": RAKUTEN_APPLICATION_ID,
    }
    responses = []
    
    # smallClassCode も detailClassCode も指定されている場合
    # 県 + 市 + detail エリアの指定
    if small_class_code is not None and detail_class_code is not None:
        RAKUTEN_PARAMS["smallClassCode"] = small_class_code
        RAKUTEN_PARAMS["detailClassCode"] = detail_class_code
        response = requests.get(RAKUTEN_URL, params=RAKUTEN_PARAMS)
        responses.append(response.json())
        return responses
    
    # smallClassCode のみ指定されている場合 (detailClassCode が下位クラスとして存在するかを確認)
    # 県 + 市の指定
    # CAUTION: detailClassの分だけ検索結果が増える
    elif small_class_code is not None:
        RAKUTEN_PARAMS["smallClassCode"] = small_class_code
        small_classes = get_subclasses_by_middle_class(middle_class_code)["smallClasses"]
        for small_class in small_classes:
            if small_class["smallClassCode"] == small_class_code:
                # detailClassCode が存在する場合
                if small_class["detailClasses"]:
                    detail_classes = small_class["detailClasses"]
                    for detail_class in detail_classes:
                        RAKUTEN_PARAMS["detailClassCode"] = detail_class["detailClassCode"]
                        response = requests.get(RAKUTEN_URL, params=RAKUTEN_PARAMS)
                        responses.append(response.json())
                        time.sleep(0.5)
                # detailClassCode が存在しない場合
                else:
                    if "detailClassCode" in RAKUTEN_PARAMS:
                        RAKUTEN_PARAMS.pop("detailClassCode")
                    response = requests.get(RAKUTEN_URL, params=RAKUTEN_PARAMS)
                    responses.append(response.json())
                
                return responses
    
    # smallClassCode も detailClassCode も指定されていない場合
    # 県のみの指定
    # CAUTION: smallClass, detailClassの分だけ検索結果が増える
    small_classes = get_subclasses_by_middle_class(middle_class_code)
    print("SMALL SEARCH")
    for small_class in small_classes["smallClasses"]:
        RAKUTEN_PARAMS["smallClassCode"] = small_class["smallClassCode"]
        if small_class["detailClasses"]:
            detail_classes = small_class["detailClasses"]
            for detail_class in detail_classes:
                RAKUTEN_PARAMS["detailClassCode"] = detail_class["detailClassCode"]
                response = requests.get(RAKUTEN_URL, params=RAKUTEN_PARAMS)
                responses.append(response.json())
                time.sleep(0.5)
        else:
            if "detailClassCode" in RAKUTEN_PARAMS:
                RAKUTEN_PARAMS.pop("detailClassCode")
            response = requests.get(RAKUTEN_URL, params=RAKUTEN_PARAMS)
            responses.append(response.json())
            time.sleep(0.5)

    return response.json()



# EXAMPLE OF USAGE
def main():
    # 群馬の場合のサブクラスを取得
    # subclasses = get_subclasses_by_middle_class("gunma")
    # print("\n\nSubclasses of Gunma")
    # pprint(subclasses)
    
    
    # 地域コードを指定して、空き部屋を検索
    middle_class_code = "miyagi"
    small_class_code = "matsushima"
    checkin = "2025-02-19"
    checkout = "2025-02-20"
    num_adult = 1
    max_charge = 10000
    hits = 1
    keyword = "seaside"
# {'area': {'middle_class_code': 'miyagi', 'small_class_code': 'matsushima', 'detail_class_code': 'seaside'}, 'checkin': '2025-02-19', 'checkout': '2025-02-20', 'budget': 10000, 'num_adults': 2, 'keyword': 'seaside'}

    
    hotels = fetch_hotels_by_class_code(middle_class_code=middle_class_code,
                                        small_class_code=small_class_code,
                                        checkin=checkin,
                                        checkout=checkout,
                                        num_adult=num_adult,
                                        max_charge=max_charge,
                                        hits=hits,
                                        keyword=keyword)
    # print(f"\n\nHotels in {middle_class_code} {small_class_code}")
    for hotel in hotels:
        basic_info = hotel["hotels"][0]["hotel"][0]["hotelBasicInfo"]
        print("型:", type(basic_info))
        print("内容:", basic_info, "\n\n")
    
    # 荒い検索ができているか
    # middle_class_code = "gunma"
    # small_class_code = None
    # detail_class_code = None
    # hotels = fetch_hotels_by_class_code(middle_class_code=middle_class_code,
    #                                     small_class_code=small_class_code,
    #                                     detail_class_code=detail_class_code,
    #                                     checkin=checkin,
    #                                     checkout=checkout,
    #                                     num_adult=num_adult,
    #                                     max_charge=max_charge,
    #                                     keyword=keyword)
    # print(f"\n\nROUGH SEARCH: Hotels in {middle_class_code} {small_class_code} {detail_class_code}")
    # pprint(hotels)


if __name__ == "__main__":
    main()
