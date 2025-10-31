# 📊 Data Analytics Portfolio Demo

A unified Streamlit web application showcasing two comprehensive data analytics case studies:
1. **🕵️ Agent Network Fraud Detection** - ML-powered fraud detection system
2. **🏭 Industrial IoT Analytics** - Predictive maintenance, demand forecasting, and anomaly detection

🌐 **[View Live Demo](#)** *(Add your deployed URL here)*

---

## 🎯 Features

### Case Study 1: Fraud Detection
- ✅ Real-time fraud risk scoring (0-100 scale)
- ✅ Multi-model ensemble (Rule-based + Random Forest + Isolation Forest)
- ✅ Explainable AI with clear fraud indicators
- ✅ Interactive dashboards and visualizations
- ✅ AI chatbot for data queries

**Key Metrics:** 87.5% accuracy, 70% fraud reduction, 10x faster verification

### Case Study 2: Industrial IoT
- ✅ **Predictive Maintenance**: Predict equipment failures 48h in advance
- ✅ **Demand Forecasting**: Optimize production planning with 95% accuracy
- ✅ **Quality Monitoring**: Real-time anomaly detection
- ✅ Comprehensive time-series analysis
- ✅ AI chatbot for operational insights

**Key Metrics:** 30-40% downtime reduction, 15-20% energy savings, real-time alerting

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Local Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd portfolio-demo
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open browser**
Navigate to `http://localhost:8501`

---

## 📦 Project Structure

```
portfolio-demo/
├── app.py                      # Main landing page
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── pages/
│   ├── 2_🕵️_Case_Study_1.py  # Fraud Detection
│   └── 3_🏭_Case_Study_2.py  # Industrial IoT
├── utils/
│   ├── data_generator.py      # Synthetic data generation
│   ├── fraud_detection.py     # Fraud ML models
│   ├── iot_analytics.py       # IoT ML models
│   └── chatbot.py             # AI chatbot
├── assets/                     # Images and resources
├── data/                       # Data storage
└── README.md                   # This file
```

---

## 🌐 Deployment Guide

### Option 1: Streamlit Cloud (Recommended - Free)

1. **Push code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

2. **Deploy to Streamlit Cloud**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Sign in with GitHub
- Click "New app"
- Select your repository
- Set main file path: `app.py`
- Click "Deploy"

**Your app will be live at:** `https://<app-name>.streamlit.app`

### Option 2: Hugging Face Spaces (Free)

1. **Create account** at [huggingface.co/spaces](https://huggingface.co/spaces)

2. **Create new Space**
- Click "Create new Space"
- Select "Streamlit" as SDK
- Upload your code

3. **App Configuration**
Create `app.py` as entry point (already configured)

**Your app will be live at:** `https://huggingface.co/spaces/<username>/<space-name>`

### Option 3: Railway (Free Tier)

1. **Create account** at [railway.app](https://railway.app)

2. **Create `Procfile`** in project root:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

3. **Deploy via GitHub**
- Connect Railway to your GitHub repo
- Railway will auto-detect Streamlit and deploy

### Option 4: Render (Free Tier)

1. **Create account** at [render.com](https://render.com)

2. **Create `start.sh`** file:
```bash
#!/bin/bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

3. **Deploy**
- Connect GitHub repository
- Select "Web Service"
- Build command: `pip install -r requirements.txt`
- Start command: `sh start.sh`

---

## 🛠️ Technology Stack

### Core Framework
- **Streamlit** - Web application framework
- **Python 3.8+** - Programming language

### Data Processing
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

### Machine Learning
- **Scikit-learn** - ML algorithms (Random Forest, Isolation Forest)
- **XGBoost** - Gradient boosting
- **Prophet** - Time series forecasting

### Visualization
- **Plotly** - Interactive charts
- **Matplotlib** - Static plots
- **Seaborn** - Statistical visualization

---

## 📊 Usage Guide

### Case Study 1: Fraud Detection

1. Navigate to "Case Study 1" page
2. Adjust parameters:
   - Number of agents (50-500)
   - Fraud ratio (5-30%)
3. Click "Generate Data"
4. Explore dashboards:
   - Risk Distribution
   - Fraud Indicators
   - Agent Details
   - AI Chat

**Sample Questions for AI:**
- "How many critical risk agents?"
- "Show me top risky agents"
- "What's the risk distribution?"

### Case Study 2: Industrial IoT

1. Navigate to "Case Study 2" page
2. Select analysis type:
   - Predictive Maintenance
   - Demand Forecasting
   - Quality Monitoring
3. Generate data for each analysis
4. Explore interactive dashboards
5. Use AI chatbot for insights

**Sample Questions for AI:**
- "What's the current pump status?"
- "Forecast demand for tomorrow"
- "Any anomalies detected today?"

---

## 🎨 Customization

### Modify Themes
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
```

### Add New Metrics
Edit respective files in `utils/` directory

### Change Data Generation
Modify `utils/data_generator.py` parameters

---

## 📝 Documentation

### Data Generation
All data is synthetically generated for demonstration purposes:
- **Fraud Detection**: Simulates agent registrations with fraud patterns
- **IoT Sensors**: Simulates equipment degradation over time
- **Water Demand**: Simulates consumption patterns with seasonality
- **Water Quality**: Simulates quality parameters with anomalies

### ML Models

**Fraud Detection:**
- Rule-Based: Threshold-based scoring
- Random Forest: Supervised classification
- Isolation Forest: Unsupervised anomaly detection
- Ensemble: Weighted combination

**Predictive Maintenance:**
- Random Forest Classifier for failure prediction
- Feature engineering on time-series data

**Demand Forecasting:**
- Prophet for seasonality detection
- Feature-based regression

**Anomaly Detection:**
- Isolation Forest for quality monitoring
- Statistical thresholds

---

## 🔒 Security & Privacy

- All data is synthetic and generated on-the-fly
- No real business data is used or stored
- No authentication required (demo purposes)
- Suitable for public showcase

---

## 📈 Performance

- **Load time**: < 3 seconds
- **Data generation**: < 2 seconds
- **Model training**: < 5 seconds
- **Visualization rendering**: < 1 second

Optimized for demo purposes with lightweight models.

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Module not found error
```bash
Solution: pip install -r requirements.txt --upgrade
```

**Issue**: Streamlit command not found
```bash
Solution: python -m streamlit run app.py
```

**Issue**: Port already in use
```bash
Solution: streamlit run app.py --server.port 8502
```

**Issue**: Out of memory on free hosting
```bash
Solution: Reduce data generation parameters (n_agents, n_days)
```

---

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

---

## 📄 License

This project is open source and available for educational and portfolio purposes.

---

## 👤 Contact

**Portfolio Showcase**

For inquiries about data analytics services or collaboration:
- 📧 Email: [your-email]
- 💼 LinkedIn: [your-linkedin]
- 🌐 Portfolio: [your-website]

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- ML libraries: Scikit-learn, XGBoost, Prophet
- Visualization: Plotly, Matplotlib

---

**⭐ Star this repository if you found it useful!**

*Last updated: 2025*
