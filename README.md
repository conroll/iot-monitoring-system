# IoT Monitoring System

An end-to-end IoT system for industrial device monitoring and control.

## 🚀 Tech Stack
- Python
- FastAPI
- MQTT (Mosquitto)
- PostgreSQL
- React
- Docker

## 📊 Features
- Real-time telemetry data via MQTT
- Backend data ingestion and storage
- React dashboard with charts
- Device control (start / stop)
- Alert system with automatic shutdown

## 🧠 Architecture
Device → MQTT → FastAPI → PostgreSQL → React

## ⚙️ How to Run

### 1. Start MQTT (Docker)
```bash
docker run -d -p 1883:1883 eclipse-mosquitto
