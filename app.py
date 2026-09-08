import streamlit as st
import joblib
import numpy as np

# Load models
flood_model = joblib.load("models/flood_model.pkl")
fire_model = joblib.load("models/fire_model.pkl")
pollution_model = joblib.load("models/pollution_model.pkl")

# Page configuration
st.set_page_config(
    page_title="Environmental Intelligence Network",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_flood_category(risk_percent):
    """Get flood risk category, color, and border color."""
    if risk_percent < 25:
        return "LOW", "#00cc44", "#003300"
    elif risk_percent < 50:
        return "MODERATE", "#ffdd00", "#333300"
    elif risk_percent < 75:
        return "HIGH", "#ff8800", "#330000"
    else:
        return "EXTREME", "#ff0000", "#660000"

def get_fire_category(risk_percent):
    """Get fire risk category, color, and border color."""
    if risk_percent < 25:
        return "LOW", "#00cc44", "#003300"
    elif risk_percent < 50:
        return "ELEVATED", "#ffdd00", "#333300"
    elif risk_percent < 75:
        return "HIGH", "#ff8800", "#330000"
    else:
        return "EXTREME FIRE RISK", "#ff0000", "#660000"

def get_pollution_category(risk_percent):
    """Get pollution risk category, color, and border color."""
    if risk_percent < 25:
        return "GOOD", "#00cc44", "#003300"
    elif risk_percent < 50:
        return "MODERATE", "#ffdd00", "#333300"
    elif risk_percent < 75:
        return "POOR", "#ff8800", "#330000"
    else:
        return "SEVERE", "#ff0000", "#660000"

def render_hazard_card(title, emoji, risk_percent, category, color, sensor_info):
    """Render a hazard card with visual progress meter."""
    meter_width = min(risk_percent, 100)
    card_html = (
        f'<div style="background:linear-gradient(135deg,rgba(10,10,25,0.95),rgba(20,20,40,0.95));border:2px solid {color};border-radius:12px;padding:24px;margin:8px 0;box-shadow:0 8px 32px rgba(0,0,0,0.5);font-family:Segoe UI,Tahoma,sans-serif;">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;">'
        f'<div style="font-size:18px;font-weight:600;color:#e0e0e0;">{emoji} {title}</div>'
        f'<div style="font-size:42px;font-weight:bold;color:{color};text-align:right;">{risk_percent:.1f}%</div>'
        f'</div>'
        f'<div style="background:rgba(0,0,0,0.6);border-radius:8px;height:28px;overflow:hidden;margin:16px 0;border:1px solid rgba(255,255,255,0.1);">'
        f'<div style="background:linear-gradient(90deg,{color},{color}dd);height:100%;width:{meter_width}%;border-radius:8px;transition:width 0.3s ease;"></div>'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.1);font-size:13px;">'
        f'<div style="font-weight:600;color:{color};">● {category}</div>'
        f'<div style="color:#999;text-align:right;">{sensor_info}</div>'
        f'</div>'
        f'</div>'
    )
    return card_html

