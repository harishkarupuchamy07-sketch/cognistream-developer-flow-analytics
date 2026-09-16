import React, { useEffect, useState } from "react";
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, 
  LineChart, Line, 
  AreaChart, Area 
} from "recharts";

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeNav, setActiveNav] = useState("dashboard");
  const [data, setData] = useState([
    { event_type: "ide_focus", count: 184 },
    { event_type: "slack_msg", count: 42 },
    { event_type: "commit", count: 31 },
    { event_type: "pr_review", count: 23 }
  ]);

  const trendData = [
    { Hour: "09:00", Focus: 30, Interruptions: 5 },
    { Hour: "10:00", Focus: 45, Interruptions: 12 },
    { Hour: "11:00", Focus: 60, Interruptions: 8 },
    { Hour: "12:00", Focus: 25, Interruptions: 15 },
    { Hour: "13:00", Focus: 50, Interruptions: 4 },
    { Hour: "14:00", Focus: 75, Interruptions: 2 },
  ];

  const PIE_COLORS = ["#34d399", "#38bdf8", "#fbbf24", "#f43f5e"];

  useEffect(() => {
    const fetchMetrics = () => {
      fetch("http://127.0.0.1:8000/api/metrics/flow-state")
        .then((res) => res.json())
        .then((json) => {
          if (Array.isArray(json) && json.length > 0) setData(json);
        })
        .catch(() => {});
    };
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 3000);
    return () => clearInterval(interval);
  }, []);

  const totalEvents = data.reduce((acc, curr) => acc + curr.count, 0);
  const ideFocus = data.find((d) => d.event_type === "ide_focus")?.count || 0;
  const slackMsgs = data.find((d) => d.event_type === "slack_msg")?.count || 0;
  const flowScore = totalEvents > 0 ? Math.round((ideFocus / totalEvents) * 100) : 0;

  const cardStyle = {
    background: "rgba(15, 23, 42, 0.9)",
    border: "1px solid #1e293b",
    borderRadius: "16px",
    padding: "20px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.5)"
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", backgroundColor: "#020617", color: "#f8fafc", fontFamily: "sans-serif" }}>
      
      {/* Sidebar Navigation */}
      <aside style={{
        width: sidebarOpen ? "250px" : "80px",
        transition: "width 0.2s ease",
        backgroundColor: "#0f172a",
        borderRight: "1px solid #1e293b",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: "20px 16px",
        zIndex: 50,
        boxSizing: "border-box"
      }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "32px" }}>
            {sidebarOpen && (
              <span style={{ fontSize: "20px", fontWeight: "900", color: "#38bdf8", letterSpacing: "0.5px" }}>
                CogniStream
              </span>
            )}
            <button 
              onClick={() => setSidebarOpen(!sidebarOpen)}
              style={{ background: "#1e293b", border: "1px solid #334155", color: "#fff", padding: "6px 12px", borderRadius: "8px", cursor: "pointer", marginLeft: "auto" }}
            >
              {sidebarOpen ? "◀" : "▶"}
            </button>
          </div>

          <nav style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {[
              { id: "dashboard", label: "Dashboard", icon: "📊" },
              { id: "flow", label: "Flow Analysis", icon: "⚡" },
              { id: "logs", label: "Interruption Logs", icon: "🚨" },
              { id: "settings", label: "Settings", icon: "⚙️" },
            ].map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveNav(item.id)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "12px",
                  padding: "12px 14px",
                  borderRadius: "10px",
                  border: "none",
                  cursor: "pointer",
                  fontWeight: "600",
                  fontSize: "14px",
                  textAlign: "left",
                  backgroundColor: activeNav === item.id ? "#0d9488" : "transparent",
                  color: activeNav === item.id ? "#ffffff" : "#94a3b8",
                  width: "100%"
                }}
              >
                <span style={{ fontSize: "18px" }}>{item.icon}</span>
                {sidebarOpen && <span>{item.label}</span>}
              </button>
            ))}
          </nav>
        </div>

        {sidebarOpen && (
          <div style={{ padding: "12px", backgroundColor: "#1e293b", borderRadius: "10px", fontSize: "12px", color: "#94a3b8" }}>
            <p style={{ margin: 0, fontWeight: "bold", color: "#f8fafc" }}>Engine: ClickHouse</p>
            <p style={{ margin: "4px 0 0 0", color: "#34d399", fontWeight: "600" }}>● Connected</p>
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <main style={{ flex: 1, padding: "32px", overflowY: "auto", boxSizing: "border-box" }}>
        
        {/* Header Bar */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "32px", paddingBottom: "16px", borderBottom: "1px solid #1e293b" }}>
          <div>
            <h1 style={{ fontSize: "26px", fontWeight: "800", margin: 0, color: "#ffffff" }}>
              {activeNav === "dashboard" && "Executive Telemetry Hub"}
              {activeNav === "flow" && "Developer Flow Analytics"}
              {activeNav === "logs" && "Interruption Logs"}
              {activeNav === "settings" && "Pipeline Settings"}
            </h1>
            <p style={{ color: "#94a3b8", fontSize: "14px", margin: "4px 0 0 0" }}>Real-time telemetry engine powered by FastAPI & ClickHouse</p>
          </div>
        </div>

        {/* Dynamic Nav View */}
        {activeNav === "dashboard" && (
          <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
            
            {/* KPI Cards */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "16px" }}>
              <div style={cardStyle}>
                <p style={{ color: "#94a3b8", fontSize: "12px", margin: 0 }}>Total Activity Events</p>
                <h2 style={{ color: "#38bdf8", fontSize: "32px", margin: "8px 0 0 0", fontWeight: "900" }}>{totalEvents}</h2>
              </div>
              <div style={cardStyle}>
                <p style={{ color: "#94a3b8", fontSize: "12px", margin: 0 }}>Flow Efficiency Ratio</p>
                <h2 style={{ color: "#34d399", fontSize: "32px", margin: "8px 0 0 0", fontWeight: "900" }}>{flowScore}%</h2>
              </div>
              <div style={cardStyle}>
                <p style={{ color: "#94a3b8", fontSize: "12px", margin: 0 }}>Deep Focus Blocks</p>
                <h2 style={{ color: "#2dd4bf", fontSize: "32px", margin: "8px 0 0 0", fontWeight: "900" }}>{ideFocus}</h2>
              </div>
              <div style={cardStyle}>
                <p style={{ color: "#94a3b8", fontSize: "12px", margin: 0 }}>Slack Interruptions</p>
                <h2 style={{ color: "#fbbf24", fontSize: "32px", margin: "8px 0 0 0", fontWeight: "900" }}>{slackMsgs}</h2>
              </div>
            </div>

            {/* 4 Interactive Charts Grid */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))", gap: "20px" }}>
              
              {/* Chart 1: Bar Chart */}
              <div style={cardStyle}>
                <h3 style={{ color: "#ffffff", margin: "0 0 4px 0", fontSize: "16px" }}>Telemetry Event Distribution</h3>
                <p style={{ color: "#94a3b8", fontSize: "12px", margin: "0 0 16px 0" }}>Event frequency categorized by tool</p>
                <div style={{ height: "220px", width: "100%" }}>
                  <ResponsiveContainer>
                    <BarChart data={data}>
                      <XAxis dataKey="event_type" stroke="#64748b" fontSize={12} />
                      <YAxis stroke="#64748b" fontSize={12} />
                      <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", color: "#fff" }} />
                      <Bar dataKey="count" fill="#34d399" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Chart 2: Donut Chart */}
              <div style={cardStyle}>
                <h3 style={{ color: "#ffffff", margin: "0 0 4px 0", fontSize: "16px" }}>Activity Ratio Breakdown</h3>
                <p style={{ color: "#94a3b8", fontSize: "12px", margin: "0 0 16px 0" }}>Developer attention distribution</p>
                <div style={{ height: "220px", width: "100%" }}>
                  <ResponsiveContainer>
                    <PieChart>
                      <Pie data={data} dataKey="count" nameKey="event_type" innerRadius={60} outerRadius={85} paddingAngle={4}>
                        {data.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", color: "#fff" }} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Chart 3: Smooth Cubic Line Chart */}
              <div style={cardStyle}>
                <h3 style={{ color: "#ffffff", margin: "0 0 4px 0", fontSize: "16px" }}>Focus vs Interruption Timeline</h3>
                <p style={{ color: "#94a3b8", fontSize: "12px", margin: "0 0 16px 0" }}>Hourly focus trend</p>
                <div style={{ height: "220px", width: "100%" }}>
                  <ResponsiveContainer>
                    <LineChart data={trendData}>
                      <XAxis dataKey="Hour" stroke="#64748b" fontSize={12} />
                      <YAxis stroke="#64748b" fontSize={12} />
                      <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", color: "#fff" }} />
                      <Line type="monotone" dataKey="Focus" stroke="#34d399" strokeWidth={3} dot={{ fill: "#34d399" }} />
                      <Line type="monotone" dataKey="Interruptions" stroke="#fbbf24" strokeWidth={3} dot={{ fill: "#fbbf24" }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Chart 4: Area Chart */}
              <div style={cardStyle}>
                <h3 style={{ color: "#ffffff", margin: "0 0 4px 0", fontSize: "16px" }}>Cumulative Load Density</h3>
                <p style={{ color: "#94a3b8", fontSize: "12px", margin: "0 0 16px 0" }}>Cognitive density profile</p>
                <div style={{ height: "220px", width: "100%" }}>
                  <ResponsiveContainer>
                    <AreaChart data={data}>
                      <XAxis dataKey="event_type" stroke="#64748b" fontSize={12} />
                      <YAxis stroke="#64748b" fontSize={12} />
                      <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", color: "#fff" }} />
                      <Area type="monotone" dataKey="count" stroke="#38bdf8" fill="#0284c7" fillOpacity={0.4} />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

            </div>

          </div>
        )}

      </main>
    </div>
  );
}
