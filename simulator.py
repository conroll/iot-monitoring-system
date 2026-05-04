import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

DEVICE_ID = "machine-001"
TELEMETRY_TOPIC = f"factory/device/{DEVICE_ID}/telemetry"
COMMAND_TOPIC = f"factory/device/{DEVICE_ID}/command"

# 当前设备状态
status = "stopped"


# -----------------------------
# MQTT 回调
# -----------------------------
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT")
    client.subscribe(COMMAND_TOPIC)
    print("Subscribed to:", COMMAND_TOPIC)


def on_message(client, userdata, msg):
    global status

    command = msg.payload.decode().strip()
    print("Command received:", command)

    if command == "start":
        status = "running"
    elif command == "stop":
        status = "stopped"

    print("Current status:", status)


# -----------------------------
# MQTT 客户端初始化
# -----------------------------
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

print("Device simulator started...")

# -----------------------------
# 主循环（持续发送数据）
# -----------------------------
while True:
    data = {
        "device_id": DEVICE_ID,
        "temperature": round(random.uniform(20, 80), 2),
        "voltage": round(random.uniform(22, 26), 2),
        "vibration": round(random.uniform(0.1, 1.0), 2),
        "status": status,  # ✅ 用当前状态
        "timestamp": time.time(),
    }

    client.publish(TELEMETRY_TOPIC, json.dumps(data))
    print("Sent:", data)

    time.sleep(2)