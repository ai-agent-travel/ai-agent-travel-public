from flask import jsonify
from langgraph.types import Command
import logging
from core.state import AgentState
from typing import Dict, Any
import os
import firebase_admin
from firebase_admin import credentials, firestore

logger = logging.getLogger(__name__)

# Firestore の利用を無効化する環境変数 (DISABLE_FIRESTORE) を確認し、利用するかどうかを決定します。
DISABLE_FIRESTORE = os.getenv("DISABLE_FIRESTORE", "false").lower() == "true"

if not DISABLE_FIRESTORE:
    if not firebase_admin._apps:
        try:
            # Application Default Credentials を使用して初期化します。
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print("Firestore の初期化に失敗しました。エラー:", e)
            DISABLE_FIRESTORE = True

db = None
if not DISABLE_FIRESTORE:
    try:
        db = firestore.client()
    except Exception as e:
        print("Firestore クライアントの取得に失敗しました。エラー:", e)
        DISABLE_FIRESTORE = True

def save_to_firestore(data: dict) -> None:
    """
    レスポンスデータを Firestore の 'responses' コレクションに保存する処理です。
    Firestore が利用できない場合はエラーを発生させずにスキップします。
    """
    if DISABLE_FIRESTORE or db is None:
        print("Firestore が無効または利用できないため、保存処理をスキップします。")
        return

    try:
        doc_ref = db.collection('responses').document()
        doc_ref.set(data)
        print("Firestore への保存に成功しました。")
    except Exception as e:
        print("Firestore への保存中にエラーが発生しました。エラー:", e)

def load_user_personalize() -> str:
    """
    Firestore からユーザのパーソナライズデータを取得する処理を行います。
    初回の入力時に使用され、Firestore が利用できない場合やデータが存在しない場合は空文字を返します。
    """
    if DISABLE_FIRESTORE or db is None:
        print("Firestore が無効のため、ユーザのパーソナライズデータを空文字で初期化します。")
        return ""
    try:
        # Firestore 上の 'user_personalize' コレクションの 'default' ドキュメントからデータを取得する想定です。
        doc = db.collection('user_personalize').document('default').get()
        if doc.exists:
            data = doc.to_dict()
            return data.get("value", "")
        else:
            print("Firestore にユーザパーソナライズのデフォルトデータが存在しません。")
            return ""
    except Exception as e:
        print("Firestore からユーザパーソナライズデータの取得中にエラーが発生しました。エラー:", e)
        return ""

def handle_phase1_request(
    state_input: dict,
    user_message: str,
    form_info: dict,
    thread_id: str,
    current_phase: str,
    main_graph,
    config: dict
) -> Dict[str, Any]:
    """Phase1のリクエスト処理を行うハンドラー"""

    # 初回の入力の場合、state_input に 'user_personalize' キーが存在しなければ
    # Firestore からユーザパーソナライズデータを取得して挿入します。
    if "user_personalize" not in state_input:
        state_input["user_personalize"] = load_user_personalize()

    if current_phase:
        state_input["current_phase"] = current_phase

    if user_message:
        if form_info:
            state_input["form_info"] = form_info

        for event in main_graph.stream(
            Command(resume=user_message),
            config=config,
            stream_mode="updates"
        ):
            logger.info("event:" + str(event))
            result = event.get("change_phase", event)
    else:
        if form_info:
            state_input["form_info"] = form_info

        for event in main_graph.stream(
            state_input,
            config=config
        ):
            logger.info(event)
            result = event.get("change_phase", event)

    return create_phase1_response(result, thread_id, current_phase, form_info)

def create_phase1_response(
    result: dict, 
    thread_id: str, 
    current_phase: str,
    form_info: dict
) -> Dict[str, Any]:
    """Phase1のレスポンスを生成する"""

    logger.info(f"result: {result}")
    current_phase = result.get("current_phase", current_phase)
    
    base_response = {
        "form_info": form_info,
        "current_phase": current_phase,
        "thread_id": thread_id,
        "user_input_message": "",
        "plans": []  # phase1では空配列
    }
    
    def format_messages(messages):
        """メッセージを指定された形式に変換する"""
        formatted_messages = []
        logger.info(f"messages_handler: {messages}")
        for i, msg in enumerate(messages, 1):
            formatted_msg = {
                "role": msg.get("role", "assistant"),
                "content": msg.get("content", ""),
                "order": i
            }
            if formatted_msg["role"] == "assistant":
                formatted_msg["selector"] = msg.get("selector", [])
            formatted_messages.append(formatted_msg)
        return formatted_messages
    
    if "__interrupt__" in result:
        interrupt_data = result["__interrupt__"][0].value
        interrupt_messages = interrupt_data.get("__interrupt__", {}).get("messages", [])
        
        return {
            **base_response,
            "interrupt": True,
            "messages": format_messages(interrupt_messages) if interrupt_messages else [
                {
                    "role": "assistant",
                    "content": interrupt_data.get("__interrupt__", {}).get("question", ""),
                    "selector": ["", ""],
                    "order": 1
                }
            ]
        }
    else:
        response = {
            **base_response,
            "interrupt": False,
            "messages": format_messages(result.get("messages", [
                {
                    "role": "assistant",
                    "content": "",
                    "selector": ["", ""],
                    "order": 1
                }
            ]))
        }

        # Firestore への保存を試みますが、利用できなければエラーはログに記録してスキップします。
        save_to_firestore(response)

        return response 