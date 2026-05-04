import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

function App() {
  const [data, setData] = useState([]);

  const fetchData = () => {
    axios.get("http://127.0.0.1:8000/telemetry").then((res) => {
      setData(res.data);
    });
  };

  const sendCommand = async (cmd) => {
    await axios.post(`http://127.0.0.1:8000/command/machine-001?cmd=${cmd}`);
    setTimeout(fetchData, 1000);
  };

  useEffect(() => {
    fetchData();
    const timer = setInterval(fetchData, 2000);
    return () => clearInterval(timer);
  }, []);

  const latest = data[0];
  const alerts = [];

  if (latest) {
  if (latest.temperature > 70) alerts.push("高温报警");
  if (latest.vibration > 0.8) alerts.push("振动异常");
  if (latest.voltage < 22.5) alerts.push("低电压报警");
  }

  return (
    <div style={{ padding: 30 }}>
      <h1>IoT Dashboard</h1>

      <button onClick={() => sendCommand("start")} style={{ marginRight: 10 }}>
        启动设备
      </button>

      <button onClick={() => sendCommand("stop")}>
        停止设备
      </button>

      {latest && (
        <div style={{ border: "1px solid #ddd", padding: 20, marginTop: 20, marginBottom: 30 }}>
          <h2>当前设备状态</h2>
          <p><b>设备：</b>{latest.device_id}</p>
          <p><b>温度：</b>{latest.temperature} °C</p>
          <p><b>电压：</b>{latest.voltage} V</p>
          <p><b>振动：</b>{latest.vibration}</p>
          <p><b>状态：</b>{latest.status === "running" ? "在跑" : "停止"}</p>
        </div>
      )}

      <h2>温度实时曲线</h2>
      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <LineChart data={[...data].reverse()}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="id" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="temperature" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <h2>报警信息</h2>

      {alerts.length === 0 ? (
        <p>无报警</p>
      ) : (
        alerts.map((alert, index) => (
          <p key={index} style={{ color: "red", fontWeight: "bold" }}>
            🚨 {alert}
          </p>
        ))
      )}

      <h2>振动实时曲线</h2>
      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <LineChart data={[...data].reverse()}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="id" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="vibration" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;