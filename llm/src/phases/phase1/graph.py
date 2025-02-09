from typing import Literal
from langgraph.graph import StateGraph, END
from core.state import AgentState
from services.llm import llm_service
from langgraph.types import Command, interrupt
from langchain_core.messages import AIMessage, HumanMessage
from phases.phase1.schemas import Messages
import logging
from langchain_core.messages import AIMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
logger = logging.getLogger(__name__)

def human_node(state: AgentState) -> AgentState:
    """
    ユーザー入力を処理するノード
    """
    logger.info("=== human_node start ===")
    logger.info(f"state: {state}")
    user_input = ""
    user_input = interrupt(
        value={
            "__interrupt__": {
                "question": "何かご希望やご要望はありますか？",
                "messages": state.get("messages", []),
                "form_info": state.get("form_info", {})
            }
        }
    )
    
    # resumeで受け取った値を確認
    messages = state.get("messages", [])
    if user_input:
        logger.info(f"Received user inputs: {user_input}")
        
        # messagesを更新
        messages.append({"role": "human", "content": str(user_input)})
        logger.info(f"messages: {messages}")

    
        # ユーザー入力待ちの場合はinterrupt
    return Command(
        update={
            "messages": messages
        },
        goto="hearing_llm"
    )



def hearing_llm_node(state: AgentState) -> Command[Literal["human_node", "change_phase"]]:
    messages = state.get("messages", [])
    form_info = state.get("form_info", {})
    user_personalize = state.get("user_personalize", "")

    # 過去の会話履歴をテキストとしてまとめる
    if messages and messages[-1].get("role", "") == "human":
        messages_to_include = messages[:-1]
    else:
        messages_to_include = messages

    history_text = "\n".join(
        f'{"あなた(ケビン)" if msg.get("role") == "assistant" else msg.get("role", "")}: {msg.get("content", "")}'
        for msg in messages_to_include if msg is not None
    )

    # messagesリストが空でないことを確認した上で最後のメッセージを評価
    if messages and messages[-1].get("role", "") == "human":
        input_content = messages[-1].get("content", "")
    else:
        input_content = ""
    logger.info(f"input_content: {input_content}")

    # ChatPromptTemplateを使用してプロンプトを作成
    # システムメッセージ内に {history} プレースホルダを追加し、
    # これまでの会話履歴を参照できるようにします。
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "あなたは旅行コンシェルジュのケビンです。"
                "すでに以下の情報が入力されています:\n"
                "- 行き先: {place}\n"
                "- 出発日: {startDate}\n"
                "- 帰着日: {endDate}\n"
                "- 人数: {people}\n"
                "- 宿泊宿全体の予算: {accomodationBudget}\n\n"
                "これらの情報を元に、旅行プラン作成に必要な追加情報をユーザから引き出します。\n"
                "質問は必ず、宿泊先、観光スポット、グルメ、または旅のスタイルに関するもののみとしてください。\n"
                "質問は簡潔かつフレンドリーにし、全体で5ターン程度に必要な情報が揃ったと判断できたら、"
                "直ちに『これで必要な情報が揃いました』と伝えてください。\n"
                "質問しないでいい項目、予算について。移動手段。など質問する必要はない。"
                "出力は、メッセージと is_done の2つのみです。"
                "メッセージは role、content、selector の3つのみを含み、selector には内容に対する選択肢を示してください。"
                "これまでのヒアリング履歴:\n{history}\n\n"
                "ユーザの入力に対して、次の質問を考えてください、OKの場合は、messageのcontentに「これで必要な情報が揃いました。プランを作成します」とし、is_doneをTrueにしてください。"
            ),
            ("human", "{input}\n" "ユーザーの特徴: '{user_personalize}'\nユーザの特徴がある場合、ユーザーの特徴を20%ほど考慮して質問してください。")
        ]
    )

    # 各変数に実際の値を注入（form_info から取得、また会話履歴とユーザーの最新入力も渡す）
    prompt_text = prompt.format(
        history=history_text,
        place=form_info.get("place", ""),
        startDate=form_info.get("startDate", ""),
        endDate=form_info.get("endDate", ""),
        people=form_info.get("people", ""),
        accomodationBudget=form_info.get("accomodationBudget", ""),
        input=input_content,  # ユーザーの追加入力
        user_personalize=user_personalize
    )

    logger.info("LLMへのプロンプト送信前のテキスト: %s", prompt_text)
    response_data = llm_service.invoke_structured_v2(Messages, prompt_text)
    logger.info(f"response_data: {response_data}")
    response_dict = response_data.dict()
    logger.info(f"response_dict: {response_dict}")
    updated_messages = messages + [response_dict.get("message", {})]
    logger.info(f"updated_messages: {updated_messages}")
    if response_dict.get("is_done", False):
        logger.info("これで必要な情報が揃いました")
        return Command(
            update={
                "messages": updated_messages,
                "is_done": response_dict.get("is_done", True)
            },
            goto="change_phase"
        )
    else:
        return Command(
            update={
                "messages": updated_messages
            },
            goto="human_node"
        )