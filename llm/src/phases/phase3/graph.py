from langgraph.graph import StateGraph, START, END
from core.state import AgentState
from typing import Literal, List, Dict
from langgraph.types import Command
from phases.phase3.node_prompt import create_planning_prompt, create_task_prompt
from services.llm import llm_service, LLMService
import logging
from phases.phase3.schemas import TravelPreferences, TaskList, ExecutionPlan, PlansOutput, PlansOutput
from langchain_google_vertexai import create_structured_runnable
from langchain_core.prompts import ChatPromptTemplate
import json
from datetime import datetime, timedelta
import uuid
import time
from services.travel.fetch_hotels import fetch_hotels_by_class_code
from services.travel.fetch_places import search_places

logger = logging.getLogger(__name__)

def find_user_summary_message(messages: list[dict]) -> dict | None:
    """
    messages リスト内から、"type" が "user_summary" のメッセージを返却する。
    見つからなければ None を返す。
    """
    return next((msg for msg in messages if msg.get("type") == "user_summary"), "")

def format_offered_plans(plan_data: list[dict]) -> str:
    """
    JSON構造のプラン情報（リスト形式）を読みやすい文章に変換する。
    
    :param plan_data: プラン情報のリスト
    :return: 読みやすく整形されたプランの文章文字列
    """
    if not plan_data:
        return "プラン情報がありません。"
    
    result = ""
    for plan in plan_data:
        title = plan.get("title", "無題のプラン")
        result += f"【プランタイトル】: {title}\n"
        day_plans = plan.get("dayPlans", [])
        if not day_plans:
            result += "  ※日程情報がありません。\n"
        else:
            for day_plan in day_plans:
                day = day_plan.get("day", "日付不明")
                result += f"\n  [Day {day}]\n"
                
                # 宿泊施設情報
                accommodation = day_plan.get("accommodation", {})
                accom_name = accommodation.get("name", "不明な宿泊施設")
                accom_address = accommodation.get("address", "住所不明")
                price = accommodation.get("price", "不明")
                rating = accommodation.get("rating", "評価なし")
                access = accommodation.get("access", "")
                access_info = f"、アクセス: {access}" if access else ""
                result += f"    宿泊施設: {accom_name}{access_info}（住所: {accom_address}、価格: {price}円、評価: {rating}）\n"
                
                # 観光スポット情報
                spots = day_plan.get("spots", [])
                if spots:
                    result += "    観光スポット:\n"
                    for spot in spots:
                        spot_name = spot.get("name", "名称不明")
                        spot_address = spot.get("address", "住所不明")
                        result += f"      - {spot_name}（住所: {spot_address}）\n"
                
                # ランチ情報
                lunch = day_plan.get("lunch", [])
                if lunch:
                    result += "    ランチ:\n"
                    for restaurant in lunch:
                        res_name = restaurant.get("name", "名称不明")
                        res_address = restaurant.get("address", "住所不明")
                        result += f"      - {res_name}（住所: {res_address}）\n"
                
                # 夕食情報
                dinner = day_plan.get("dinner", [])
                if dinner:
                    result += "    夕食:\n"
                    for restaurant in dinner:
                        res_name = restaurant.get("name", "名称不明")
                        res_address = restaurant.get("address", "住所不明")
                        result += f"      - {res_name}（住所: {res_address}）\n"
        result += "\n"  # プランごとに余白を追加
    return result

def user_fbk_summary_node(state: AgentState) -> AgentState:
    # ここで phase1_messages と form_info を解析し、user_input を作成
    # 例: LLMを使って解析
    offered_plans = state.get("plans", [])
    form_info = state.get("form_info", {})
    messages = state.get("messages", [])
    if messages:
        user_hearing_summary = find_user_summary_message(messages)
        if user_hearing_summary != "":
            print("user_summary のメッセージが見つかりました:", user_hearing_summary)
        else:
            print("user_summary のメッセージは見つかりませんでした。")
            user_hearing_summary = ""   ## DBから取得したい
    else:
        raise ValueError("messagesが空です")


    user_fbk = state.get("user_fbk", "")
    offered_plans_ver_str = format_offered_plans(offered_plans)

    prompt = f"""
    あなたはAIエージェントチームのサマライザーです。ユーザの希望を要約してください。
    ##前提: これは、旅行プラン作成するためのサービスで、ユーザヒアリング、プラン作成を行いました。しかし、ユーザからFBKを受け取り、再度プランを練り直すことになった。
    ##やること： ユーザのヒアリング結果、提供したプラン、FBKをもとにユーザの希望を要約してください

    ## ヒアリング、提供したプラン、FBK
    入力フォーム情報：{form_info}
    ヒアリングの結果を要約したもの：{user_hearing_summary}
    提供したプラン: {offered_plans_ver_str}
    ユーザのFBK：{user_fbk}
    """
    
    response = llm_service.invoke(prompt)
    # メッセージとして保存
    if "messages" not in state:
        state["messages"] = []
    
    state["messages"].append({
        "role": "assistant",
        "content": response,
        "type": "user_fbk_summary"
    })
    return state

