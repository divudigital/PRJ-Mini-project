from agent import self_healing_graph

result = self_healing_graph.invoke(
    {
        "cell_id": "CELL_001",
        "rsrp": -115,
        "sinr": 2,
        "latency": 73,
        "jitter": 30
    }
)

print("\n")
print("=" * 70)
print("AGENTIC REMEDIATION RESULT")
print("=" * 70)

print(f"Status: {result['status']}")

print("\nAction Taken:")
print(result["action_taken"])

print("\nRetrieved Knowledge:")
print(result["rag_context"])

print("=" * 70)