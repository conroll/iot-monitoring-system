# IoT Monitoring System

An end-to-end IoT system for industrial device monitoring and control.

## 🚀 Tech Stack
- Python
- FastAPI
- MQTT (Mosquitto)
- PostgreSQL
- React
- Docker

---

## 📊 Features

- Real-time telemetry data via MQTT
- Backend data ingestion and storage
- React dashboard with charts (temperature & vibration)
- Device control (start / stop)
- Alert system with automatic shutdown on critical conditions

---

## 🧠 Architecture


Device (Python Simulator)
↓ MQTT publish
Mosquitto (Broker)
↓ subscribe
FastAPI Backend
↓ ORM
PostgreSQL Database
↓ API
React Frontend Dashboard


---

## 🔄 Data Flow


Device → MQTT → Backend → Database → Frontend


## 🔁 Control Flow


Frontend → API → MQTT → Device


---

## ⚙️ How to Run

### 1. Start MQTT (Docker)

```bash
docker run -d -p 1883:1883 eclipse-mosquitto
2. Start PostgreSQL (if not running)

Make sure PostgreSQL is running and database is created:

iot_platform
user: iot_user
password: iot_password
3. Run Backend
python -m uvicorn backend.main:app
4. Run Device Simulator
python simulator.py
5. Run Frontend
cd frontend
npm install
npm run dev

Open browser:

http://localhost:5174
🚨 Alert System

The system automatically triggers a STOP command when critical thresholds are exceeded:

Metric	Condition	Action
Temperature	> 78°C	Stop device
Vibration	> 0.95	Stop device
Voltage	< 22.0V	Stop device
🎯 Highlights
Implemented MQTT-based publish/subscribe communication
Designed real-time monitoring dashboard using React
Built device control system via API and MQTT
Implemented automatic safety shutdown mechanism
Solved real-world issues:
CORS cross-origin problems
MQTT duplicate subscriptions
Data ordering issues (latest-first handling)
Error handling for non-JSON MQTT messages
📌 Future Improvements
WebSocket for true real-time updates
Authentication & user management
Historical data analytics
Multi-device support
Deployment (Docker Compose / Cloud)
👤 Author

conroll

💡 Notes

This project simulates an industrial IoT monitoring system and demonstrates
end-to-end data flow, real-time processing, and control logic.
