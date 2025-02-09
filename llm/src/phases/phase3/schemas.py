from typing import List, Optional, Dict
from pydantic import BaseModel, Field
import uuid

# ベース要素のスキーマ
class Accommodation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="一意のID")
    hotel_no: int = Field(..., description="ホテル番号")  # APIの "hotelNo"
    name: str = Field(..., description="ホテルの名前")  # APIの "hotelName"
    address: str = Field(..., description="ホテルの住所 (address1 と address2 の連結値)")
    thumbnail: str = Field(..., description="ホテルのサムネイル画像のURL")
    price: int = Field(..., description="ホテルの価格 (hotelMinCharge)")
    rating: float = Field(..., description="ホテルの基本評価（reviewAverage）")
    
    # 追加フィールド（スネークケースで定義）
    hotel_image_url: str = Field(..., description="ホテルの画像URL")  # hotelImageUrl
    hotel_information_url: str = Field(..., description="ホテル情報のURL")  # hotelInformationUrl
    hotel_thumbnail_url: str = Field(..., description="ホテルのサムネイル画像のURL（詳細画像）")  # hotelThumbnailUrl
    hotel_special: str = Field(..., description="ホテルの特別情報")  # hotelSpecial
    dp_plan_list_url: str = Field(..., description="DPプランリストURL")  # dpPlanListUrl
    plan_list_url: str = Field(..., description="プランリストURL")  # planListUrl
    review_average: float = Field(..., description="レビューの平均評価")  # reviewAverage
    room_image_url: Optional[str] = Field(None, description="客室画像のURL")  # roomImageUrl

    # 追加の詳細情報
    access: str = Field(..., description="ホテルへのアクセス情報")  # access
    postal_code: str = Field(..., description="郵便番号")  # postalCode
    telephone_no: str = Field(..., description="電話番号")  # telephoneNo
    fax_no: str = Field(..., description="FAX番号")  # faxNo
    hotel_kana: str = Field(..., description="ホテルのカナ表記")  # hotelKanaName
    hotel_map_image_url: str = Field(..., description="ホテルの地図画像URL")  # hotelMapImageUrl
    parking_information: str = Field(..., description="駐車場情報")  # parkingInformation
    review_count: int = Field(..., description="レビュー件数")  # reviewCount
    review_url: str = Field(..., description="レビューURL")  # reviewUrl
    user_review: str = Field(..., description="ユーザーレビュー")  # userReview
    
    # 緯度・経度などの位置情報（必要に応じて追加）
    latitude: Optional[float] = Field(None, description="緯度")
    longitude: Optional[float] = Field(None, description="経度")

    hotel_rating_info: Optional[Dict[str, float]] = Field(
        None, description="ホテルの詳細な評価情報 例: bathAverage, equipmentAverage, locationAverage, mealAverage, roomAverage, serviceAverage"
    )

class Spot(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="一意のID")
    name: str = Field(description="スポットの名前")
    address: str = Field(description="スポットの住所")
    opening_hours: List[str] = Field(description="スポットの開店時間")
    rating: float = Field(description="評価")
    related_url: str = Field(description="スポットの公式サイトのURL")
    thumbnail: str = Field(description="スポットのサムネイル画像のURL")
    description: str = Field(description="スポットの説明")

class Restaurant(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="一意のID")
    name: str = Field(description="レストランの名前")
    address: str = Field(description="レストランの住所")
    opening_hours: List[str] = Field(description="レストランの開店時間")
    rating: float = Field(description="評価")
    related_url: str = Field(description="レストランの公式サイトのURL")
    thumbnail: str = Field(description="レストランのサムネイル画像のURL")
    description: str = Field(description="レストランの説明")

# プラン関連のスキーマ
class DayPlan(BaseModel):
    """
    1日のプラン
    """
    id: str = Field(description="ランダムなID")
    day: int = Field(description="日付")
    accommodation: Accommodation = Field(..., description="宿泊施設")
    spots: List[Spot] = Field(default_factory=list, description="観光スポット, spotsは1日複数可能")
    lunch: List[Restaurant] = Field(default_factory=list, description="ランチ")
    dinner: List[Restaurant] = Field(default_factory=list, description="ディナー")

class Plan(BaseModel):
    """
    旅程をまとめた旅のプラン
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="一意のID")
    title: str = Field(description="プランのタイトル")
    dayPlans: List[DayPlan] = Field(default_factory=list, description="プラン内容をまとめたリスト, 日数分のプランを作成してください")

class PlansOutput(BaseModel):
    """
    複数のプランをまとめた出力
    """
    plans: Optional[Plan] = Field(..., description="プラン")
# タスク関連のスキーマ
class AreaCode(BaseModel):
    middle_class_code: str = Field(description="都道府県名 tokyo, osaka, etc.")
    small_class_code: str = Field(description="都道府県名 tokyo, osaka, etc.")
    detail_class_code: Optional[str] = Field(description="詳細エリア名, 例: 海が見える, 温泉, etc.")

class HotelSearch(BaseModel):
    area: AreaCode
    checkin: str
    checkout: str
    budget: int
    num_adults: int
    keyword: str

class RestaurantSearch(BaseModel):
    area: str
    meal_time: str
    budget: int
    cuisine_type: str
    num_people: int

class SpotSearch(BaseModel):
    area: str
    category: str
    estimated_hours: float

class SearchTask(BaseModel):
    hotel_search: List[HotelSearch]
    restaurant_searches: List[RestaurantSearch]
    spot_searches: List[SpotSearch]

class TaskList(BaseModel):
    tasks: List[SearchTask]

# ユーザー設定関連のスキーマ
class TravelPreferences(BaseModel):
    accommodation_type: str
    sightseeing_type: str
    pace: str
    budget: str
    duration: str
    num_people: str

# 実行計画関連のスキーマ
class ExecutionPlan(BaseModel):
    steps: List[str]
    reasoning: str

# 使用例：
"""
{
    "search_tasks": [
        {
            "category": "accommodation",
            "priority": 1,
            "conditions": {
                "keywords": ["温泉", "和室", "露天風呂"],
                "location": "箱根",
                "filters": {
                    "price_range": [20000, 40000],
                    "rating_min": 4.0
                }
            },
            "required_info": [
                "name",
                "price",
                "rating",
                "amenities",
                "room_types",
                "availability"
            ]
        },
        {
            "category": "restaurant",
            "priority": 2,
            "conditions": {
                "keywords": ["懐石料理", "個室"],
                "location": "箱根",
                "filters": {
                    "price_range": [10000, 20000],
                    "has_private_room": true
                }
            },
            "required_info": [
                "name",
                "price_range",
                "menu_highlights",
                "opening_hours",
                "reservation_availability"
            ]
        }
    ],
    "reasoning": "宿泊施設の検索を最優先に設定し、その後で周辺の飲食店を探すことで、効率的な旅程作成が可能になります。",
    "dependencies": {
        "restaurant": ["accommodation"],
        "spot": ["accommodation"]
    }
}
""" 