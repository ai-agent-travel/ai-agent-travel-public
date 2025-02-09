# src/main.py

from flask import Flask, request, jsonify
import uuid
import logging
from dotenv import load_dotenv
import os
from langgraph.types import Command
from core.graph import build_main_graph
from core.state import AgentState
from phases.phase1.handler import handle_phase1_request
from phases.phase2.handler import handle_phase2_request
from phases.phase3.handler import handle_phase3_request
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
load_dotenv()

CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", os.getenv("PROJECT_FRONTEND_URL", "http://localhost:3000")],
        "allow_headers": ["Content-Type"],
    }
})
# グラフをビルド
main_graph = build_main_graph()
logger.info("=== Main graph built ===")
logger.info(main_graph.get_graph(xray=1).draw_mermaid())


@app.route("/agent", methods=["POST"])
def chat_api():
    """
    リクエスト例:
    {
      "thread_id": "xxxxx",   // 省略可(新規ならUUID生成)
      "user_message": "ユーザの入力(省略可)",
      "form_info": { "place": "沖縄" } // 初回のみ設定してもOK
    }
    """
    state_input = {}
    body = request.get_json() or {}
    thread_id = body.get("thread_id") or str(uuid.uuid4())
    user_message = body.get("user_message", "")
    current_phase = body.get("current_phase", "phase1")
    form_info = body.get("form_info", {})

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    if current_phase == "phase1":
        return handle_phase1_request(
            state_input,
            user_message,
            form_info,
            thread_id,
            current_phase,
            main_graph,
            config
        )
    elif current_phase == "phase2":
        # Phase2の処理
        return handle_phase2_request(
            state_input,
            thread_id,
            body,
            main_graph,
            config
        )
    elif current_phase == "phase3":
        # Phase3の処理
        return handle_phase3_request(
            state_input,
            thread_id,
            body,
            main_graph,
            config
        )
    else:
        return jsonify({
            "error": "Invalid phase",
            "message": f"Unknown phase: {current_phase}"
        }), 400

@app.route("/healthcheck", methods=["GET"])
def health():
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8083)), debug=True)