def planning_node(state: dict) -> dict:
    """
    チームの行動計画を立てるノード
    - 現状の分析
    - チームとして何をすべきか
    - どのような順序で進めるか
    - 各ステップでの判断基準
    を決定する
    """
    messages = state.get("messages", [])
    if messages:
        user_hearing_summary = find_user_summary_message(messages)
        if user_hearing_summary != "":
            print("user_summary のメッセージが見つかりました:", user_hearing_summary)
        else:
            print("user_summary のメッセージは見つかりませんでした。")
            user_hearing_summary = ""   ## DBから取得したい
    else:
        raise ValueError("messagesが空です")
    form_info = state.get("form_info", {})
    user_fbk = state.get("user_fbk", "")
    offered_plans = state.get("plans", [])
    offered_plans_ver_str = format_offered_plans(offered_plans)
    
    prompt = f"""
    以下のユーザの旅行要件に基づいて、旅行プラン作成に必要なタスクを洗い出してください。各日ごとに、以下の3つのカテゴリについて情報が必要です：
    - 宿泊（宿の候補や空室状況など）
    - 観光スポット（おすすめの観光地、イベント情報など）
    - 食事（レストラン、食事プランなど）

    また、各タスクで必要な外部API呼び出しの目的や必要なパラメータも簡潔に記述してください。

    【入力フォーム情報】
    {form_info} 
    【ヒアリングサマリー】
    {user_hearing_summary}

    【提供したプラン】 
    {offered_plans_ver_str}
    【ユーザのFBK】
    {user_fbk}

    注意すべき点：
    - ユーザーの希望は、フォーム情報とヒアリングサマリーをもとに、チームとしての行動計画を立てるための情報です。
    - 旅行日数によって提案数は増加していくので、日数を考慮に入れてどれくらい検索が必要かを考えてください
    """
    
    try:
        # チームの行動計画を取得
        planning_response = llm_service.invoke(prompt)
        
        # メッセージとして保存
        if "messages" not in state:
            state["messages"] = []
        
        state["messages"].append({
            "role": "assistant",
            "content": planning_response,
            "type": "team_planning"
        })
        
        return state
        
    except Exception as e:
        logger.error(f"チーム計画立案エラー: {str(e)}")
        raise

def clean_and_parse_json(response: str) -> dict:
    """LLMの応答からJSONを抽出してパース"""
    # マークダウンの装飾を削除
    cleaned_response = response.replace("```json", "").replace("```", "").strip()
    logger.debug("Cleaned Response:\n%s", cleaned_response)
    
    return json.loads(cleaned_response)

def task_node(state: dict) -> dict:
    """タスクリストを生成するノード"""
    try:
        messages = state.get("messages", [])
        user_fbk_summary = next((msg["content"] for msg in messages if msg.get("type") == "user_fbk_summary"), "")
        # 複数存在する場合は、最後の team_planning の内容を取得する
        team_planning_msgs = [msg["content"] for msg in messages if msg.get("type") == "team_planning"]
        planning_info = team_planning_msgs[-1] if team_planning_msgs else ""

        logger.info(f"user_fbk_summary: {user_fbk_summary}")
        logger.info(f"planning_info: {planning_info}")
        # プロンプトテンプレートを修正
        prompt = f"""
        あなたは旅行プランニングチームのタスクマネージャーです。
        以下の情報を元に、具体的な情報収集タスクのリストを作成してください。
        以下のタスクプランに基づいて、各タスクで実行するための具体的なAPIリクエスト内容を生成してください。各リクエストは、対象の日付、カテゴリ（宿泊、観光、食事）、および検索に必要な条件（予算、地域、ユーザの好みなど）を含むようにしてください。

        [ユーザの希望]
        {user_fbk_summary}

        【タスクプラン】
        {planning_info}

        """

        # LLMで処理
        response = llm_service.invoke_structured(
            TaskList,
            prompt
        )
        
        # TaskListオブジェクトを辞書に変換
        task_list_dict = response.model_dump()
        
        # 状態を更新（list[dict] として保存）
        state["task_list"] = task_list_dict["tasks"]
        return state

    except Exception as e:
        logger.error(f"タスク生成でエラーが発生: {str(e)}")
        logger.error(f"エラーの詳細: {str(e.__class__.__name__)}")
        raise

