from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

def handle_phase2_request(
    state_input,
    thread_id,
    body,
    main_graph,
    config
):
    logger.info("=== handle_phase2_request start ===")
    state_input["current_phase"] = "phase2"
    state_input["phase1_messages"] = body.get("messages", [])
    state_input["form_info"] = body.get("form_info", {})
    for event in main_graph.stream(
        state_input,
        config=config
    ):
        logger.info("event:" + str(event))
        result = event
    # result = state_input
    return create_phase2_response(result, thread_id, body)

def recursive_model_dump(obj):
    """
    Pydantic モデルをはじめ、ネストされたモデルやリスト、辞書の場合、
    再帰的に辞書に変換する関数です。
    """
    # Pydantic v2 の場合は model_dump で、v1 の場合は dict() を使います
    if hasattr(obj, "model_dump"):
        return recursive_model_dump(obj.model_dump())
    elif hasattr(obj, "dict"):
        return recursive_model_dump(obj.dict())
    elif isinstance(obj, dict):
        return {k: recursive_model_dump(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_model_dump(item) for item in obj]
    else:
        return obj

def create_phase2_response(
    result: dict, 
    thread_id: str, 
    body: dict
) -> Dict[str, Any]:
    """Phase2のレスポンスを生成する"""
    logger.info("=== create_phase2_response start ===")
    logger.info(f"result: {result}")
    logger.info(f"result.change_phase: {result.get('change_phase', {}).get('plans', {})}")
    
    # change_phase内の plans を取得し、可能な範囲で再帰的に辞書に変換する
    plans = result.get('change_phase', {}).get('plans', {})
    logger.info(f"plans: {plans}")
    logger.info("plansの型: " + str(type(plans)))
    logger.info("===========================")
    if plans:
        plans = recursive_model_dump(plans)
        # 単一のプランを配列に変換
        if not isinstance(plans, list):
            plans = [plans]
    else:
        plans = []
    
    response = {
        "form_info": body.get("form_info", {}),
        "current_phase": "phase3",
        "thread_id": body.get("thread_id", ""),
        "messages": body.get("messages", []),
        "user_input_message": "",
        "plans": plans
    }
    
    # レスポンス全体を再帰的に変換してから返す
    return response