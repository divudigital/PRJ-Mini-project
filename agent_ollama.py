import json
from typing import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama

# ==========================================
# 1. STATE DEFINITION
# ==========================================
class TelemetryState(TypedDict):
    cell_id: str
    rsrp: float       # Reference Signal Received Power (dBm)
    sinr: float       # Signal-to-Interference-plus-Noise Ratio (dB)
    latency: float    # Latency in ms
    status: str       # "NORMAL" or "DEGRADED"
    action_taken: str

# ==========================================
# 2. DETERMINISTIC AGENT TOOL / ACTION
# ==========================================
class ReconfigureSchema(BaseModel):
    cell_id: str = Field(description="Target 5G Cell Tower ID")
    bandwidth_boost_mhz: int = Field(description="Additional bandwidth allocation (Max 20MHz)")

def trigger_fastapi_reconfiguration(cell_id: str, bandwidth_boost_mhz: int) -> str:
    """Simulates a REST API call to FastAPI microservice to reconfigure RAN bandwidth."""
    # 3GPP Safety Guardrail
    if bandwidth_boost_mhz > 20:
        bandwidth_boost_mhz = 20
    
    return f"SUCCESS: REST API invoked -> Cell {cell_id} allocated +{bandwidth_boost_mhz}MHz bandwidth boost. QoS restored."

# ==========================================
# 3. LANGGRAPH NODES
# ==========================================
def monitoring_node(state: TelemetryState) -> TelemetryState:
    """Node 1: SLA Threshold Checker."""
    if state["rsrp"] < -110 or state["sinr"] < 5 or state["latency"] > 50:
        state["status"] = "DEGRADED"
    else:
        state["status"] = "NORMAL"
    return state

def rca_reasoning_node(state: TelemetryState) -> TelemetryState:
    """Node 2: Local Ollama LLM Reasoning & Action Execution."""
    if state["status"] == "NORMAL":
        state["action_taken"] = "No action required. Network operating within SLA."
        return state

    # Local Ollama LLM instance (No API Key needed)
    llm = Ollama(model="llama3.2:1b", temperature=0)

    prompt = f"""
    You are an Autonomous 5G Network Agent.
    Cell Tower: {state['cell_id']} is experiencing network degradation.
    Current Telemetry:
    - RSRP: {state['rsrp']} dBm (SLA Limit: > -110 dBm)
    - SINR: {state['sinr']} dB (SLA Limit: > 5 dB)
    - Latency: {state['latency']} ms (SLA Limit: < 50 ms)

    Determine the required bandwidth boost in MHz (between 5 and 20) to recover the network.
    Return ONLY a valid JSON with keys "cell_id" and "bandwidth_boost_mhz".
    Example output format:
    {{"cell_id": "{state['cell_id']}", "bandwidth_boost_mhz": 15}}
    """

    try:
        response_text = llm.invoke(prompt)
        # JSON Extracting logic from response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        
        action_data = json.loads(json_str)
        
        # Execute Deterministic Tool
        result = trigger_fastapi_reconfiguration(
            cell_id=action_data.get("cell_id", state["cell_id"]),
            bandwidth_boost_mhz=action_data.get("bandwidth_boost_mhz", 10)
        )
        state["action_taken"] = result

    except Exception as e:
        # Fallback Safe Rule Execution
        state["action_taken"] = trigger_fastapi_reconfiguration(state["cell_id"], 15)

    return state

# ==========================================
# 4. BUILD THE LANGGRAPH WORKFLOW
# ==========================================
builder = StateGraph(TelemetryState)

builder.add_node("Monitor", monitoring_node)
builder.add_node("ReasonAndAct", rca_reasoning_node)

builder.set_entry_point("Monitor")
builder.add_edge("Monitor", "ReasonAndAct")
builder.add_edge("ReasonAndAct", END)

self_healing_graph = builder.compile()

# ==========================================
# 5. TEST EXECUTION (Simulated Degraded Cell)
# ==========================================
if __name__ == "__main__":
    test_input = {
        "cell_id": "NAGPUR_CELL_08",
        "rsrp": -118.5,  # Degraded
        "sinr": 3.2,     # High Interference
        "latency": 78.0, # High Latency
        "status": "UNKNOWN",
        "action_taken": ""
    }

    print("\nRunning Autonomous 5G Self-Healing Loop via Local Ollama LLM...")
    output = self_healing_graph.invoke(test_input)
    
    print("\n================ RESULT ================")
    print(f"Cell ID      : {output['cell_id']}")
    print(f"SLA Status   : {output['status']}")
    print(f"Action Taken : {output['action_taken']}")
    print("========================================")
    