def execute_hotel_search(hotel_search: dict) -> List[dict]:
    """ホテル検索を実行"""
    try:
        result = fetch_hotels_by_class_code(
            middle_class_code=hotel_search['area']['middle_class_code'],
            small_class_code=hotel_search['area'].get('small_class_code'),
            detail_class_code=hotel_search['area'].get('detail_class_code'),
            checkin=hotel_search.get('checkin', "2025-04-01"),
            checkout=hotel_search.get('checkout', "2025-04-02"),
            num_adult=hotel_search.get('num_adults', 2),
            max_charge=hotel_search.get('budget', 10000),
            hits=2,
            keyword=hotel_search.get('keyword', "温泉")
        )
        logger.info(f"fetch_hotels_by_class_code result: {result} \n\n")
        
        # 結果がリスト形式で、エラー情報が含まれている場合
        if isinstance(result, list) and result and isinstance(result[0], dict) and "error" in result[0]:
            logger.error(f"API Error: {result[0].get('error_description')}")
            return []
        
        # 結果が辞書形式の場合、'hotels' キーからホテル情報のリストを取得
        if isinstance(result, dict):
            return result.get("hotels", [])
        
        return result
    except Exception as e:
        logger.info(f"ホテル検索でエラーが発生: {str(e)}")
        return []

def execute_restaurant_search(restaurant_search: dict) -> List[dict]:
    """レストラン検索を実行"""
    try:
        query = f"{restaurant_search['area']} {restaurant_search['cuisine_type']} レストラン {restaurant_search['meal_time']}"
        restaurants = search_places(query, max_places=2)
        # 予算でフィルタリング（簡易的な実装）
        filtered_restaurants = [
            r for r in restaurants
            if 'price_level' not in r or r.get('price_level', 0) * 10000 <= restaurant_search['budget']
        ]
        return filtered_restaurants
    except Exception as e:
        logger.info(f"レストラン検索でエラーが発生: {str(e)}")
        return []

def execute_spot_search(spot_search: dict) -> List[dict]:
    """観光スポット検索を実行"""
    try:
        query = f"{spot_search['area']} {spot_search['category']} 観光スポット"
        spots = search_places(query, max_places=2)
        return spots
    except Exception as e:
        logger.info(f"観光スポット検索でエラーが発生: {str(e)}")
        return []

def execution_node(state: dict) -> dict:
    """検索タスクを実行し、必要な情報を一括で収集するノード
    （検索結果を日付ごとにグループ化せず、全体として集約します）"""
    search_results = {
        'hotels': [],
        'restaurants': [],
        'spots': []
    }
    
    try:
        tasks = state.get("task_list", [])
        if not isinstance(tasks, list):
            tasks = [tasks]  # tasksをリスト化
        
        for task in tasks:
            # hotel_search がリストになっていることを想定
            hotel_search_list = task.get("hotel_search", [])
            if hotel_search_list and isinstance(hotel_search_list, list):
                for hotel_search in hotel_search_list:
                    logger.info(f"hotel_search: {hotel_search}")
                    hotels = execute_hotel_search(hotel_search)
                    if hotels:
                        search_results['hotels'].extend(hotels)
                        time.sleep(1)  # API呼び出し制限対応
            else:
                logger.info("エラー: タスクに有効なホテル検索情報がありません")
            
            for restaurant_search in task.get("restaurant_searches", []):
                restaurants = execute_restaurant_search(restaurant_search)
                search_results['restaurants'].extend(restaurants)
                time.sleep(1)
            
            for spot_search in task.get("spot_searches", []):
                spots = execute_spot_search(spot_search)
                search_results['spots'].extend(spots)
                time.sleep(1)
        
        if not search_results['hotels']:
            logger.warning("警告: ホテル検索結果が0件です")
        if not search_results['restaurants']:
            logger.warning("警告: レストラン検索結果が0件です")
        if not search_results['spots']:
            logger.warning("警告: 観光スポット検索結果が0件です")
    
    except Exception as e:
        logger.error(f"実行ノードでエラーが発生: {str(e)}")
        raise
    
    state["search_results"] = search_results
    return state

def reflection_node(state: dict) -> dict:
    """検索結果を評価するノード"""
    # 実際のチェックはスキップして、OKとする
    state["messages"].append({
        "role": "assistant",
        "content": "検索結果は要件を満たしています。",
        "type": "reflection"
    })
    return state

