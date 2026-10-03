# ⚡ Intelligent Energy Analytics

An intelligent electrical energy monitoring and analytics platform built with **FastAPI, SQLite, Machine Learning, and a web-based dashboard**.

The system collects electrical measurements, stores them persistently, performs statistical analysis, detects abnormal operating conditions, applies machine-learning-based anomaly detection, and forecasts future active-power demand.

---

## 🚀 Features

- Electrical energy measurement monitoring
- Persistent SQLite database storage
- Statistical energy analysis
- Rule-based anomaly detection
- Machine Learning anomaly detection
- Active-power forecasting
- REST API built with FastAPI
- Interactive Swagger API documentation
- Web-based monitoring dashboard
- Power history visualization
- Recent measurement monitoring
- Synthetic demonstration dataset
- System intelligence summary

---

## 🧠 Machine Learning

### Anomaly Detection

The system uses an **Isolation Forest** model to identify unusual electrical-energy measurements.

This complements the rule-based detection system, which checks predefined operating limits such as:

- Abnormal voltage
- Abnormal frequency
- Low power factor
- Invalid current values
- Invalid active-power values

### Energy Forecasting

A **Linear Regression** model is used to forecast active-power demand from the available measurement history.

A baseline moving-average forecast is also available for comparison.

---

## 📊 Electrical Measurements

The platform processes the following electrical parameters:

| Parameter | Unit |
|---|---|
| Voltage | V |
| Current | A |
| Active Power | W |
| Reactive Power | VAR |
| Power Factor | - |
| Frequency | Hz |

Each measurement also contains a timestamp and database ID.

---

## 🏗️ System Architecture

```text
Electrical / Demo Measurements
            |
            v
       FastAPI Backend
            |
     +------+------+
     |             |
     v             v
 SQLite DB     Analytics Engine
                   |
          +--------+---------+
          |                  |
          v                  v
   Rule Detection       ML Engine
                         |
                +--------+--------+
                |                 |
                v                 v
        Isolation Forest    Linear Regression
                |
                v
           REST API
                |
                v
        Web Dashboard
```

---

## 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy

### Data & Machine Learning

- Pandas
- NumPy
- Scikit-learn
- Isolation Forest
- Linear Regression

### Database

- SQLite

### Frontend

- HTML
- CSS
- JavaScript
- Chart.js

---

## 📁 Project Structure

```text
intelligent-energy-analytics/
│
├── backend/
│   ├── analytics.py
│   ├── database.py
│   ├── main.py
│   ├── ml_engine.py
│   └── schemas.py
│
├── frontend/
│   └── index.html
│
├── .gitignore
├── README.md
└── requirements.txt
```

Runtime files such as the SQLite database, Python cache files, and the local virtual environment are excluded from Git version control.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/TheCSMaker/intelligent-energy-analytics.git
```

Enter the project directory:

```bash
cd intelligent-energy-analytics
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Backend

From the project root directory:

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001
```

The API will run at:

```text
http://127.0.0.1:8001
```

Interactive API documentation:

```text
http://127.0.0.1:8001/docs
```

---

## 🖥️ Dashboard

After starting the backend, open:

```text
frontend/index.html
```

in a web browser.

The dashboard displays:

- Average voltage
- Average current
- Average active power
- Average power factor
- Active-power history
- Number of measurements
- Rule-based anomalies
- ML anomaly status
- ML anomaly count
- Forecast active power
- Forecast model
- Recent electrical measurements
- API connection status

---

## 🔌 Main API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | API health check |
| GET | `/measurements` | Retrieve measurements |
| POST | `/measurements` | Add a measurement |
| GET | `/analytics/statistics` | Energy statistics |
| GET | `/analytics/anomalies` | Rule-based anomalies |
| GET | `/analytics/forecast` | Baseline power forecast |
| GET | `/ml/anomalies` | ML anomaly detection |
| GET | `/ml/forecast` | ML power forecast |
| POST | `/demo/load` | Load demonstration dataset |
| GET | `/system/summary` | Complete system summary |

---

## 🧪 Demonstration Dataset

For software demonstration and ML pipeline testing, a synthetic electrical-energy dataset can be loaded through:

```text
POST /demo/load
```

The demonstration data contains normal operating patterns together with abnormal measurements so that the analytics and anomaly-detection pipelines can be tested.

Synthetic data is intended for **software demonstration and validation of the analytics pipeline**, not as real-world field measurements.

---

## 📈 Analytics

The analytics layer calculates summary statistics including:

- Measurement count
- Average voltage
- Average current
- Average active power
- Average power factor

Rule-based analysis provides deterministic detection of measurements outside configured operating conditions.

---

## 🤖 Intelligent Analysis Pipeline

```text
Measurement
     ↓
Database Storage
     ↓
Statistical Analysis
     ↓
Rule-Based Detection
     ↓
Machine Learning Analysis
     ↓
Power Forecasting
     ↓
REST API
     ↓
Monitoring Dashboard
```

This architecture separates data acquisition, persistence, analytics, machine learning, API services, and visualization.

---

## ⚠️ Current Scope

This project is an engineering/software prototype for electrical-energy analytics.

The included demonstration dataset is synthetic. Machine-learning results therefore demonstrate the implementation and workflow of the analytics system rather than validated performance on a large real-world electrical dataset.

Future development can integrate real-time measurements from smart meters, IoT devices, ESP32-based monitoring hardware, or established energy datasets.

---

## 🔮 Future Development

Possible extensions include:

- Real-time IoT sensor integration
- Smart-meter integration
- ESP32 energy-monitoring nodes
- Larger real-world energy datasets
- Load/appliance classification
- Advanced time-series forecasting
- Cloud database integration
- Cloud deployment
- User authentication
- Automated alert notifications
- Model evaluation and retraining pipeline

---

## 📌 Project Status

**Version:** 1.0.0

Core system implemented:

- Backend API ✅
- Persistent database ✅
- Analytics engine ✅
- Rule-based anomaly detection ✅
- Machine-learning anomaly detection ✅
- Power forecasting ✅
- Demonstration dataset ✅
- Web dashboard ✅
- API documentation ✅

---

## 👨‍💻 Author

**TheCSMaker**

Engineering, intelligent systems, embedded systems and energy analytics project.

---

## 📄 Disclaimer

This project is intended for educational, engineering-development, and software-demonstration purposes. It should not be treated as a certified electrical protection, billing, or safety system without appropriate hardware validation, calibration, testing, and regulatory compliance.