from typing import TypedDict, Optional
from langchain_core.messages import BaseMessage

class AgentState(TypedDict, total=False):
    """
    LangGraphで使う状態の例。
    """
    messages: list[BaseMessage]         # チャット履歴 (HumanMessage / AIMessage 等)
    current_phase: str                  # 'phase1','phase2','phase3'など
    user_personalize: str               # ユーザーの個性
    form_info: dict                     # ユーザの初期入力やヒアリングで集めた情報を入れる
    user_input: str                     # ユーザーからの入力
    is_done: bool                       # フロー完了フラグなど
    phase2_task: list[dict]             # フェーズ2のタスク
    plans: list[dict]                   # プランのリスト
    preferences: dict                    # ユーザーの旅行プランの方向性
    search_tasks: list[dict]           # 検索タスクのリスト
    phase1_messages: list[dict]         # フェーズ1のメッセージ
    user_summary: str                   # ユーザーの要望サマリー
    planning_info: str                   # チームの計画
    task_list: list[dict]               # タスクリスト
    search_results: list[dict]           # 検索結果
    plans: list[dict]                   # プランのリスト