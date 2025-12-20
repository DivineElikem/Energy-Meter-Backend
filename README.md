# Smart Energy Meter Monitoring System

A comprehensive IoT solution for real-time energy monitoring, featuring AI-powered forecasting, anomaly detection, and an interactive "Energy Boss" chatbot.

## 🚀 Features

- **Real-time Monitoring**: Track energy consumption (Voltage, Current, Power) in real-time.
- **AI Forecasting**: Predict future energy usage using Facebook Prophet.
- **Anomaly Detection**: Identifies unusual consumption patterns based on consumption threshold settings.
- **Energy Boss Chatbot**: Interact with an AI assistant to get insights about your energy usage, powered by Groq (Llama 3).
- **Responsive Dashboard**: Beautiful and intuitive UI built with Next.js and Tailwind CSS.
- **MQTT Integration**: Scalable data collection from IoT devices.

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLAlchemy with SQLite
- **AI/ML**: Facebook Prophet (Forecasting), Pandas
- **LLM**: Groq (Llama 3) for Chatbot
- **Communication**: Paho-MQTT
- **Task Scheduling**: APScheduler

### Frontend
- **Framework**: Next.js 15+ (App Router)
- **Styling**: Tailwind CSS 4
- **Icons**: Lucide React
- **Charts**: Recharts
- **Animations**: Framer Motion

## 📦 Project Structure

```text
.
├── app/                # FastAPI Backend
│   ├── api/            # API Endpoints
│   ├── db/             # Database Models & CRUD
│   ├── services/       # Business Logic (MQTT, Chat, Forecast)
│   └── main.py         # App Entry Point
├── frontend/           # Next.js Frontend
│   ├── app/            # Next.js Pages & Layouts
│   ├── components/     # UI Components
│   └── services/       # API Integration
├── requirements.txt    # Python Dependencies
└── .env                # Environment Variables
```

## ⚙️ Setup Instructions

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd energy-meter-backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=sqlite:///./energy_meter.db
   MQTT_BROKER=broker.emqx.io
   MQTT_PORT=1883
   MQTT_TOPIC=energy/readings
   GROQ_API_KEY=your_groq_api_key
   ```

5. **Start the backend server**:
   ```bash
   python -m app.main
   ```
   The API will be available at `http://localhost:8000`.

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```
   The dashboard will be available at `http://localhost:3000`.

## 📈 ML & AI

This project leverages:
- **Facebook Prophet** for accurate time-series forecasting of energy consumption.
- **RAG (Retrieval-Augmented Generation)** principles to give the "Energy Boss" chatbot context about current readings.


