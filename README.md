# 5G QoS Network Intelligence Dashboard

## 📱 Project Overview

A **Streamlit-based AI/ML dashboard** for predicting and analyzing **5G Quality of Service (QoS)** metrics. The application provides real-time predictions for network performance, call drop risk assessment, and KPI impact analysis using machine learning models.

### Key Features
- 🎯 **AI-Powered QoS Prediction** – Real-time network QoS status prediction
- 📊 **Interactive KPI Dashboard** – Visual analysis of network KPIs and their impact
- 🚨 **Call Drop Risk Assessment** – Predicts call drop risk (LOW/MEDIUM/HIGH)
- 📈 **Model Performance Metrics** – Compares multiple ML models (RF, XGBoost, LSTM, GRU, Transformer)
- 🎨 **Dark Theme UI** – Modern neon-styled dashboard interface
- ⚡ **Real-time Adjustments** – Live slider-based parameter tuning

---

## 📋 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum
- **Storage**: 500MB minimum

### Python Dependencies
All dependencies are listed in `requirements.txt`:

```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.15.0
scikit-learn>=1.3.0
joblib>=1.3.0
```

---

## 🚀 Installation & Setup

### Step 1: Clone or Navigate to Project Folder

```bash
cd "C:\Users\ad\Desktop\3rd sem\PRJ-Mini project"
```

### Step 2: Create & Activate Virtual Environment

**On Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS/Linux (Bash):**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Or Install Individually:**

```bash
pip install streamlit pandas numpy plotly scikit-learn joblib
```

### Step 4: Verify Installation

```bash
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')"
```

---

## 📂 Project Structure

```
PRJ-Mini project/
│
├── app.py                          # Main Streamlit application
├── README.md                       # This file
├── requirements.txt                # Python dependencies
│
├── colab_data/                     # Pre-trained models & data
│   ├── best_ml_model.pkl          # ML model (serialized)
│   ├── scaler.pkl                 # Feature scaler (serialized)
│   ├── 5g_network_data.csv        # 5G network dataset
│   ├── lstm_model.h5              # LSTM model
│   ├── gru_model.h5               # GRU model
│   └── logs.txt                   # Model training logs
│
└── .venv/                          # Virtual environment (created after setup)
```

---

## ▶️ Running the Project

### Method 1: Simple Start (Recommended)

```bash
streamlit run app.py
```

### Method 2: With Explicit Python & Port

```bash
python -m streamlit run app.py --server.port 8501
```

### Method 3: With Full Configuration

```bash
streamlit run app.py --server.port 8501 --logger.level=info --client.showErrorDetails=true
```

**Output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## 🌐 Accessing the Dashboard

1. **After running the app**, open your browser
2. Go to: **http://localhost:8501**
3. Dashboard loads automatically with default values

### Dashboard Components

| Component | Purpose |
|-----------|---------|
| **Sidebar Input Panel** | Adjust RAN KPIs (Signal, Speed, Latency, Jitter, Network Type) |
| **QoS Metrics Card** | Real-time QoS status, Model confidence, UX score |
| **Call Drop Risk Badge** | Visual risk indicator (Green/Yellow/Red) |
| **KPI Impact Chart** | Horizontal bar chart showing impact on call drop |
| **Model Comparison Table** | Performance metrics of different ML models |

---

## 🎛️ How to Use the Dashboard

### 1. **Adjust RAN KPIs** (Left Sidebar)
- **Signal Strength**: -120 to -50 dBm
- **Download Speed**: 0-1000 Mbps
- **Upload Speed**: 0-500 Mbps
- **Latency**: 0-200 ms
- **Jitter**: 0-100 ms
- **Network Type**: 5G NSA or 5G SA

### 2. **Click "🚀 Predict QoS"** Button
- Triggers ML model prediction
- Displays predicted QoS status
- Shows model confidence percentage
- Calculates UX score and call drop risk

### 3. **View Results**
- **QoS Status**: GOOD or POOR
- **User Experience Score**: 0-100
- **Call Drop Risk**: LOW, MEDIUM, or HIGH (color-coded)
- **Top KPI Impacts**: Visual ranking of KPI importance

