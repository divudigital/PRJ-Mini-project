from retriever import get_context

query = """
RSRP -115
Latency 73
Jitter 30
"""

result = get_context(query)

print("\n")
print("RETRIEVED KNOWLEDGE")
print("=" * 50)
print(result)