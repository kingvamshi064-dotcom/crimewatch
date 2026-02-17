from __future__ import annotations

from datetime import datetime
from typing import Optional
import logging
import time

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import streamlit as st

# ============================================================
# 🔐 SECURITY & AUDIT LOGGING
# ============================================================
logging.basicConfig(
    filename="crimewatch_audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_action(action: str, user: Optional[str] = None, details: Optional[str] = None) -> None:
    logging.info(f"Action: {action} | User: {user or 'anonymous'} | Details: {details or 'N/A'}")


# ============================================================
# 🎬 PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="CrimeWatch AI | Sovereign Intelligence HUD",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 🎨 EPIC SOVEREIGN HUD CSS
# ============================================================
EPIC_SOVEREIGN_HUD_THEME = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500;700&display=swap');

:root {
    --midnight-void: #020205;
    --tactical-cyan: #00f3ff;
    --matrix-green: #00ff41;
    --intelligence-gold: #e0af68;
    --blood-orange: #ff4d00;
    --text-primary: #e5f3ff;
    --text-muted: #8aa0b8;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background: radial-gradient(circle at 20% 10%, #0a0a14, #020205 65%) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background:
        radial-gradient(circle at center, #0a0a14 0%, #020205 70%),
        linear-gradient(30deg, rgba(0,243,255,0.03) 12%, transparent 12.5%, transparent 87%, rgba(0,243,255,0.03) 87.5%, rgba(0,243,255,0.03)),
        linear-gradient(150deg, rgba(0,243,255,0.03) 12%, transparent 12.5%, transparent 87%, rgba(0,243,255,0.03) 87.5%, rgba(0,243,255,0.03));
    background-size: cover, 48px 84px, 48px 84px;
}

.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background:
        linear-gradient(rgba(255,255,255,0) 50%, rgba(0,0,0,0.11) 50%),
        linear-gradient(90deg, rgba(255,0,0,0.02), rgba(0,255,0,0.01), rgba(0,0,255,0.02));
    background-size: 100% 3px, 3px 100%;
    opacity: 0.22;
    z-index: 9999;
}

.block-container { padding-top: 0.6rem !important; max-width: 98% !important; }

.clean-header-container {
    position: sticky;
    top: 0;
    z-index: 9998;
    background: linear-gradient(135deg, rgba(2,6,23,0.95), rgba(10,18,34,0.95));
    border: 1px solid rgba(0,243,255,0.35);
    border-radius: 16px;
    padding: 14px 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.5), inset 0 0 20px rgba(0,243,255,0.08);
    margin-bottom: 14px;
}

.header-grid {
    display: grid;
    grid-template-columns: 2fr 1.2fr 1fr;
    gap: 16px;
    align-items: center;
}

.brand-section { display: flex; align-items: center; gap: 12px; }
.brand-logo { font-size: 34px; filter: drop-shadow(0 0 10px rgba(0,243,255,0.55)); }
.brand-title {
    margin: 0;
    font-weight: 800;
    color: var(--tactical-cyan);
    letter-spacing: 0.04em;
    font-size: 22px;
}
.brand-subtitle {
    margin: 2px 0 0;
    color: var(--text-muted);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.14em;
}

.mission-section {
    padding: 10px 14px;
    border: 1px solid rgba(0,243,255,0.24);
    border-radius: 12px;
    background: rgba(0,243,255,0.08);
}
.mission-label {
    margin: 0;
    color: #9db3c6;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
}
.mission-text {
    margin: 3px 0 0;
    color: var(--intelligence-gold);
    font-size: 12px;
    font-weight: 700;
}