### 4. **Review Model Performance**
- Table shows accuracy and F1-scores
- Compares 5 different ML models
- Identifies best-performing model

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install streamlit
```

### Issue: "FileNotFoundError: colab_data/best_ml_model.pkl"

**Solution:**
- Ensure `colab_data/` folder exists in project directory
- Verify model files are present:
  - `best_ml_model.pkl`
  - `scaler.pkl`

### Issue: "Port 8501 already in use"

**Solution:**
```bash
streamlit run app.py --server.port 8502
```
(Replace 8502 with any available port)

### Issue: Dashboard shows "Script execution error"

**Solution:**
1. Check Python version: `python --version` (should be 3.8+)
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Restart the Streamlit app

### Issue: Slow performance or crashes

**Solution:**
- Close other applications to free RAM
- Clear Streamlit cache: `streamlit cache clear`
- Reduce dataset size if loading large CSV files

---

## 📊 Key Model Information

### Supported ML Models
| Model | Accuracy | F1-Score | Type |
|-------|----------|----------|------|
| Random Forest | 92.1% | 91.8% | Tree-based |
| XGBoost | 93.4% | 93.1% | Boosting |
| LSTM | 94.68% | 94.67% | Deep Learning (Sequential) |
| GRU | 94.68% | 94.67% | Deep Learning (Recurrent) |
| Transformer | 96.2% | 96.0% | Deep Learning (Attention) |

### Features Used

The model uses **12 features**:
1. Signal Strength (dBm)
2. Download Speed (Mbps)
3. Upload Speed (Mbps)
4. Latency (ms)
5. Jitter (ms)
6. Network Type (5G NSA=0, 5G SA=1)
7. Hour (Time feature)
8. Day (Time feature)
9. Month (Time feature)
10. Weekday (Time feature)
11. Peak Hour (Binary)
12. Weekend (Binary)

---

## 📝 Environment Variables (Optional)

To customize Streamlit behavior, create a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#4f46e5"
backgroundColor = "#070B14"
secondaryBackgroundColor = "#1e293b"
textColor = "#e2e8f0"
font = "sans serif"

[server]
port = 8501
headless = false
runOnSave = true

[logger]
level = "info"
```

---

## 🛑 Stopping the App

Press **Ctrl + C** in the terminal where Streamlit is running.

---

## 📞 Project Details

- **Project Type**: Telecom AI/ML Dashboard
- **Framework**: Streamlit + Plotly
- **Data Source**: 5G Network CSV dataset
- **Models**: Scikit-Learn, TensorFlow/Keras
- **Python Version**: 3.8+

---

## 📌 Important Notes

✅ **Before First Run:**
- Ensure all files in `colab_data/` are present
- Verify Python 3.8+ is installed
- Create virtual environment for isolation

✅ **Performance Tips:**
- Dashboard automatically caches predictions
- Use `--logger.level=error` to reduce console output
- Close browser tabs to reduce memory usage

✅ **Data Privacy:**
- Models are trained and stored locally
- No data is sent to external servers
- CSV data stays within project folder

---

## 🎓 Learning Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Documentation**: https://plotly.com/python
- **Scikit-Learn**: https://scikit-learn.org
- **5G QoS Concepts**: https://www.3gpp.org

---

## 📄 License

This project is for educational and research purposes.

---

## ✅ Verification Checklist

Before reporting issues, verify:

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] All dependencies installed: `pip list | grep streamlit`
- [ ] `colab_data/` folder exists with model files
- [ ] Port 8501 is not in use
- [ ] No firewall blocking localhost:8501

---

## 🚀 Quick Start Command (One-Liner)

**Windows PowerShell:**
```powershell
cd "C:\Users\ad\Desktop\3rd sem\PRJ-Mini project"; .\.venv\Scripts\Activate.ps1; streamlit run app.py
```

**macOS/Linux:**
```bash
cd ~/PRJ-Mini\ project && source .venv/bin/activate && streamlit run app.py
```

---

**Happy Testing! 🎯📡**

For issues or questions, ensure all steps above are followed correctly.
