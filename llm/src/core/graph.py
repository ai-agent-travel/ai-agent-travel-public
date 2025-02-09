# src/core/graph.py

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from core.state import AgentState
# from phases.phase1.graph import build_phase1_graph
from phases.phase1.graph import hearing_llm_node
from phases.phase1.graph import human_node
from phases.phase2.graph import build_phase2_graph
from phases.phase3.graph import build_phase3_graph

from langgraph.types import Command

import logging

logger = logging.getLogger(__name__)

def router_node(state: AgentState) -> AgentState:
    logger.info(f"state: {state}")
    if state["current_phase"] == "phase1":
        return state
    elif state["current_phase"] == "phase2":
        return state
    elif state["current_phase"] == "phase3":
        return state




def change_phase(state: AgentState) -> AgentState:
    if state["current_phase"] == "phase1":
        state["current_phase"] = "phase2"
    elif state["current_phase"] == "phase2":
        state["current_phase"] = "phase3"
    
    return state

# def build_main_graph():
#     memory_saver = MemorySaver()

#     phase1_graph = build_phase1_graph()

#     # メイングラフを作る (ここではシンプルに phase1_graph しか呼ばない)
#     main_flow = StateGraph(AgentState)
#     main_flow.add_node("phase1_subgraph", phase1_graph.compile())
#     main_flow.set_entry_point("phase1_subgraph")

#     # phase1_subgraph が終了すると END に行く
#     main_flow.add_edge("phase1_subgraph", END)

#     # コンパイルに checkpointer を指定すると、interrupt 時にデータが保持される
#     compiled_graph = main_flow.compile(checkpointer=memory_saver)
#     return compiled_graph


def build_main_graph():


    memory_saver = MemorySaver()

    phase2_subgraph = build_phase2_graph()
    phase3_subgraph = build_phase3_graph()


    # メイングラフを作る (ここではシンプルに phase1_graph しか呼ばない)
    workflow = StateGraph(AgentState)
    workflow.add_node("router", router_node)
    ## phase1
    workflow.add_node("human_node", human_node)
    workflow.add_node("hearing_llm", hearing_llm_node)
    ## phase2
    workflow.add_node("phase2_subgraph", phase2_subgraph)
    ## phase3
    workflow.add_node("phase3_subgraph", phase3_subgraph)
    ## change_phase
    workflow.add_node("change_phase", change_phase)

    workflow.add_edge(START, "router")
    workflow.add_conditional_edges(
        "router",
        lambda state: state["current_phase"],
        {
            "phase1": "hearing_llm",
            "phase2": "phase2_subgraph",
            "phase3": "phase3_subgraph"
        }
    )
    workflow.add_edge("phase2_subgraph", "change_phase")
    workflow.add_edge("phase3_subgraph", "change_phase")
    workflow.add_edge("change_phase", END)


    # コンパイルに checkpointer を指定すると、interrupt 時にデータが保持される
    compiled_graph = workflow.compile(checkpointer=memory_saver)
    return compiled_graph
