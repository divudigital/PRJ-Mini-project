# AI/ML-Based 5G QoS Monitoring and Agentic Self-Healing Framework

## Project Overview

This project presents a prototype framework for monitoring 5G network Quality of Service (QoS), assessing connection-drop risk, identifying potential network issues, and recommending remediation actions through an agentic workflow.

It combines machine-learning-based analysis with rule-based KPI monitoring, Retrieval-Augmented Generation (RAG), and LangGraph orchestration. A Streamlit dashboard provides an interactive interface for exploring network conditions and reviewing the agent's analysis and recommended actions.

**Project positioning:** An integrated prototype for explainable 5G QoS monitoring and simulated self-healing.

## Key Features

- **5G QoS Monitoring:** Analyze network KPIs such as signal strength, latency, and jitter.
- **ML-Based Risk Assessment:** Use the available trained classification model to assess dropped-connection risk.
- **Interactive Dashboard:** Explore network conditions and view analysis through Streamlit.
- **Agentic Workflow:** Orchestrate monitoring, knowledge retrieval, root-cause analysis, and remediation recommendations.
- **RAG Knowledge Retrieval:** Retrieve relevant context from the local telecom knowledge base using FAISS.
- **Simulated Remediation:** Demonstrate proposed network actions through application-level tools.
- **Docker Deployment:** Build and run the dashboard in a containerized environment.

## System Architecture

1. **Dashboard Layer – `app.py`**
   Accepts network KPI inputs and presents QoS analysis, risk information, and agent responses.

2. **Agent Orchestration – `agent.py`**
   Coordinates the monitoring and remediation workflow using LangGraph.

3. **Knowledge Retrieval – `retriever.py`**
   Retrieves relevant telecom information from the local FAISS knowledge index.

4. **Knowledge Base – `ragdata/`**
   Contains telecom rules, network policies, and remediation playbook information.

5. **Action Layer – `tools.py`**
   Demonstrates proposed remediation operations through simulated application-level actions.

6. **Dataset Processing – `main.py`**
   Provides the dataset-oriented execution path.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Dashboard | Streamlit, Plotly |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost, LightGBM |
| Agent Orchestration | LangGraph, LangChain |
| Retrieval | FAISS |
| Deployment | Docker |

## Project Structure

```text
PRJ-Mini-project/
│
├── app.py
├── agent.py
├── retriever.py
├── tools.py
├── main.py
├── test_agent.py
├── test_rag.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── IMPLEMENTED_FEATURES.md
│
├── ragdata/
│   ├── 3gpp_rules.txt
│   ├── network_policies.txt
│   └── remediation_playbook.txt
│
├── faiss_index/
│   ├── index.faiss
│   └── index.pkl
│
└── colab_data/
    └── Local model and dataset artifacts
```

*Note: The exact contents of `colab_data/` depend on the local project setup. Model artifacts are excluded from GitHub and may need to be supplied separately.*

## Workflow

```text
Network KPI Inputs
        |
        v
Streamlit Dashboard
        |
        v
QoS Monitoring and Risk Assessment
        |
        v
LangGraph Agent Workflow
        |
        v
Telecom Knowledge Retrieval (RAG)
        |
        v
Root-Cause Analysis
        |
        v
Remediation Recommendation
        |
        v
Simulated Action Execution
        |
        v
Dashboard Result
```

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/divudigital/PRJ-Mini-project.git
cd PRJ-Mini-project
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Verify required local artifacts

Ensure the required model files, dataset files, and FAISS index are available in their expected directories. These artifacts are not necessarily included in the public repository.

### 5. Run the dashboard

```powershell
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Docker Deployment

Build the Docker image from the project directory:

```powershell
docker build -t qos-agent:latest .
```

Run the container:

```powershell
docker run -d --name qos-agent-updated -p 8501:8501 qos-agent:latest
```

Check running containers:

```powershell
docker ps
```

View application logs:

```powershell
docker logs qos-agent-updated
```

Open the dashboard:

```text
http://localhost:8501
```

Stop the container:

```powershell
docker stop qos-agent-updated
```

## Testing

The project includes test scripts for the agent workflow and RAG retrieval:

```powershell
python test_rag.py
python test_agent.py
```

These tests help verify knowledge retrieval and the agent's response workflow. They should not be interpreted as proof of live telecom-network integration.

## Important Implementation Scope

- QoS assessment and threshold-based monitoring are application-level prototype logic.
- ML classification and rule-based KPI assessment are distinct components.
- RAG retrieves information from the configured local knowledge base.
- Remediation actions are simulated through application-level tools.
- The project does not directly reconfigure live 5G network infrastructure.
- Thresholds used in the prototype should be interpreted in the context of the implemented configuration and dataset.

## Future Enhancements

- Integrate with authorized network telemetry and orchestration APIs.
- Evaluate the framework using larger and more diverse 5G network datasets.
- Add systematic agent evaluation, response-quality checks, and failure analysis.
- Measure individual workflow-stage latency and evaluate performance under concurrent dashboard usage.

## Repository

GitHub: https://github.com/divudigital/PRJ-Mini-project

**Project purpose:** Academic and research prototype for 5G QoS monitoring, explainable analysis, and simulated agentic remediation.