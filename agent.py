# (LangGraph + RAG Enhanced Agent)

from typing import TypedDict

from langgraph.graph import StateGraph, END

from retriever import get_context

from tools import (
    trigger_fastapi_reconfiguration,
    trigger_slice_reallocation,
    trigger_power_boost
)


# ==================================================
# STATE
# ==================================================

class TelemetryState(TypedDict):
    cell_id: str
    rsrp: float
    sinr: float
    latency: float
    jitter: float
    status: str
    action_taken: str
    rag_context: str



# ==================================================
# NODE 1
# TELEMETRY MONITORING
# ==================================================

def monitor_telemetry_node(
    state: TelemetryState
) -> TelemetryState:

    rsrp = state.get("rsrp", -80)

    latency = state.get("latency", 30)

    jitter = state.get("jitter", 5)

    if rsrp < -105 or latency > 50 or jitter > 15:

        state["status"] = "DEGRADED"

    else:

        state["status"] = "NORMAL"

    return state


# ==================================================
# NODE 2
# RAG KNOWLEDGE RETRIEVAL
# ==================================================

def rag_context_node(
    state: TelemetryState
) -> TelemetryState:

    query = f"""
    RSRP {state.get("rsrp")}
    SINR {state.get("sinr")}
    Latency {state.get("latency")}
    Jitter {state.get("jitter")}
    """

    context = get_context(query)

    state["rag_context"] = context

    return state


# ==================================================
# NODE 3
# RCA + REMEDIATION
# ==================================================

def rca_reasoning_node(
    state: TelemetryState
) -> TelemetryState:

    if state["status"] == "NORMAL":

        state[
            "action_taken"
        ] = "No action required. Cell operating within SLA."

        return state

    cell_id = state.get(
        "cell_id",
        "VNIT_NAGPUR_CELL_01"
    )

    latency = state.get("latency", 0)

    jitter = state.get("jitter", 0)

    rsrp = state.get("rsrp", -80)

    rag_context = state.get(
        "rag_context",
        ""
    )

    print("\n")
    print("=" * 60)
    print("RAG KNOWLEDGE USED")
    print("=" * 60)
    print(rag_context)
    print("=" * 60)
    print("\n")

    # -----------------
    # Decision Logic
    # -----------------

    if latency > 50 or jitter > 15:

        result = trigger_slice_reallocation(
            cell_id,
            slice_type="URLLC"
        )

        reason = (
            "High latency / jitter detected. "
            "URLLC slice recommended."
        )

    elif rsrp < -105:

        result = trigger_power_boost(
            cell_id,
            power_boost_dbm=3
        )

        reason = (
            "Weak signal detected. "
            "Power boost initiated."
        )

    else:

        result = trigger_fastapi_reconfiguration(
            cell_id,
            bandwidth_boost_mhz=15
        )

        reason = (
            "Bandwidth optimization triggered."
        )

    state["action_taken"] = f"""
    ROOT CAUSE:
    {reason}

    ACTION:
    {result}

    KNOWLEDGE SOURCE:
    RAG Telecom Knowledge Base
    """

    return state


# ==================================================
# LANGGRAPH
# ==================================================

workflow = StateGraph(
    TelemetryState
)

workflow.add_node(
    "monitor",
    monitor_telemetry_node
)

workflow.add_node(
    "rag",
    rag_context_node
)

workflow.add_node(
    "remediation",
    rca_reasoning_node
)

workflow.set_entry_point(
    "monitor"
)

workflow.add_edge(
    "monitor",
    "rag"
)

workflow.add_edge(
    "rag",
    "remediation"
)

workflow.add_edge(
    "remediation",
    END
)

app = workflow.compile()

self_healing_graph = app