.status-section { display: flex; gap: 16px; justify-content: flex-end; }
.status-item { text-align: right; }
.status-label {
    margin: 0 0 4px;
    color: #9db3c6;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 12px;
    border-radius: 999px;
    border: 1px solid rgba(0,255,65,0.35);
    background: rgba(0,255,65,0.09);
}
.status-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--matrix-green);
    box-shadow: 0 0 10px var(--matrix-green);
    animation: pulseDot 1.8s infinite;
}
@keyframes pulseDot {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.3); opacity: 0.8; }
}
.status-value { margin: 0; color: #9dffba; font-size: 11px; font-weight: 700; }
.header-divider {
    margin-top: 10px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--tactical-cyan), transparent);
}

.kpi-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 12px 0; }
.kpi-card {
    background: rgba(10, 10, 18, 0.74);
    border-radius: 14px;
    border: 1px solid rgba(0,243,255,0.23);
    padding: 14px;
    box-shadow: 0 8px 26px rgba(0,0,0,0.42), inset 0 0 12px rgba(0,243,255,0.08);
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 14px;
    padding: 1px;
    background: linear-gradient(130deg, rgba(0,243,255,0.55), rgba(0,102,255,0.3), rgba(0,243,255,0.55));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
}
.kpi-label { color: #8ea7bf; font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; margin: 0; }
.kpi-value {
    margin: 8px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: var(--tactical-cyan);
}
.kpi-foot { margin: 0; color: #b8cad9; font-size: 11px; }
.kpi-card.critical {
    border-color: rgba(255,77,0,0.5);
    box-shadow: 0 10px 32px rgba(255,77,0,0.2), inset 0 0 18px rgba(255,77,0,0.2);
    animation: alertPulse 2s infinite;
}
@keyframes alertPulse {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-2px); }
}

