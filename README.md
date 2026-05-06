# 📊 Sales Forecasting System (End-to-End)

## 🚀 Overview
This project is an end-to-end time series forecasting system that predicts next 8 weeks of sales for each state.

## 🔥 Features
- Multiple models: ARIMA, Prophet, XGBoost
- Automatic model selection
- Feature engineering (lag, rolling stats, time features)
- REST API using FastAPI
- Interactive dashboard using Streamlit

## 🧠 Models Used
- ARIMA / SARIMA
- Facebook Prophet
- XGBoost (with lag features)

## ⚙️ Tech Stack
- Python
- FastAPI
- Streamlit
- Pandas, NumPy
- XGBoost, Prophet, Statsmodels

## 📂 Project Structure
## ▶️ Run Project

### 1. Install dependencies
```bash
pip install -r requirements.txt
2. Train models
python src/train.py
3. Run API
uvicorn api.app:app --reload
4. Run Dashboard
streamlit run dashboard.py
