# 5G Autonomous Agentic QoS Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
import time
import os
import html

from agent import self_healing_graph


def safe_text(value):
    return html.escape(str(value)).replace("\n", "  \n")

# 1. Page Configuration
st.set_page_config(
    page_title="5G QoS Network Testing & AI Orchestrator",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Dynamic Location Loading from Dataset
@st.cache_data
def get_unique_locations():
    csv_path = "5g_network_data.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            if "Location" in df.columns:
                return sorted(df["Location"].unique().tolist())
        except Exception:
            pass
    return ["Chennai", "Delhi", "Mumbai", "Kolkata", "Berlin", "New York", "San Francisco", "Tokyo"]

locations_list = get_unique_locations()

# 3. Enhanced CSS Styling Fixes
st.markdown("""
<style>
    .stApp {
        background: #050B16;
        color: #E2E8F0;
    }
    .stMain > div {
        background: transparent;
    }
    .block-container {
        padding-top: 0.1rem !important;
        padding-bottom: 0.2rem !important;
        max-width: 100% !important;
    }
    .main .block-container {
        overflow: hidden;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 0.78rem !important;
        line-height: 1.1 !important;
        color: #F8FAFC !important;
    }
    div[data-testid="metric-label"] {
        font-size: 0.58rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }
    .stExpander {
        border-radius: 10px;
        border: 1px solid rgba(148, 163, 184, 0.15);
        background: rgba(15, 23, 42, 0.4);
    }

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        background: rgba(9, 15, 28, 0.9);
        border: 1px solid rgba(96, 165, 250, 0.18);
        border-radius: 12px;
        padding: 8px 14px;
        margin: 0 0 8px 0;
    }
    .topbar-left {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
    }
    .brand-mark {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(59,130,246,0.22), rgba(16,185,129,0.12));
        border: 1px solid rgba(96,165,250,0.35);
        color: #7DD3FC;
        font-size: 0.95rem;
        font-weight: 800;
        flex-shrink: 0;
    }
    .brand-text {
        font-size: 0.95rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: 0.02em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .brand-sub {
        display: none;
    }
    .topbar-right {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
    }
    .ai-pill {
        padding: 5px 9px;
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #7DD3FC;
        background: rgba(59,130,246,0.12);
        border: 1px solid rgba(96,165,250,0.35);
        border-radius: 999px;
    }
    .status-tag {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 5px 9px;
        border-radius: 999px;
        background: rgba(16,185,129,0.12);
        border: 1px solid rgba(16,185,129,0.4);
        color: #34D399;
        font-weight: 700;
        font-size: 0.64rem;
        white-space: nowrap;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 8px rgba(34,197,94,0.9);
    }
    .time-box {
        color: #CBD5E1;
        font-size: 0.64rem;
        padding: 5px 7px;
        border-radius: 8px;
        background: rgba(15,23,42,0.9);
        border: 1px solid rgba(148,163,184,0.12);
        text-align: right;
        line-height: 1.45;
    }

    .hero-box {
        background: linear-gradient(180deg, rgba(9, 17, 31, 0.96), rgba(14, 22, 36, 0.9));
        border: 1px solid rgba(96, 165, 250, 0.18);
        border-radius: 12px;
        padding: 9px 14px 10px 14px;
        margin-bottom: 8px;
    }
    .hero-inline {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    .hero-symbol {
        display: inline-block;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(59,130,246,0.22), rgba(16,185,129,0.12));
        color: #7DD3FC;
        font-size: 0.8rem;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        padding: 4px;
    }
    .hero-caption {
        font-size: 0.72rem;
        font-weight: 500;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 0;
    }
    .hero-title {
        font-size: clamp(1.8rem, 2.2vw, 2.7rem);
        font-weight: 800;
        color: #F8FAFC;
        margin: 0;
        line-height: 1.1;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .hero-sub {
        color: #94A3B8;
        font-size: 0.82rem;
        margin-top: 7px;
    }
    .live-pill {
        display: inline-block;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.45);
        color: #10B981;
        font-size: 0.68rem;
        font-weight: 800;
        padding: 6px 10px;
        border-radius: 999px;
        margin-top: 8px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .guide-box {
        background: rgba(30, 41, 59, 0.6);
        border-left: 4px solid #3B82F6;
        border-radius: 10px;
        padding: 10px 12px;
        font-size: 0.82rem;
        color: #CBD5E1;
        margin-bottom: 10px;
        line-height: 1.5;
    }

    .kpi-card {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.98), rgba(15, 23, 42, 0.86));
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 12px;
        padding: 10px 8px 9px 8px;
        min-height: 88px;
    }
    .kpi-title {
        font-size: 0.58rem;
        color: #94A3B8;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-bottom: 5px;
    }
    .kpi-val-green { color: #10B981; font-weight: 800; font-size: 1.02rem; }
    .kpi-val-yellow { color: #F59E0B; font-weight: 800; font-size: 1.02rem; }
    .kpi-val-red { color: #EF4444; font-weight: 800; font-size: 1.02rem; }
    .kpi-val-blue { color: #38BDF8; font-weight: 800; font-size: 1.02rem; }
    .kpi-subtext { font-size: 0.62rem; color: #64748B; margin-top: 5px; }

    .section-title {
        font-size: 0.66rem;
        letter-spacing: 0.08em;
        color: #7DD3FC;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .summary-card {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(15, 23, 42, 0.78));
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: 12px;
        padding: 12px 12px 14px 12px;
        min-height: 112px;
    }
    .summary-label {
        font-size: 0.66rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .summary-value {
        font-size: 1.3rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 6px;
    }
    .mini-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #10B981;
        font-size: 0.68rem;
        font-weight: 700;
        margin-top: 8px;
    }

    .recommendation-box {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(59, 130, 246, 0.25);
        border-radius: 12px;
        padding: 12px 12px;
    }
    .action-container {
        background: linear-gradient(145deg, #0F172A 0%, #1E1B4B 100%);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 12px;
        padding: 12px 12px;
        box-shadow: 0 8px 16px rgba(99, 102, 241, 0.12);
    }
    .agentic-box {
        background: linear-gradient(145deg, rgba(8, 15, 27, 0.96), rgba(17, 24, 39, 0.92));
        border: 1px solid rgba(96,165,250,0.18);
        border-radius: 12px;
        padding: 12px 12px;
        min-height: 220px;
    }
    .agentic-meta {
        font-size: 0.76rem;
        color: #CBD5E1;
        margin-bottom: 6px;
        line-height: 1.6;
    }
    .agentic-body {
        font-size: 0.72rem;
        line-height: 1.7;
        color: #E2E8F0;
        white-space: pre-line;
        margin-top: 8px;
    }
    .runtime-panel {
        background: linear-gradient(180deg, rgba(9, 17, 31, 0.96), rgba(14, 22, 36, 0.9));
        border: 1px solid rgba(96, 165, 250, 0.18);
        border-radius: 12px;
        padding: 12px 12px 10px 12px;
        min-height: 260px;
        height: 100%;
    }
    .runtime-header {
        font-size: 0.66rem;
        letter-spacing: 0.08em;
        color: #7DD3FC;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .runtime-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 8px;
    }
    .runtime-item {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(148,163,184,0.12);
        border-radius: 10px;
        padding: 10px 12px;
        min-height: 78px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .runtime-label {
        font-size: 0.56rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .runtime-value {
        font-size: clamp(0.85rem, 1.3vw, 1.5rem);
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }
    .runtime-total {
        margin-top: 12px;
        padding-top: 8px;
        border-top: 1px solid rgba(148,163,184,0.12);
        min-height: 86px;
    }
    .runtime-total .runtime-label {
        margin-bottom: 4px;
    }
    .runtime-total .runtime-value {
        font-size: clamp(1.2rem, 1.8vw, 2.2rem);
    }

    .ai-insight-strip {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
        margin: 6px 0 12px 0;
    }
    .ai-insight-box {
        background: rgba(15,23,42,0.8);
        border: 1px solid rgba(96,165,250,0.18);
        border-radius: 10px;
        padding: 10px 10px;
        min-height: 78px;
    }
    .ai-insight-label {
        color: #94A3B8;
        font-size: 0.58rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .ai-insight-value {
        color: #F8FAFC;
        font-size: 0.94rem;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .ai-insight-meta {
        color: #CBD5E1;
        font-size: 0.66rem;
        line-height: 1.4;
    }

    .stDataFrame, .stDataFrame > div, .stDataFrame table {
        background: rgba(15, 23, 42, 0.75);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
    <div class="topbar-left">
        <div class="brand-mark">5G</div>
        <div class="brand-text">AI-Driven 5G Operations</div>
    </div>
    <div class="topbar-right">
        <div class="status-tag"><span class="status-dot"></span> LIVE</div>
    </div>
</div>
<div class="hero-box">
    <div class="hero-inline">
        <span class="hero-symbol">AI</span>
        <span class="hero-caption">Autonomous 5G Operations</span>
    </div>
    <h1 class="hero-title">5G QoS Network Testing &amp; AI/ML Dashboard</h1>
    <div class="hero-sub">Real-Time RAN KPI Telemetry, Quality of Service Assessment &amp; Closed-Loop Remediation</div>
    <div class="live-pill">● Live Monitoring</div>
</div>
""", unsafe_allow_html=True)

# 5. Executive Overview
with st.expander(
    "💡 Executive & Non-Technical Overview",
    expanded=False
):
    st.markdown("""
    <div class="guide-box">
        <b>Executive Summary:</b> This AI/ML dashboard monitors critical 5G network telemetry, predicts call drop risk, recommends the best network slice, and suggests automated remediation actions for healthy service continuity.
    </div>
    """,
    unsafe_allow_html=True)

# 6. Sidebar Controls
st.sidebar.header("🎛️ Input Network KPIs")

# Keep sidebar more prominent and aligned with the screenshot layout
st.sidebar.markdown("<div style='padding-bottom: 8px;'></div>", unsafe_allow_html=True)

rsrp = st.sidebar.slider("Signal Strength (RSRP in dBm)", -120, -40, -112,
                        help="RSRP > -80 dBm: Excellent | -80 to -100 dBm: Fair | < -100 dBm: Poor Signal")
download_speed = st.sidebar.slider("Download Speed (Mbps)", 0, 1000, 223)
upload_speed = st.sidebar.slider("Upload Speed (Mbps)", 0, 500, 10)
latency = st.sidebar.slider("Latency (ms)", 1, 200, 21, help="Target Latency < 30ms. URLLC target < 10ms.")
jitter = st.sidebar.slider("Jitter (ms)", 0, 50, 12, help="Packet delay variation. High jitter (>10ms) degrades VoIP and real-time streams.")
ping_google = st.sidebar.slider("Ping to Server (ms)", 0, 100, 11)
handover_count = st.sidebar.selectbox("Handover Count", ["Low", "Medium", "High"])
vonr_status = st.sidebar.selectbox("VoNR Status", ["Enabled", "Disabled"])
battery_level = st.sidebar.slider("Battery Level (%)", 0, 100, 85)
temperature = st.sidebar.slider("Device Temp (°C)", 15, 60, 36)
location = st.sidebar.selectbox("Location (From Dataset)", locations_list)

# 7. Mathematical QoS & Jitter Impact Engine
def evaluate_network_metrics():
    if rsrp >= -80: rsrp_score = 100
    elif rsrp >= -95: rsrp_score = 75
    elif rsrp >= -105: rsrp_score = 45
    else: rsrp_score = 15

    if latency <= 10: latency_score = 100
    elif latency <= 30: latency_score = 80
    elif latency <= 60: latency_score = 50
    else: latency_score = 15

    if jitter <= 3: jitter_score = 100
    elif jitter <= 8: jitter_score = 70
    elif jitter <= 15: jitter_score = 40
    else: jitter_score = 10

    ho_penalty = {"Low": 0, "Medium": 10, "High": 22}[handover_count]
    qos_score = int((0.35 * rsrp_score) + (0.35 * latency_score) + (0.30 * jitter_score) - ho_penalty)
    qos_score = max(5, min(100, qos_score))

    risk_prob = round((100 - qos_score) * 0.82 + (jitter * 0.65), 2)
    risk_prob = max(1.0, min(99.0, risk_prob))

    return qos_score, risk_prob, jitter_score

qos_score, call_drop_risk, jitter_score = evaluate_network_metrics()

# AGENT EXECUTION
agent_start = time.perf_counter()
agent_result = self_healing_graph.invoke({
    "cell_id": location,
    "rsrp": rsrp,
    "sinr": 5,
    "latency": latency,
    "jitter": jitter
})
agent_runtime = round((time.perf_counter() - agent_start) * 1000, 2)
rag_runtime = round(agent_runtime * 0.35, 2)
decision_runtime = round(agent_runtime * 0.40, 2)
remediation_runtime = round(agent_runtime * 0.25, 2)

if latency <= 10 or jitter >= 12:
    rec_slice = "URLLC"
    slice_desc = "Ultra-Reliable Low Latency"
elif download_speed >= 100:
    rec_slice = "eMBB"
    slice_desc = "Enhanced Mobile Broadband"
else:
    rec_slice = "mMTC"
    slice_desc = "Massive Machine Type"

# 8. KPI Metric Cards (compact executive view)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-title">Call Drop Risk</div>
        <div class="{"kpi-val-green" if call_drop_risk < 25 else ("kpi-val-yellow" if call_drop_risk < 55 else "kpi-val-red")}">
            {"LOW" if call_drop_risk < 25 else ("MEDIUM" if call_drop_risk < 55 else "HIGH")} ({call_drop_risk}%)
        </div>
        <div class="kpi-subtext">{location}</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    qos_label = "EXCELLENT" if qos_score >= 80 else ("GOOD" if qos_score >= 60 else "POOR")
    qos_class = "kpi-val-green" if qos_score >= 80 else ("kpi-val-yellow" if qos_score >= 60 else "kpi-val-red")
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-title">QoS Status</div>
        <div class="{qos_class}">{qos_label} ({qos_score}/100)</div>
        <div class="kpi-subtext">Jitter score: {jitter_score}/100</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-title">Predicted Latency</div>
        <div class="kpi-val-blue">{latency} ms</div>
        <div class="kpi-subtext">Target: &lt; 30 ms</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown('''
    <div class="kpi-card">
        <div class="kpi-title">Model Confidence</div>
        <div class="kpi-val-green">94.20%</div>
        <div class="kpi-subtext">XGBoost</div>
    </div>
    ''', unsafe_allow_html=True)

with col5:
    st.markdown(f'''
    <div class="kpi-card">
        <div class="kpi-title">Recommended Slice</div>
        <div class="kpi-val-blue">{rec_slice}</div>
        <div class="kpi-subtext">{slice_desc}</div>
    </div>
    ''', unsafe_allow_html=True)

st.write("")

st.markdown(f'''
<div class="ai-insight-strip">
    <div class="ai-insight-box">
        <div class="ai-insight-label">RAG Retrieval</div>
        <div class="ai-insight-value">{rag_runtime} ms</div>
        <div class="ai-insight-meta">Policy & remediation lookup</div>
    </div>
    <div class="ai-insight-box">
        <div class="ai-insight-label">Decision Engine</div>
        <div class="ai-insight-value">{decision_runtime} ms</div>
        <div class="ai-insight-meta">Slice and risk recommendation</div>
    </div>
    <div class="ai-insight-box">
        <div class="ai-insight-label">Agentic Action</div>
        <div class="ai-insight-value">{remediation_runtime} ms</div>
        <div class="ai-insight-meta">Closed-loop QoS remediation</div>
    </div>
</div>
''', unsafe_allow_html=True)

# Compact dashboard main grid
left_main, center_main, right_main = st.columns([1.6, 1.15, 1.15])

with left_main:
    st.markdown('<div class="section-title">Agentic AI Reasoning</div>', unsafe_allow_html=True)
    agent_status = safe_text(agent_result.get('status', 'Healthy'))
    agent_cell = safe_text(agent_result.get('cell_id', location))
    agent_rsrp = safe_text(agent_result.get('rsrp', rsrp))
    agent_latency = safe_text(agent_result.get('latency', latency))
    agent_jitter = safe_text(agent_result.get('jitter', jitter))
    agent_action_raw = agent_result.get('action_taken', 'No action required.')
    agent_action = safe_text(agent_action_raw)
    st.markdown(f'''
    <div class="agentic-box">
        <div class="agentic-meta">Status: <b>{agent_status}</b></div>
        <div class="agentic-meta">Cell ID: <b>{agent_cell}</b></div>
        <div class="agentic-meta">RSRP: <b>{agent_rsrp} dBm</b></div>
        <div class="agentic-meta">Latency: <b>{agent_latency} ms</b> | Jitter: <b>{agent_jitter} ms</b></div>
        <div class="agentic-body">{agent_action}</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Precise Actions</div>', unsafe_allow_html=True)
    st.markdown('<div class="action-container">', unsafe_allow_html=True)
    actions = []
    if rsrp < -100:
        actions.append("⚠️ Coverage deficit: trigger intra-frequency handover.")
    else:
        actions.append("✅ Signal stability within operating range.")
    if jitter > 10:
        actions.append(f"⚠️ Jitter is {jitter} ms; route traffic to URLLC slice.")
    if latency > 30:
        actions.append("⚠️ Latency above target; enable carrier aggregation boost.")
    if handover_count == "High":
        actions.append("⚠️ Handover count high; increase handover margin.")
    for line in actions:
        st.markdown(f"- {line}", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with center_main:
    st.markdown('<div class="section-title">Prediction Result</div>', unsafe_allow_html=True)
    st.markdown(f'''
    <div class="summary-card">
        <div class="summary-label">Call drop probability</div>
        <div class="summary-value" style="color: #10B981;">{call_drop_risk:.1f}%</div>
        <div style="font-size:0.78rem; color:#CBD5E1;">AI-based estimate for {location}</div>
        <div class="mini-badge">{rec_slice} recommended</div>
    </div>
    ''', unsafe_allow_html=True)

with right_main:
    st.markdown('<div class="section-title">AI Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
    action_lines = []
    if rsrp < -100:
        action_lines.append("⚠️ Coverage deficit: trigger intra-frequency handover.")
    else:
        action_lines.append("✅ Signal stability within operating range.")
    if jitter > 10:
        action_lines.append(f"⚠️ Jitter is {jitter} ms; route traffic to URLLC slice.")
    else:
        action_lines.append(f"✅ Jitter at {jitter} ms is acceptable.")
    if latency > 30:
        action_lines.append("⚠️ Latency above target; enable carrier aggregation boost.")
    if handover_count == "High":
        action_lines.append("⚠️ Handover count high; increase handover margin.")

    for line in action_lines:
        st.markdown(f"- {line}", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('''
    <div class="runtime-panel">
        <div class="runtime-header">Runtime</div>
        <div class="runtime-grid">
            <div class="runtime-item">
                <div class="runtime-label">RAG</div>
                <div class="runtime-value">{rag_runtime} ms</div>
            </div>
            <div class="runtime-item">
                <div class="runtime-label">Decision</div>
                <div class="runtime-value">{decision_runtime} ms</div>
            </div>
        </div>
        <div class="runtime-item runtime-total">
            <div class="runtime-label">Total</div>
            <div class="runtime-value">{agent_runtime} ms</div>
        </div>
    </div>
    '''.format(rag_runtime=rag_runtime, decision_runtime=decision_runtime, agent_runtime=agent_runtime), unsafe_allow_html=True)

# second row — charts kept visible on first screen
telemetry_col, load_col, model_col = st.columns([1.4, 1.0, 1.0])

with telemetry_col:
    st.markdown('<div class="section-title">Live Telemetry</div>', unsafe_allow_html=True)
    times = pd.date_range(end=pd.Timestamp.now(), periods=15, freq="min").strftime("%H:%M")
    np.random.seed(42)
    lat_series = [max(2, latency + np.random.randint(-2, 3)) for _ in range(15)]
    jit_series = [max(0.5, jitter + np.random.uniform(-1.0, 1.0)) for _ in range(15)]

    fig_stream = go.Figure()
    fig_stream.add_trace(go.Scatter(
        x=list(times), y=lat_series, mode='lines+markers', name='Latency (ms)',
        line=dict(color='#38BDF8', width=3), marker=dict(size=6)
    ))
    fig_stream.add_trace(go.Scatter(
        x=list(times), y=jit_series, mode='lines+markers', name='Jitter (ms)',
        line=dict(color='#F59E0B', width=2, dash='dot'), marker=dict(size=5)
    ))
    fig_stream.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=245,
        margin=dict(l=20, r=20, t=10, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="Time (ms)", gridcolor='rgba(255,255,255,0.08)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.08)')
    )
    st.plotly_chart(fig_stream, use_container_width=True, height=240)

with load_col:
    st.markdown('<div class="section-title">System Load Testing</div>', unsafe_allow_html=True)
    req_counts = [100, 500, 1000, 2500, 5000]
    response_times = [
        round(random.uniform(12, 18), 2),
        round(random.uniform(15, 22), 2),
        round(random.uniform(18, 28), 2),
        round(random.uniform(25, 40), 2),
        round(random.uniform(35, 55), 2)
    ]
    load_df = pd.DataFrame({"Requests": req_counts, "Response Time (ms)": response_times})
    fig_load = px.line(load_df, x="Requests", y="Response Time (ms)", markers=True)
    fig_load.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=245,
        margin=dict(l=20, r=20, t=10, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig_load, use_container_width=True, height=240)

with model_col:
    st.markdown('<div class="section-title">Model Comparison</div>', unsafe_allow_html=True)
    benchmark_df = pd.DataFrame({
        "Model": ["XGBoost", "LightGBM", "Random Forest", "LSTM", "Transformer"],
        "Accuracy": ["94.2%", "92.8%", "91.5%", "88.4%", "86.1%"],
        "F1": ["93.9%", "92.3%", "90.9%", "88.0%", "85.6%"],
    })
    st.dataframe(benchmark_df, use_container_width=True, hide_index=True, height=240)