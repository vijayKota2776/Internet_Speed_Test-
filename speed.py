import streamlit as st
import speedtest
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import os

# Initialize session state for history
if 'test_history' not in st.session_state:
    st.session_state.test_history = []

# Function to test internet speed
def test_speed():
    speed = speedtest.Speedtest()
    speed.get_best_server()
    
    ping = round(speed.results.ping, 2)
    download_speed = round(speed.download() / (1024 * 1024), 2)
    upload_speed = round(speed.upload() / (1024 * 1024), 2)
    isp = speed.config['client']['isp']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.session_state.test_history.append([timestamp, download_speed, upload_speed, ping, isp])
    return timestamp, download_speed, upload_speed, ping, isp

# Streamlit UI
st.set_page_config(page_title="Internet Speed Test", layout="wide")
st.title("🌐 Internet Speed Test")

# Sidebar for theme selection
st.sidebar.title("🎨 Choose Theme")
theme = st.sidebar.radio("Select a theme:", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
            body { background-color: black; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Run Speed Test Button
if st.button("🚀 Start Speed Test"):
    timestamp, download_speed, upload_speed, ping, isp = test_speed()
    st.success("✅ Test Completed!")
    
    # Display Results
    st.metric(label="📥 Download Speed", value=f"{download_speed} Mbps")
    st.metric(label="📤 Upload Speed", value=f"{upload_speed} Mbps")
    st.metric(label="📡 Ping", value=f"{ping} ms")
    st.metric(label="🏢 ISP", value=isp)
    
    # Display ISP Logo if available
    logo_path = "isp_logo.png"
    if os.path.exists(logo_path):
        st.image(Image.open(logo_path), caption=f"ISP: {isp}", width=100)
    
    # Save history to a CSV file
    df = pd.DataFrame(st.session_state.test_history, columns=["Timestamp", "Download Speed", "Upload Speed", "Ping", "ISP"])
    df.to_csv("speed_test_history.csv", index=False)

# Display Last 5 Tests
st.subheader("📜 Test History (Last 5)")
if len(st.session_state.test_history) > 0:
    df_history = pd.DataFrame(st.session_state.test_history[-5:], columns=["Timestamp", "Download Speed", "Upload Speed", "Ping", "ISP"])
    st.table(df_history)

# Plot Speed Trends
if len(st.session_state.test_history) > 1:
    st.subheader("📈 Speed Trends Over Time")
    df_trends = pd.DataFrame(st.session_state.test_history, columns=["Timestamp", "Download Speed", "Upload Speed", "Ping", "ISP"])
    fig, ax = plt.subplots()
    ax.plot(df_trends['Timestamp'], df_trends['Download Speed'], marker='o', linestyle='-', color='b', label='Download Speed')
    ax.set_xlabel("Time")
    ax.set_ylabel("Speed (Mbps)")
    ax.legend()
    st.pyplot(fig)

# Download History CSV
st.subheader("💾 Download Test History")
st.download_button(label="📥 Download CSV", data=pd.DataFrame(st.session_state.test_history, columns=["Timestamp", "Download Speed", "Upload Speed", "Ping", "ISP"]).to_csv(index=False), file_name="speed_test_history.csv", mime="text/csv")