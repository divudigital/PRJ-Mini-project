#(FastAPI / टेस्ट एग्जीक्यूशन)(Kaggle Dataset '5g_network_data.csv' Integration)

import os
import pandas as pd
from agent import app

def run_agent_on_dataset():
    csv_path = os.path.join("colab_data", "5g_network_data.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} file not found!")
        return

    df = pd.read_csv(csv_path)
    
    # Dataset से dynamic row selection
    random_row = df.sample(n=1).iloc[0]

    # Flexible column mapping (अक्सर CSV में अलग नाम होते हैं)
    rsrp_col = next((col for col in df.columns if 'signal' in col.lower() or 'rsrp' in col.lower()), None)
    latency_col = next((col for col in df.columns if 'latency' in col.lower()), None)
    sinr_col = next((col for col in df.columns if 'sinr' in col.lower()), None)

    # Values extraction with dynamic fallback ranges if column not matched
    rsrp_val = float(random_row[rsrp_col]) if rsrp_col else float(random_row.iloc[0])
    latency_val = float(random_row[latency_col]) if latency_col else float(random_row.iloc[1])
    sinr_val = float(random_row[sinr_col]) if sinr_col else 4.0

    initial_state = {
        "cell_id": "VNIT_NAGPUR_CELL_01",
        "rsrp": rsrp_val,
        "sinr": sinr_val,
        "latency": latency_val,
        "status": "UNKNOWN",
        "action_taken": "NONE"
    }

    print("\n" + "="*50)
    print(f"Incoming Telemetry -> RSRP: {rsrp_val} dBm, SINR: {sinr_val} dB, Latency: {latency_val} ms")
    print("Executing Autonomous Agent Self-Healing Loop...")
    print("="*50)

    output = app.invoke(initial_state)

    print("\n==================== AGENT EXECUTION RESULT ====================")
    print(f"Cell ID      : {output.get('cell_id', 'VNIT_NAGPUR_CELL_01')}")
    print(f"SLA Status   : {output.get('status', 'NORMAL')}")
    print(f"Action Taken : {output.get('action_taken', 'No action needed.')}")
    print("================================================================")

if __name__ == "__main__":
    run_agent_on_dataset()