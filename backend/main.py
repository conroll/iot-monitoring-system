from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
import json

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://iot_user:iot_password@localhost:5432/iot_platform"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    temperature = Column(Float)
    voltage = Column(Float)
    vibration = Column(Float)
    status = Column(String)
    timestamp = Column(Float)


Base.metadata.create_all(bind=engine)

BROKER = "localhost"
MQTT_PORT = 1883
TELEMETRY_TOPIC = "factory/device/+/telemetry"


def send_stop_command(device_id):
    control_client = mqtt.Client()
    control_client.connect(BROKER, MQTT_PORT, 60)

    topic = f"factory/device/{device_id}/command"
    result = control_client.publish(topic, "stop")
    result.wait_for_publish()

    control_client.disconnect()

    print("STOP command sent to:", device_id)


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT")
    client.subscribe(TELEMETRY_TOPIC)
    print("Subscribed to:", TELEMETRY_TOPIC)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("Received:", payload)

    if not msg.topic.endswith("/telemetry"):
        print("Ignored non-telemetry topic:", msg.topic)
        return

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print("Invalid JSON ignored:", payload)
        return

    db = SessionLocal()
    record = Telemetry(
        device_id=data["device_id"],
        temperature=data["temperature"],
        voltage=data["voltage"],
        vibration=data["vibration"],
        status=data["status"],
        timestamp=data["timestamp"],
    )
    db.add(record)
    db.commit()
    db.close()

    print("Saved to database")

    if (
        data["temperature"] > 78
        or data["vibration"] > 0.95
        or data["voltage"] < 22.0
    ):
        print("🚨 Critical Alert! Auto stopping device")
        send_stop_command(data["device_id"])


def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, MQTT_PORT, 60)
    client.loop_start()


@app.on_event("startup")
def startup_event():
    start_mqtt()


@app.get("/")
def read_root():
    return {"message": "IoT Backend Running"}


@app.get("/telemetry")
def get_telemetry():
    db = SessionLocal()
    records = db.query(Telemetry).order_by(Telemetry.id.desc()).limit(20).all()
    db.close()
    return records


@app.post("/command/{device_id}")
def send_command(device_id: str, cmd: str):
    control_client = mqtt.Client()
    control_client.connect(BROKER, MQTT_PORT, 60)

    topic = f"factory/device/{device_id}/command"
    result = control_client.publish(topic, cmd)
    result.wait_for_publish()

    control_client.disconnect()

    print("Command sent:", topic, cmd)

    return {
        "status": "sent",
        "device_id": device_id,
        "command": cmd,
    }