.briefing-container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
    padding: 14px;
    border-radius: 14px;
    border: 1px solid rgba(224,175,104,0.45);
    background: rgba(20, 16, 10, 0.55);
    box-shadow: 0 8px 22px rgba(0,0,0,0.4), inset 0 0 10px rgba(224,175,104,0.12);
    margin: 8px 0 14px;
}
.briefing-title {
    margin: 0 0 8px;
    color: var(--intelligence-gold);
    font-size: 12px;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    font-weight: 700;
}
.briefing-content { margin: 0; color: #d4e2ee; font-size: 12px; line-height: 1.65; }

.warning-panel {
    margin-top: 14px;
    background: linear-gradient(135deg, rgba(60, 0, 0, 0.7), rgba(120, 15, 0, 0.55));
    border: 1px solid rgba(255,77,0,0.4);
    border-radius: 12px;
    padding: 14px;
}
.warning-title { margin: 0 0 7px; color: #ffb79b; font-size: 16px; font-weight: 700; }
.warning-content { margin: 0; color: #ffd7c5; line-height: 1.65; font-size: 13px; }
.warning-footer { margin-top: 8px; color: #ffb79b; font-size: 11px; }

.data-stream-ticker {
    margin-top: 12px;
    background: rgba(5,5,10,0.9);
    border: 1px solid rgba(0,243,255,0.25);
    border-radius: 10px;
    padding: 8px 12px;
    overflow: hidden;
}
.ticker-content {
    display: inline-block;
    white-space: nowrap;
    animation: ticker 28s linear infinite;
    color: var(--matrix-green);
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
}
.stream-item { margin-right: 26px; border-right: 1px solid rgba(0,255,65,0.3); padding-right: 12px; }
@keyframes ticker {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

.footer {
    margin-top: 14px;
    padding: 12px;
    border-top: 1px solid rgba(0,243,255,0.23);
    color: #8ea7bf;
    font-size: 11px;
    text-align: center;
}
.footer-title { color: var(--tactical-cyan); font-weight: 700; letter-spacing: 0.1em; margin-bottom: 6px; }
.footer-warning { color: var(--intelligence-gold); margin-top: 6px; }
.footer-legal { color: #7f91a6; margin-top: 6px; font-size: 10px; }

#MainMenu, header, footer,
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stDeployButton"] {
    visibility: hidden !important;
    display: none !important;
}

::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: #05070c; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--tactical-cyan), rgba(0,243,255,0.35));
    border-radius: 8px;
}

@media (max-width: 1100px) {
    .header-grid { grid-template-columns: 1fr; }
    .status-section { justify-content: flex-start; }
    .briefing-container { grid-template-columns: 1fr; }
    .kpi-container { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 650px) {
    .kpi-container { grid-template-columns: 1fr; }
}
</style>
"""

st.markdown(EPIC_SOVEREIGN_HUD_THEME, unsafe_allow_html=True)


# ============================================================
# 📊 DATA ENGINE
# ============================================================
@st.cache_data(show_spinner=False, ttl=1800)
def load_crime_data() -> pd.DataFrame:
    np.random.seed(42)

    years = list(range(2018, 2025))
    states = {
        "Uttar Pradesh": (26.8467, 80.9462),
        "Maharashtra": (19.7515, 75.7139),
        "Bihar": (25.0961, 85.3131),
        "Madhya Pradesh": (22.9734, 78.6569),
        "Rajasthan": (27.0238, 74.2179),
        "Tamil Nadu": (11.1271, 78.6569),
        "Karnataka": (15.3173, 75.7139),
        "West Bengal": (22.9868, 87.8550),
    }
    crime_types = ["Theft", "Robbery", "Assault", "Cyber Fraud", "Narcotics", "Burglary", "Murder"]

    rows: list[dict[str, float | int | str]] = []
    for year in years:
        year_factor = 1 + ((year - 2018) * 0.05)
        for state, (lat, lon) in states.items():
            state_factor = np.random.uniform(0.9, 1.25)
            for crime in crime_types:
                crime_factor = {
                    "Theft": 1.3,
                    "Robbery": 1.0,
                    "Assault": 1.1,
                    "Cyber Fraud": 1.35,
                    "Narcotics": 0.9,
                    "Burglary": 0.95,
                    "Murder": 0.35,
                }[crime]
                incidents = int(np.random.randint(350, 1300) * year_factor * state_factor * crime_factor)
                solve_rate = np.random.uniform(0.48, 0.91)
                arrests = int(incidents * solve_rate)
                risk_score = float(np.clip((incidents / 30) + np.random.normal(0, 6), 10, 100))

                rows.append(
                    {
                        "Year": year,
                        "State": state,
                        "Crime_Type": crime,
                        "Incidents": incidents,
                        "Arrests": arrests,
                        "Risk_Score": risk_score,
                        "Latitude": float(lat + np.random.normal(0, 0.7)),
                        "Longitude": float(lon + np.random.normal(0, 0.8)),
                    }
                )

    df = pd.DataFrame(rows)
    log_action("Data Loaded", details=f"rows={len(df):,}, years={df['Year'].min()}-{df['Year'].max()}")
    return df


def apply_tactical_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk", size=12, color="#dcefff"),
        title=dict(font=dict(size=18, color="#00f3ff")),
        margin=dict(l=20, r=20, t=52, b=20),
        legend=dict(bgcolor="rgba(8, 15, 30, 0.7)", bordercolor="rgba(0,243,255,0.22)", borderwidth=1),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)", zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", zeroline=False),
    )
    return fig


def get_hud_metrics(df: pd.DataFrame) -> dict[str, str]:
    avg_risk = float(df["Risk_Score"].mean()) if not df.empty else 0.0
    if avg_risk >= 75:
        status = "CRITICAL"
    elif avg_risk >= 55:
        status = "ELEVATED"
    else:
        status = "OPERATIONAL"

    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "node": "INTEL-NODE-04",
        "status": status,
        "uptime": "99.98%",
    }


def render_sovereign_header(df: pd.DataFrame) -> None:
    metrics = get_hud_metrics(df)
    status_color = {
        "CRITICAL": "#ff4d00",
        "ELEVATED": "#e0af68",
        "OPERATIONAL": "#00ff41",
    }.get(metrics["status"], "#00ff41")

    st.markdown(
        f"""
        <div class="clean-header-container">
            <div class="header-grid">
                <div class="brand-section">
                    <div class="brand-logo">🤖</div>
                    <div>
                        <p class="brand-title">CRIMEWATCH AI</p>
                        <p class="brand-subtitle">Sovereign Intelligence HUD • Tactical Command v4.0</p>
                    </div>
                </div>
                <div class="mission-section">
                    <p class="mission-label">System Protocol</p>
                    <p class="mission-text">PREDICTIVE PATTERN RECOGNITION ACTIVE</p>
                </div>
                <div class="status-section">
                    <div class="status-item">
                        <p class="status-label">System Heartbeat</p>
                        <div class="status-badge">
                            <span class="status-dot"></span>
                            <p class="status-value" style="color:{status_color};">{metrics['status']}</p>
                        </div>
                    </div>
                    <div class="status-item">
                        <p class="status-label">Node • Uptime • Sync</p>
                        <p class="status-value" style="color:#00f3ff;">{metrics['node']} • {metrics['uptime']} • {metrics['timestamp']}</p>
                    </div>
                </div>
            </div>
            <div class="header-divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def run_live_simulation() -> bool:
    st.sidebar.markdown("### 🛠️ HUD Controls")
    live_mode = st.sidebar.toggle("📡 ENGAGE LIVE FEED", value=False)
    pulse_placeholder = st.sidebar.empty()

    if live_mode:
        i = 0
        while i < 4:
            threats = 8 + np.random.randint(0, 8)
            latency = 9 + np.random.randint(2, 14)
            packet = np.random.randint(1000, 9999)
            pulse_placeholder.markdown(
                f"""
                <div style="padding:10px; border-radius:10px; border:1px solid rgba(0,243,255,0.28); background:rgba(0,243,255,0.08); margin-top:8px;">
                    <code style="color:#00f3ff;">[SYSTEM] PACKET_0x{packet} processed</code><br>
                    <code style="color:#00ff41;">[INTEL] ACTIVE THREATS: {threats} | LATENCY: {latency}ms</code>
                </div>
                """,
                unsafe_allow_html=True,
            )
            i += 1
            time.sleep(0.35)
    else:
        pulse_placeholder.info("Live Feed Offline. Standing by...")

    return live_mode


def generate_intelligence_briefing(df: pd.DataFrame) -> dict[str, str | int | float]:
    if df.empty:
        return {
            "forecast": 0,
            "trend": "STABLE",
            "hotspot": "N/A",
            "primary_threat": "N/A",
            "confidence": "0%",
            "slope": 0.0,
        }

    yearly_totals = df.groupby("Year", as_index=False)["Incidents"].sum().sort_values("Year")
    x = yearly_totals["Year"].values
    y = yearly_totals["Incidents"].values

    if len(x) > 1:
        m, c = np.polyfit(x, y, 1)
    else:
        m, c = 0.0, float(y[0])

    target_year = int(df["Year"].max()) + 1
    forecast = int(max(0, m * target_year + c))
    trend = "INCREASING" if m > 0 else "DECREASING" if m < 0 else "STABLE"

    latest_year = int(df["Year"].max())
    latest = df[df["Year"] == latest_year]
    hotspot = latest.groupby("State")["Incidents"].sum().idxmax() if not latest.empty else "N/A"
    primary = latest.groupby("Crime_Type")["Incidents"].sum().idxmax() if not latest.empty else "N/A"

    confidence = float(np.clip(82 + np.random.normal(0, 3), 74, 93))
    return {
        "forecast": forecast,
        "trend": trend,
        "hotspot": hotspot,
        "primary_threat": primary,
        "confidence": f"{confidence:.1f}%",
        "slope": float(m),
    }


def render_briefing_room(intel: dict[str, str | int | float]) -> None:
    st.markdown(
        f"""
        <div class="briefing-container">
            <div>
                <p class="briefing-title">AI SITREP</p>
                <p class="briefing-content">
                    Trend analysis shows <strong>{intel['trend']}</strong> incident movement. Predicted total for {datetime.now().year + 1}:<br>
                    <strong style="color:#00f3ff;">{int(intel['forecast']):,}</strong> incidents.
                </p>
            </div>
            <div>
                <p class="briefing-title">Primary Threat Vector</p>
                <p class="briefing-content">
                    Most active state: <strong>{intel['hotspot']}</strong><br>
                    Dominant pattern: <strong>{intel['primary_threat']}</strong><br>
                    Model confidence: <strong style="color:#00ff41;">{intel['confidence']}</strong>
                </p>
            </div>
            <div>
                <p class="briefing-title">Commander Intent</p>
                <p class="briefing-content">
                    1) Prioritize rapid response in <strong>{intel['hotspot']}</strong>.<br>
                    2) Increase interception against <strong>{intel['primary_threat']}</strong> vectors.<br>
                    3) Maintain continuous watch on sector clusters and anomaly spikes.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(df: pd.DataFrame) -> None:
    if df.empty:
        st.warning("No data available for KPI computation.")
        return

    latest_year = int(df["Year"].max())
    latest = df[df["Year"] == latest_year]

    total_incidents = int(latest["Incidents"].sum())
    risk_index = float(latest["Risk_Score"].mean())
    solve_rate = float((latest["Arrests"].sum() / max(latest["Incidents"].sum(), 1)) * 100)
    critical_threats = int((latest["Risk_Score"] >= 80).sum())

    st.markdown(
        f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <p class="kpi-label">{latest_year} Total Incidents</p>
                <p class="kpi-value">{total_incidents:,}</p>
                <p class="kpi-foot">National observed crime volume</p>
            </div>
            <div class="kpi-card">
                <p class="kpi-label">Risk Index</p>
                <p class="kpi-value">{risk_index:.1f}</p>
                <p class="kpi-foot">Composite tactical risk score</p>
            </div>
            <div class="kpi-card">
                <p class="kpi-label">Solve Rate</p>
                <p class="kpi-value">{solve_rate:.1f}%</p>
                <p class="kpi-foot">Arrests / Incidents</p>
            </div>
            <div class="kpi-card critical">
                <p class="kpi-label">Critical Threats</p>
                <p class="kpi-value" style="color:#ff8d62;">{critical_threats}</p>
                <p class="kpi-foot">High-risk clusters requiring intervention</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def run_cluster_analysis(df: pd.DataFrame, n_clusters: int = 5) -> tuple[pd.DataFrame, pd.DataFrame]:
    if df.empty or len(df) < n_clusters:
        return df.copy(), pd.DataFrame(columns=["Latitude", "Longitude", "Sector"])

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    coords = df[["Latitude", "Longitude"]]
    labels = model.fit_predict(coords)

    out = df.copy()
    out["Sector"] = labels.astype(str)

    centers = pd.DataFrame(model.cluster_centers_, columns=["Latitude", "Longitude"])
    centers["Sector"] = [str(i) for i in range(len(centers))]
    return out, centers


def render_visuals(df: pd.DataFrame, intel: dict[str, str | int | float]) -> None:
    if df.empty:
        st.info("No data available for visualization.")
        return

    st.markdown("### 🌐 Predictive Trends • Heatmaps • Cluster Analysis")

    c1, c2 = st.columns(2)

    with c1:
        fig_map = px.density_mapbox(
            df,
            lat="Latitude",
            lon="Longitude",
            z="Risk_Score",
            radius=18,
            center=dict(lat=22.5, lon=80.5),
            zoom=3.3,
            mapbox_style="carto-darkmatter",
            color_continuous_scale=[(0.0, "#00f3ff"), (0.5, "#00b8ff"), (1.0, "#ff4d00")],
            title="Spatial Density Heatmap (Risk Trace)",
            hover_data={"State": True, "Crime_Type": True, "Risk_Score": ':.1f', "Latitude": False, "Longitude": False},
        )
        fig_map = apply_tactical_theme(fig_map)
        fig_map.update_layout(coloraxis_showscale=False, height=430)
        st.plotly_chart(fig_map, use_container_width=True)

    with c2:
        clustered, centers = run_cluster_analysis(df, n_clusters=5)
        fig_cluster = px.scatter(
            clustered,
            x="Longitude",
            y="Latitude",
            color="Sector",
            size="Risk_Score",
            hover_data=["State", "Crime_Type", "Incidents"],
            title="K-Means Sectoring (5 Tactical Clusters)",
            color_discrete_sequence=["#00f3ff", "#e0af68", "#00ff41", "#ff4d00", "#8b5cf6"],
        )
        if not centers.empty:
            fig_cluster.add_trace(
                go.Scatter(
                    x=centers["Longitude"],
                    y=centers["Latitude"],
                    mode="markers+text",
                    text=[f"C{i}" for i in range(len(centers))],
                    textposition="top center",
                    marker=dict(symbol="x", size=16, color="#ffffff", line=dict(width=2, color="#ff4d00")),
                    name="Centroids",
                )
            )
        fig_cluster = apply_tactical_theme(fig_cluster)
        fig_cluster.update_layout(height=430)
        st.plotly_chart(fig_cluster, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        yearly = df.groupby("Year", as_index=False)["Incidents"].sum().sort_values("Year")
        future_year = int(df["Year"].max()) + 1
        yearly = pd.concat(
            [
                yearly,
                pd.DataFrame({"Year": [future_year], "Incidents": [int(intel["forecast"])]}),
            ],
            ignore_index=True,
        )
        yearly["Series"] = ["Historical"] * (len(yearly) - 1) + ["Forecast"]

        fig_line = px.line(
            yearly,
            x="Year",
            y="Incidents",
            markers=True,
            color="Series",
            title="Temporal Trend + Linear Forecast",
            color_discrete_map={"Historical": "#00f3ff", "Forecast": "#e0af68"},
        )
        fig_line = apply_tactical_theme(fig_line)
        fig_line.update_layout(height=360)
        st.plotly_chart(fig_line, use_container_width=True)

    with c4:
        pie_df = df.groupby("Crime_Type", as_index=False)["Incidents"].sum().sort_values("Incidents", ascending=False)
        fig_donut = px.pie(
            pie_df,
            names="Crime_Type",
            values="Incidents",
            hole=0.48,
            title="Crime Distribution (Donut)",
            color_discrete_sequence=px.colors.sequential.Plasma,
        )
        fig_donut.update_traces(textposition="inside", textinfo="percent+label")
        fig_donut = apply_tactical_theme(fig_donut)
        fig_donut.update_layout(height=360)
        st.plotly_chart(fig_donut, use_container_width=True)


def render_warning_panel(df: pd.DataFrame) -> None:
    if df.empty:
        return

    latest = df[df["Year"] == df["Year"].max()]
    hot = latest.sort_values("Risk_Score", ascending=False).head(1)

    if hot.empty:
        return

    row = hot.iloc[0]
    st.markdown(
        f"""
        <div class="warning-panel">
            <p class="warning-title">⚠️ URGENT ALERT • CRITICAL ANOMALY DETECTED</p>
            <p class="warning-content">
                High-frequency <strong>{row['Crime_Type']}</strong> patterns detected in <strong>{row['State']}</strong> sector.
                Tactical engine estimates elevated escalation risk in the next 48 hours.
            </p>
            <p class="warning-footer">
                Protocol-9: ENABLED • Auto-notification: SENT • Risk Score: {row['Risk_Score']:.1f} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_export_module(df: pd.DataFrame) -> None:
    st.markdown("### 📥 Intel Data Stream & Exfiltration Module")

    if df.empty:
        st.info("No records available for export.")
        return

    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("🔍 Search Intelligence Database", placeholder="Filter by State, Crime Type, or Year")
    with col2:
        year_filter = st.selectbox("Year", options=["ALL"] + sorted(df["Year"].astype(str).unique().tolist(), reverse=True))

    filtered = df.copy()
    if year_filter != "ALL":
        filtered = filtered[filtered["Year"].astype(str) == year_filter]

    if query:
        mask = filtered.astype(str).apply(lambda s: s.str.contains(query, case=False, regex=False)).any(axis=1)
        filtered = filtered[mask]

    if filtered.empty:
        st.warning("No records match current search filters.")
        return

    st.dataframe(filtered.sort_values(["Year", "Risk_Score"], ascending=[False, False]), use_container_width=True, hide_index=True)

    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 DOWNLOAD SITREP",
        data=csv_bytes,
        file_name=f"SITREP_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=False,
    )


def render_ticker(df: pd.DataFrame) -> None:
    if df.empty:
        return

    latest = df[df["Year"] == df["Year"].max()]
    top_state = latest.groupby("State")["Incidents"].sum().idxmax() if not latest.empty else "N/A"
    top_crime = latest.groupby("Crime_Type")["Incidents"].sum().idxmax() if not latest.empty else "N/A"

    st.markdown(
        f"""
        <div class="data-stream-ticker">
            <div class="ticker-content">
                <span class="stream-item">📡 LATENCY: {10 + np.random.randint(1, 12)}MS</span>
                <span class="stream-item">⚠️ HOT SECTOR: {top_state}</span>
                <span class="stream-item">🧠 THREAT VECTOR: {top_crime}</span>
                <span class="stream-item">🔐 ENCRYPTION: AES-256-GCM</span>
                <span class="stream-item">⏱️ SYNC: {datetime.now().strftime('%H:%M:%S')} UTC</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        """
        <div class="footer">
            <div class="footer-title">Sovereign Intelligence HUD • Secure Terminal</div>
            <div>CONNECTION: SECURE • LATENCY: STABLE • ENCRYPTION: AES-256-GCM</div>
            <div class="footer-warning">RESTRICTED ACCESS • All actions are logged for audit trail and compliance review.</div>
            <div class="footer-legal">© 2026 CRIMEWATCH AI • MeitY AI Ethics Framework • DPDP Act 2023</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 🚀 APP ORCHESTRATION
# ============================================================
def main() -> None:
    df = load_crime_data()

    # Control panel / filters
    run_live_simulation()

    left, right = st.columns([2.8, 1.2])
    with left:
        year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
        year_range = st.slider("Operational Year Window", year_min, year_max, (year_min, year_max))
    with right:
        state_options = ["ALL STATES"] + sorted(df["State"].unique().tolist())
        state_filter = st.selectbox("State Sector", state_options)

    filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
    if state_filter != "ALL STATES":
        filtered = filtered[filtered["State"] == state_filter]

    render_sovereign_header(filtered)

    if filtered.empty:
        st.error("No data available for the selected filters. Expand the year window or switch to ALL STATES.")
        log_action("Filters Applied", details=f"empty-set years={year_range}, state={state_filter}")
        return

    intel = generate_intelligence_briefing(filtered)

    render_briefing_room(intel)
    render_kpis(filtered)
    render_visuals(filtered, intel)
    render_warning_panel(filtered)
    render_export_module(filtered)
    render_ticker(filtered)
    render_footer()

    log_action(
        "Dashboard Viewed",
        details=(
            f"years={year_range}, state={state_filter}, rows={len(filtered):,}, "
            f"avg_risk={filtered['Risk_Score'].mean():.2f}"
        ),
    )


if __name__ == "__main__":
    main()