def render_sensor_status_card(name, emoji, value, unit, status):
    """Render a sensor status card."""
    if status == "NORMAL":
        status_color = "#00cc44"
        status_symbol = "✓"
    elif status == "ELEVATED":
        status_color = "#ffdd00"
        status_symbol = "⚠"
    else:  # HIGH
        status_color = "#ff0000"
        status_symbol = "⛔"
    
    card_html = (
        f'<div style="background:linear-gradient(135deg,rgba(20,20,40,0.9),rgba(30,30,50,0.9));border:1px solid rgba(100,150,200,0.3);border-radius:8px;padding:12px;text-align:center;font-family:Segoe UI,Tahoma,sans-serif;">'
        f'<div style="font-size:20px;margin-bottom:6px;">{emoji}</div>'
        f'<div style="font-size:11px;color:#999;margin-bottom:4px;text-transform:uppercase;letter-spacing:0.5px;">{name}</div>'
        f'<div style="font-size:22px;font-weight:bold;color:#00ff88;margin-bottom:6px;">{value}</div>'
        f'<div style="font-size:10px;color:#666;margin-bottom:8px;">{unit}</div>'
        f'<div style="font-size:11px;color:{status_color};font-weight:600;letter-spacing:0.5px;">{status_symbol} {status}</div>'
        f'</div>'
    )
    return card_html

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0a1a 0%, #15151f 50%, #0d0d1a 100%);
        color: #e0e0e0;
    }
    
    .main {
        background: transparent;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    section[data-testid="stSidebar"] {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown("""
<div style="
    padding: 32px 0;
    text-align: center;
    border-bottom: 2px solid rgba(0, 200, 100, 0.3);
    margin-bottom: 24px;
">
    <div style="
        font-size: 36px;
        font-weight: 800;
        color: #00ff88;
        letter-spacing: 3px;
        margin-bottom: 8px;
        font-family: 'Courier New', monospace;
    ">
        🌍 ENVIRONMENTAL INTELLIGENCE NETWORK
    </div>
    <div style="
        font-size: 13px;
        color: #888;
        letter-spacing: 2px;
        text-transform: uppercase;
    ">
        AI-Powered Multi-Hazard Edge Monitoring Node
    </div>
    <div style="
        font-size: 12px;
        color: #00ff88;
        margin-top: 12px;
        letter-spacing: 1px;
    ">
        ● SYSTEM ONLINE &nbsp; | &nbsp; NODE 01
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SENSOR INPUTS (Collapsible)
# ============================================================================

with st.expander("⚙️ SENSOR SIMULATION & CONTROL", expanded=True):
    st.markdown("<div style='color: #999; font-size: 12px; margin-bottom: 12px;'>Adjust sensor values to simulate real-world environmental conditions. All values update in real-time.</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temperature = st.number_input("🌡️ Temperature (°C)", 0.0, 60.0, 30.0, key="temp")
        humidity = st.number_input("💧 Humidity (%)", 0.0, 100.0, 60.0, key="humid")
        soil_moisture = st.number_input("🌱 Soil Moisture (%)", 0.0, 100.0, 50.0, key="soil")
    
    with col2:
        rainfall = st.number_input("🌧️ Rainfall (mm/hr)", 0.0, 500.0, 10.0, key="rain")
        water_level = st.number_input("💦 Water Level (cm)", 0.0, 500.0, 40.0, key="water")
        water_rise_rate = st.number_input("📈 Water Rise Rate (cm/10min)", 0.0, 20.0, 5.0, key="rise")
    
    with col3:
        pm25 = st.number_input("🌫️ PM2.5 (µg/m³)", 0.0, 1000.0, 30.0, key="pm25")
        pm10 = st.number_input("🌫️ PM10 (µg/m³)", 0.0, 600.0, 50.0, key="pm10")
        smoke = st.number_input("💨 Smoke Level", 0.0, 1000.0, 10.0, key="smoke")
        co = st.number_input("⚠️ CO Level (ppm)", 0.0, 20.0, 2.0, key="co")

# ============================================================================
# RISK CALCULATIONS (Keep existing model logic)
# ============================================================================

flood_input = np.array([[water_level, rainfall, soil_moisture, water_rise_rate]])
flood_probability = flood_model.predict_proba(flood_input)[0][1]
flood_percent = flood_probability * 100
flood_category, flood_color, flood_border = get_flood_category(flood_percent)

fire_input = np.array([[temperature, humidity, smoke, co]])
fire_probability = fire_model.predict_proba(fire_input)[0][1]
fire_percent = fire_probability * 100
fire_category, fire_color, fire_border = get_fire_category(fire_percent)

pollution_input = np.array([[pm25, pm10, co, temperature, humidity]])
pollution_probability = pollution_model.predict_proba(pollution_input)[0][1]
pollution_percent = pollution_probability * 100
pollution_category, pollution_color, pollution_border = get_pollution_category(pollution_percent)

# ============================================================================
# HAZARD THREAT ASSESSMENT
# ============================================================================

st.markdown("""
<div style="
    margin: 32px 0 16px 0;
    padding: 12px 16px;
    background: rgba(0, 150, 100, 0.08);
    border-left: 4px solid #00cc77;
    border-radius: 4px;
">
    <div style="
        font-size: 13px;
        color: #00dd88;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase;
    ">
        ⚠️ HAZARD THREAT ASSESSMENT
    </div>
</div>
""", unsafe_allow_html=True)

col_flood, col_fire, col_pollution = st.columns(3)

with col_flood:
    flood_sensor_info = f"{water_level:.0f}cm water, {rainfall:.2f}mm/hr"
    st.markdown(render_hazard_card(
        "FLOOD THREAT",
        "🌊",
        flood_percent,
        flood_category,
        flood_color,
        flood_sensor_info
    ), unsafe_allow_html=True)

with col_fire:
    fire_sensor_info = f"{temperature:.0f}°C, {humidity:.0f}% RH, smoke"
    st.markdown(render_hazard_card(
        "FIRE THREAT",
        "🔥",
        fire_percent,
        fire_category,
        fire_color,
        fire_sensor_info
    ), unsafe_allow_html=True)

with col_pollution:
    pollution_sensor_info = f"PM2.5: {pm25:.0f}, PM10: {pm10:.0f}"
    st.markdown(render_hazard_card(
        "AIR QUALITY THREAT",
        "🏭",
        pollution_percent,
        pollution_category,
        pollution_color,
        pollution_sensor_info
    ), unsafe_allow_html=True)

# ============================================================================
# LIVE SENSOR INTELLIGENCE
# ============================================================================

st.markdown("""
<div style="
    margin: 32px 0 16px 0;
    padding: 12px 16px;
    background: rgba(100, 150, 255, 0.08);
    border-left: 4px solid #6699ff;
    border-radius: 4px;
">
    <div style="
        font-size: 13px;
        color: #6699ff;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase;
    ">
        📡 LIVE SENSOR INTELLIGENCE
    </div>
</div>
""", unsafe_allow_html=True)

# Helper function for sensor status
def get_sensor_status(value, thresholds_normal, thresholds_elevated):
    if value <= thresholds_normal:
        return "NORMAL"
    elif value <= thresholds_elevated:
        return "ELEVATED"
    else:
        return "HIGH"

sensor_row1 = st.columns(5)
with sensor_row1[0]:
    st.markdown(render_sensor_status_card(
        "Temperature",
        "🌡️",
        f"{temperature:.1f}",
        "°C",
        get_sensor_status(temperature, 25, 35)
    ), unsafe_allow_html=True)

with sensor_row1[1]:
    st.markdown(render_sensor_status_card(
        "Humidity",
        "💧",
        f"{humidity:.1f}",
        "%",
        get_sensor_status(humidity, 70, 85)
    ), unsafe_allow_html=True)

with sensor_row1[2]:
    st.markdown(render_sensor_status_card(
        "Rainfall",
        "🌧️",
        f"{rainfall:.2f}",
        "mm/hr",
        get_sensor_status(rainfall, 5, 20)
    ), unsafe_allow_html=True)

with sensor_row1[3]:
    st.markdown(render_sensor_status_card(
        "Water Level",
        "💦",
        f"{water_level:.1f}",
        "cm",
        get_sensor_status(water_level, 50, 100)
    ), unsafe_allow_html=True)

with sensor_row1[4]:
    st.markdown(render_sensor_status_card(
        "PM2.5",
        "🌫️",
        f"{pm25:.0f}",
        "µg/m³",
        get_sensor_status(pm25, 35, 75)
    ), unsafe_allow_html=True)

sensor_row2 = st.columns(5)
with sensor_row2[0]:
    st.markdown(render_sensor_status_card(
        "Water Rise",
        "📈",
        f"{water_rise_rate:.2f}",
        "cm/10min",
        get_sensor_status(water_rise_rate, 3, 8)
    ), unsafe_allow_html=True)

with sensor_row2[1]:
    st.markdown(render_sensor_status_card(
        "PM10",
        "🌫️",
        f"{pm10:.0f}",
        "µg/m³",
        get_sensor_status(pm10, 50, 100)
    ), unsafe_allow_html=True)

with sensor_row2[2]:
    st.markdown(render_sensor_status_card(
        "Smoke",
        "💨",
        f"{smoke:.0f}",
        "Level",
        get_sensor_status(smoke, 50, 200)
    ), unsafe_allow_html=True)

with sensor_row2[3]:
    st.markdown(render_sensor_status_card(
        "CO Level",
        "⚠️",
        f"{co:.2f}",
        "ppm",
        get_sensor_status(co, 5, 10)
    ), unsafe_allow_html=True)

with sensor_row2[4]:
    st.markdown(render_sensor_status_card(
        "Soil Moisture",
        "🌱",
        f"{soil_moisture:.1f}",
        "%",
        get_sensor_status(soil_moisture, 40, 70)
    ), unsafe_allow_html=True)

# ============================================================================
# AI RISK ANALYSIS
# ============================================================================

st.markdown("""
<div style="
    margin: 32px 0 16px 0;
    padding: 12px 16px;
    background: rgba(150, 100, 255, 0.08);
    border-left: 4px solid #9966ff;
    border-radius: 4px;
">
    <div style="
        font-size: 13px;
        color: #9966ff;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase;
    ">
        🤖 AI RISK ANALYSIS
    </div>
</div>
""", unsafe_allow_html=True)

analysis_cols = st.columns(3)

with analysis_cols[0]:
    analysis_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(0, 100, 150, 0.15), rgba(20, 20, 40, 0.9));
        border: 1px solid {flood_color};
        border-radius: 8px;
        padding: 16px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    ">
        <div style="font-weight: 600; margin-bottom: 10px; color: #00ddff;">
            🌊 Flood Risk Analysis
        </div>
        <div style="font-size: 13px; line-height: 1.6; color: #ccc;">
            Water level is at <span style="color: {flood_color}; font-weight: bold;">{water_level:.1f} cm</span>
            with rainfall of <span style="color: {flood_color}; font-weight: bold;">{rainfall:.2f} mm/hr</span>.
            These rising water conditions are contributing to <span style="color: {flood_color}; font-weight: bold;">{flood_category.lower()} flood risk</span>.
        </div>
    </div>
    """
    st.markdown(analysis_html, unsafe_allow_html=True)

with analysis_cols[1]:
    analysis_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(150, 100, 0, 0.15), rgba(20, 20, 40, 0.9));
        border: 1px solid {fire_color};
        border-radius: 8px;
        padding: 16px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    ">
        <div style="font-weight: 600; margin-bottom: 10px; color: #ff9933;">
            🔥 Fire Risk Analysis
        </div>
        <div style="font-size: 13px; line-height: 1.6; color: #ccc;">
            Temperature of <span style="color: {fire_color}; font-weight: bold;">{temperature:.1f}°C</span>,
            humidity at <span style="color: {fire_color}; font-weight: bold;">{humidity:.1f}%</span>,
            and smoke levels of <span style="color: {fire_color}; font-weight: bold;">{smoke:.0f}</span> are
            contributing to <span style="color: {fire_color}; font-weight: bold;">{fire_category.lower()} fire risk</span>.
        </div>
    </div>
    """
    st.markdown(analysis_html, unsafe_allow_html=True)

with analysis_cols[2]:
    analysis_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(100, 100, 0, 0.15), rgba(20, 20, 40, 0.9));
        border: 1px solid {pollution_color};
        border-radius: 8px;
        padding: 16px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    ">
        <div style="font-weight: 600; margin-bottom: 10px; color: #ccaa00;">
            🏭 Air Quality Analysis
        </div>
        <div style="font-size: 13px; line-height: 1.6; color: #ccc;">
            PM2.5 levels at <span style="color: {pollution_color}; font-weight: bold;">{pm25:.0f} µg/m³</span>
            and PM10 at <span style="color: {pollution_color}; font-weight: bold;">{pm10:.0f} µg/m³</span> are
            contributing to <span style="color: {pollution_color}; font-weight: bold;">{pollution_category.lower()} air quality</span>.
        </div>
    </div>
    """
    st.markdown(analysis_html, unsafe_allow_html=True)

# ============================================================================
# ACTIVE ALERT PANEL
# ============================================================================

st.markdown("""
<div style="
    margin: 32px 0 16px 0;
    padding: 12px 16px;
    background: rgba(255, 100, 100, 0.08);
    border-left: 4px solid #ff6666;
    border-radius: 4px;
">
    <div style="
        font-size: 13px;
        color: #ff6666;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase;
    ">
        🚨 ACTIVE ALERT PANEL
    </div>
</div>
""", unsafe_allow_html=True)

critical_hazards = []
if flood_percent >= 70:
    critical_hazards.append(("🌊", "FLOOD THREAT", "EXTREME FLOOD RISK DETECTED", flood_percent, "Monitor local water levels and issue an early warning if the trend continues."))
if fire_percent >= 70:
    critical_hazards.append(("🔥", "FIRE THREAT", "EXTREME FIRE RISK DETECTED", fire_percent, "Activate fire monitoring protocols and alert nearby communities."))
if pollution_percent >= 70:
    critical_hazards.append(("🏭", "AIR QUALITY THREAT", "SEVERE AIR QUALITY ALERT", pollution_percent, "Issue air quality alerts and recommend protective measures to residents."))

if critical_hazards:
    for emoji, hazard_type, alert_title, risk_value, recommendation in critical_hazards:
        alert_html = f"""
        <div style="
            background: linear-gradient(135deg, rgba(255, 50, 50, 0.1), rgba(100, 0, 0, 0.1));
            border: 2px solid #ff5555;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        ">
            <div style="
                font-size: 15px;
                font-weight: bold;
                color: #ff6666;
                margin-bottom: 8px;
            ">
                🚨 {emoji} {alert_title}
            </div>
            <div style="
                font-size: 13px;
                color: #ff8888;
                margin-bottom: 10px;
            ">
                Risk Level: <span style="font-weight: bold; color: #ff0000;">{risk_value:.1f}%</span>
            </div>
            <div style="
                font-size: 12px;
                color: #ddd;
                padding: 10px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 4px;
                border-left: 3px solid #ff5555;
            ">
                <strong>Recommended Action:</strong> {recommendation}
            </div>
        </div>
        """
        st.markdown(alert_html, unsafe_allow_html=True)
else:
    safe_html = """
    <div style="
        background: linear-gradient(135deg, rgba(0, 200, 100, 0.1), rgba(0, 100, 50, 0.1));
        border: 2px solid #00dd88;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    ">
        <div style="
            font-size: 18px;
            font-weight: bold;
            color: #00ff88;
            margin-bottom: 4px;
        ">
            ✅ NO CRITICAL HAZARDS DETECTED
        </div>
        <div style="
            font-size: 12px;
            color: #88dd88;
        ">
            All monitored hazards are within acceptable thresholds.
        </div>
    </div>
    """
    st.markdown(safe_html, unsafe_allow_html=True)

# ============================================================================
# SYSTEM STATUS
# ============================================================================

st.markdown("""
<div style="
    margin: 32px 0 16px 0;
    padding: 12px 16px;
    background: rgba(100, 100, 100, 0.08);
    border-left: 4px solid #888888;
    border-radius: 4px;
">
    <div style="
        font-size: 13px;
        color: #888888;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase;
    ">
        ℹ️ SYSTEM STATUS & DIAGNOSTICS
    </div>
</div>
""", unsafe_allow_html=True)

status_cols = st.columns(5)

status_cards = [
    ("NODE ID", "NODE 01", "🖥️"),
    ("AI MODELS", "3 LOADED", "🤖"),
    ("SENSOR SIM", "● ACTIVE", "📡"),
    ("LOCAL INFERENCE", "● ACTIVE", "⚡"),
    ("NETWORK", "STANDBY", "🌐"),
]

for col_idx, (label, value, icon) in enumerate(status_cards):
    with status_cols[col_idx]:
        status_html = f"""
        <div style="
            background: linear-gradient(135deg, rgba(40, 40, 60, 0.9), rgba(30, 30, 50, 0.9));
            border: 1px solid rgba(100, 150, 200, 0.2);
            border-radius: 8px;
            padding: 14px;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        ">
            <div style="font-size: 18px; margin-bottom: 6px;">{icon}</div>
            <div style="font-size: 11px; color: #999; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">{label}</div>
            <div style="font-size: 14px; font-weight: bold; color: #00ff88;">{value}</div>
        </div>
        """
        st.markdown(status_html, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="
    text-align: center;
    color: #555;
    font-size: 11px;
    padding: 24px;
    margin-top: 32px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    letter-spacing: 1px;
">
    Environmental Intelligence Network | Edge Monitoring Node v1.0 | Real-Time AI Risk Assessment
</div>
""", unsafe_allow_html=True)