def extract_hotel_info(search_results: dict) -> list[dict]:
    """ネストされた検索結果からホテル情報を抽出する関数

    search_results の構造例:
    {
        "hotels": [
            {
                "pagingInfo": { ... },
                "hotels": [
                    {
                        "hotel": [
                            { "hotelBasicInfo": { ... } },
                            { "hotelRatingInfo": { ... } }
                        ]
                    },
                    ...
                ]
            },
            ...
        ],
        "restaurants": [ ... ],
        "spots": [ ... ]
    }
    """

def plans_create_node(state: dict) -> dict:
    """旅行プランを生成するノード"""
    try:
        # 必要な情報を取得
        user_fbk_summary = next((msg["content"] for msg in state.get("messages", []) if msg.get("type") == "user_fbk_summary"), "")
        planning_info = next((msg["content"] for msg in state.get("messages", []) if msg.get("type") == "team_planning"), "")
        search_results = state.get("search_results", {})

        old_plans = state.get("plans", [])
        offered_plans_ver_str = format_offered_plans(old_plans)

        # aggregated search_results（日付ごとではなくカテゴリ別に集約）
        search_results_text = "【検索された施設情報】\n"
        
        # ホテル情報の抽出と表示
        search_results_text += "\n■ ホテル\n"
        hotels = search_results.get("hotels", [])
        formatted_hotels_text = ""

        if hotels:
            for hotel_item in hotels:
                hotel_list = hotel_item.get("hotel", [])
                basic_info = {}
                rating_info = {}
                for entry in hotel_list:
                    if "hotelBasicInfo" in entry:
                        basic_info = entry["hotelBasicInfo"]
                    elif "hotelRatingInfo" in entry:
                        rating_info = entry["hotelRatingInfo"]

                if basic_info:
                    formatted_hotels_text += (
                        f"・ホテルNo: {basic_info.get('hotelNo', '不明')}\n"
                        f"  名前: {basic_info.get('hotelName', '不明')}\n"
                        f"  住所: {basic_info.get('address1', '不明')} {basic_info.get('address2', '')}\n"
                        f"  価格: {basic_info.get('hotelMinCharge', '不明')}\n"
                        f"  アクセス: {basic_info.get('access', '不明')}\n"
                        f"  駐車場情報: {basic_info.get('parkingInformation', '不明')}\n"
                        f"  郵便番号: {basic_info.get('postalCode', '不明')}\n"
                        f"  ホテル情報URL: {basic_info.get('hotelInformationUrl', '不明')}\n"
                        f"  プランリストURL: {basic_info.get('planListUrl', '不明')}\n"
                        f"  DPプランリストURL: {basic_info.get('dpPlanListUrl', '不明')}\n"
                        f"  レビューURL: {basic_info.get('reviewUrl', '不明')}\n"
                        f"  ホテルカナ名: {basic_info.get('hotelKanaName', '不明')}\n"
                        f"  ホテル特別情報: {basic_info.get('hotelSpecial', '不明')}\n"
                        f"  電話番号: {basic_info.get('telephoneNo', '不明')}\n"
                        f"  FAX番号: {basic_info.get('faxNo', '不明')}\n"
                        f"  ホテル画像URL: {basic_info.get('hotelImageUrl', '不明')}\n"
                        f"  サムネイル画像URL: {basic_info.get('hotelThumbnailUrl', '不明')}\n"
                        f"  客室画像URL: {basic_info.get('roomImageUrl', '不明')}\n"
                        f"  客室サムネイル画像URL: {basic_info.get('roomThumbnailUrl', '不明')}\n"
                        f"  地図画像URL: {basic_info.get('hotelMapImageUrl', '不明')}\n"
                        f"  (Basic) 評価: {basic_info.get('reviewAverage', '不明')}\n"
                        f"  (Basic) 評価数: {basic_info.get('reviewCount', '不明')}\n"
                        f"  ユーザーレビュー: {basic_info.get('userReview', '不明')}\n"
                        f"  入浴評価: {rating_info.get('bathAverage', '不明')}\n"
                        f"  設備評価: {rating_info.get('equipmentAverage', '不明')}\n"
                        f"  立地評価: {rating_info.get('locationAverage', '不明')}\n"
                        f"  食事評価: {rating_info.get('mealAverage', '不明')}\n"
                        f"  客室評価: {rating_info.get('roomAverage', '不明')}\n"
                        f"  サービス評価: {rating_info.get('serviceAverage', '不明')}\n"
                    )
                else:
                    # 基本情報が存在しなかった場合は、ホテル情報全体を文字列に変換して追加
                    formatted_hotels_text += str(hotel_item) + "\n"

        # 整形後の内容が空文字の場合は、代わりに raw な情報を追加する
        # formatted_hotels_text = ""
        if not formatted_hotels_text.strip():
            formatted_hotels_text = str(hotels) + "\n"

        search_results_text += formatted_hotels_text
        
        # レストラン情報
        search_results_text += "\n■ レストラン\n"
        if search_results.get("restaurants"):
            for restaurant in search_results["restaurants"]:
                search_results_text += (
                    f"・名前: {restaurant.get('name', '不明')}\n"
                    f"  住所: {restaurant.get('address', '不明')}\n"
                    f"  営業時間: {restaurant.get('opening_hours', '不明')}\n"
                    f"  電話番号: {restaurant.get('phone_number', '不明')}\n"
                    f"  評価: {restaurant.get('rating', '不明')}\n"
                    f"  ユーザ評価合計: {restaurant.get('user_ratings_total', '不明')}\n"
                    f"  ウィルソンスコア: {restaurant.get('wilson_score', '不明')}\n"
                    f"  詳細URL: {restaurant.get('related_url', '不明')}\n"
                    f"  検索クエリ: {restaurant.get('search_query', '不明')}\n"
                )
        else:
            search_results_text += "※レストラン情報がありません\n"
        
        # 観光スポット情報
        search_results_text += "\n■ 観光スポット\n"
        if search_results.get("spots"):
            for spot in search_results["spots"]:
                search_results_text += (
                    f"・名前: {spot.get('name', '不明')}\n"
                    f"  住所: {spot.get('address', '不明')}\n"
                    f"  説明: {spot.get('description', '不明')}\n"
                    f"  電話番号: {spot.get('phone_number', '不明')}\n"
                    f"  評価: {spot.get('rating', '不明')}\n"
                    f"  ユーザ評価合計: {spot.get('user_ratings_total', '不明')}\n"
                    f"  ウィルソンスコア: {spot.get('wilson_score', '不明')}\n"
                    f"  詳細URL: {spot.get('related_url', '不明')}\n"
                    f"  検索クエリ: {spot.get('search_query', '不明')}\n"
                )
        else:
            search_results_text += "※観光スポット情報がありません\n"
        
        prompt = f"""あなたは旅行プランナーです。
以下の情報に基づいて旅行プランを作成してください。出力はJSON形式で、以下のフォーマットに沿ってください。
また、プラン作成のためにthumbnailが抜けていたりする場合がある。この場合は、無理に入力せず、空欄にしてください。

検討すべき内容
- ユーザの希望に沿っているか
- 旅行日数とプランの日数が一致しているか=> アウトプットのjsonは、必ず日数分のプランを作成してください
- ホテル、レストラン、観光スポットの情報が正しいか
- ホテル、レストラン、観光スポットの情報がユーザの希望に沿っているか
- ホテル、レストラン、観光スポットの情報が旅行日数と一致しているか
- 最終日はホテル不要です。

[注意]
- 日数分プランを提示してください
- プランは、日数分提示してください
- 1日ごとに必要な情報は、ホテル、レストラン（ランチと、ディナー)、観光スポットです。
[ユーザの希望]
{user_fbk_summary}

[チームの計画]
{planning_info}

[検索結果]
{search_results_text}

[以前、提供したプラン] 1度ユーザには、プランを提供しており、FBKをもらっている。この状況を踏まえて、新しいプランを作成してください。
{old_plans}
"""
        # LLMで構造化出力を処理
        response = llm_service.invoke_structured(
            PlansOutput,
            prompt
        )
        
        # PlansOutputインスタンスから生成されたプランを状態に保存
        state["plans"] = response.plans
        return state

    except Exception as e:
        logger.error(f"プラン生成でエラーが発生: {str(e)}")
        logger.error(f"エラーの詳細: {str(e.__class__.__name__)}")
        raise


def build_phase3_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("user_fbk_summary_node", user_fbk_summary_node)
    workflow.add_node("planning_node", planning_node)
    workflow.add_node("task_node", task_node)
    workflow.add_node("execution_node", execution_node)
    workflow.add_node("reflection_node", reflection_node)
    workflow.add_node("plans_create_node", plans_create_node)

    workflow.add_edge(START, "user_fbk_summary_node")
    workflow.add_edge("user_fbk_summary_node", "planning_node")
    workflow.add_edge("planning_node", "task_node")
    workflow.add_edge("task_node", "execution_node")
    workflow.add_edge("execution_node", "reflection_node")
    # workflow.add_edge("reflection_node", "execution_node")
    workflow.add_edge("reflection_node", "plans_create_node")
    workflow.add_edge("plans_create_node", END)

    return workflow.compile()


