#(LangGraph + Local Ollama LLM)

import json
# Agentic Self-Healing Workflow Engine
from typing import TypedDict
from langgraph.graph import StateGraph, END
from tools import (
    trigger_fastapi_reconfiguration,
    trigger_slice_reallocation,
    trigger_power_boost
)

# State Definition
class TelemetryState(TypedDict):
    cell_id: str
    rsrp: float
    sinr: float
    latency: float
    jitter: float
    status: str
    action_taken: str

# 1. Monitoring & Anomaly Detection Node
def monitor_telemetry_node(state: TelemetryState) -> TelemetryState:
    rsrp = state.get("rsrp", -80)
    latency = state.get("latency", 30)
    jitter = state.get("jitter", 5)

    if rsrp < -105 or latency > 50 or jitter > 15:
        state["status"] = "DEGRADED"
    else:
        state["status"] = "NORMAL"
    return state

# 2. Dynamic RCA & Multi-Action Remediation Node
def rca_reasoning_node(state: TelemetryState) -> TelemetryState:
    if state["status"] == "NORMAL":
        state["action_taken"] = "No action required. Cell operating within optimal SLA limits."
        return state

    cell_id = state.get("cell_id", "VNIT_NAGPUR_CELL_01")
    latency = state.get("latency", 0)
    jitter = state.get("jitter", 0)
    rsrp = state.get("rsrp", -80)

    # Context-Aware Decision Matrix based on Root Cause
    if latency > 50 or jitter > 15:
        # Priority 1: High Latency / Buffer Jitter -> Slice Migration (URLLC)
        result = trigger_slice_reallocation(cell_id, slice_type="URLLC")
    elif rsrp < -105:
        # Priority 2: Weak Signal / Edge Coverage -> gNodeB Power Boost
        result = trigger_power_boost(cell_id, power_boost_dbm=3)
    else:
        # Priority 3: Low Throughput / Bandwidth Limit -> Carrier Aggregation
        result = trigger_fastapi_reconfiguration(cell_id, bandwidth_boost_mhz=15)

    state["action_taken"] = result
    return state

# Build LangGraph Workflow
workflow = StateGraph(TelemetryState)
workflow.add_node("monitor", monitor_telemetry_node)
workflow.add_node("remediation", rca_reasoning_node)

workflow.set_entry_point("monitor")
workflow.add_edge("monitor", "remediation")
workflow.add_edge("remediation", END)

app = workflow.compile()
self_healing_graph = app