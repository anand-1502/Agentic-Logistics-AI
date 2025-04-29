# 🚛 Agentic Logistics AI

Agentic Logistics AI is a **supply chain risk scoring** and **shipment intelligence platform** that lets users upload their shipment data, dynamically analyze risks using AI, visualize risk distributions, and download enhanced datasets — with a clean and professional dashboard UI.

---

## 🧠 Problem Statement

In modern supply chains, logistics managers often lack **real-time insights** into shipment risks caused by delays, ratings, operational issues, and external factors.  
There is no easy way to **analyze**, **score**, and **act** on shipment risks dynamically before they escalate into major supply chain disruptions.

---

## 💡 Solution

Agentic Logistics AI provides an intuitive platform where:
- Users can **upload shipment data** easily.
- AI dynamically **analyzes shipment risk** based on important features.
- Risk levels are **visualized** interactively through dashboards.
- Results are **downloadable** for further operational use.
- The system is **future-ready** with integrations for **weather** and **news data** to make the model even smarter.

---

## ⚙️ How the System Works

1. **Upload shipment data** through a streamlined UI.
2. **Select risk columns** that influence risk scoring.
3. **Run the AI agent** to predict and score shipment risks.
4. **View interactive visualizations** (pie and bar charts).
5. **Download** the enriched, risk-scored dataset.

---

## 🛠️ Project Structure

agentic_logistics_ai/ 
│
├── app/ # Backend FastAPI application 
|     │ 
|     ├── init.py # Initialization file 
|     │ 
|     ├── agent.py # Core AI risk scoring logic 
|     │ 
|     ├── database.py # SQLite database operations 
|     │ 
|     ├── main.py # Starts FastAPI server 
|     │ 
|     ├── routes.py # API routes for frontend to interact with backend 
|     │ 
|     ├── news_api.py # (Future) News API integration 
|     ├── weather_api.py # (Future) Weather API integration 
│ 
├── data/ # Example data and database 
|     │ 
|     ├── shipments.db # SQLite database storing shipment records 
|     │ 
|     ├── Train.csv # Full dataset 
|     │ 
|     ├── Train_small.csv # Small sample dataset 
├── frontend/ # Streamlit dashboard UI 
|     ├── dashboard.py # Frontend Streamlit app 
|     │ 
|     ├── bg.jpg # Background image for UI 
|     │ 
|     ├── documentation/ # Screenshots and diagrams 
|           │     
|           ├── one.png 
|           │ 
|           ├── two.png 
|           │ 
|           ├── three.png 
|           │ 
|           ├── four.png
│           │ 
|           ├──system_diagram.png # System architecture diagram 
├── scripts/ # (Reserved for future utility scripts) 
├── .env # Environment variables 
├── Dockerfile # Docker container setup 
├── main.py # Backend entrypoint (FastAPI) 
├── requirements.txt # Python dependency list 
├── README.md # This file


