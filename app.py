import streamlit as st
import pandas as pd
import numpy as np
import time
from src.predict import NIDSPredictor
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="AI-NIDS Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium" look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #f0f2f6;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #41444e;
        text-align: center;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #00CC96;
    }
    .metric-label {
        font-size: 1em;
        color: #a0a0a0;
    }
    .status-safe {
        background-color: #00cc96;
        color: black;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .status-warning {
        background-color: #ffa15a;
        color: black;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .status-critical {
        background-color: #ef553b;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def load_predictor():
    """Singleton style loading of predictor"""
    if 'predictor' not in st.session_state:
        try:
            st.session_state.predictor = NIDSPredictor()
        except Exception as e:
            st.error(f"Failed to load model: {e}")
            return None
    return st.session_state.predictor

def main():
    # Sidebar
    st.sidebar.title("🛡️ AI-NIDS")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio("Navigation", ["Dashboard", "Real-time Analysis", "System Health"])
    
    st.sidebar.markdown("---")
    st.sidebar.info("System Status: **Active**")
    
    predictor = load_predictor()

    if page == "Dashboard":
        render_dashboard(predictor)
    elif page == "Real-time Analysis":
        render_analysis(predictor)
    elif page == "System Health":
        render_health()

def render_dashboard(predictor):
    st.title("Network Security Overview")
    
    # Simulate or show last batch stats (placeholder logic for demo)
    # In a real app, this would pull from a database
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">Active</div><div class="metric-label">System Status</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">0</div><div class="metric-label">Threats (24h)</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">100%</div><div class="metric-label">Uptime</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">Low</div><div class="metric-label">Current Risk</div></div>', unsafe_allow_html=True)

    st.markdown("### 📊 Recent Traffic Activity")
    # Placeholder chart
    df = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
    st.line_chart(df)

def render_analysis(predictor):
    st.title("🕵️ Real-time Traffic Analysis")
    
    uploaded_file = st.file_uploader("Upload Network Traffic Capture (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(df)} packets successfully.")
            
            if st.button("Analyze Traffic", type="primary"):
                with st.spinner("Analyzing packets with Random Forest Model..."):
                    # Simulate processing time for effect
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    # Predict
                    results = predictor.predict(df)
                    
                    if isinstance(results, dict) and "error" in results:
                        st.error(results["error"])
                        return
                        
                    # Add results to DF
                    results_df = pd.DataFrame(results)
                    final_df = pd.concat([df.reset_index(drop=True), results_df], axis=1)
                    
                    # Metrics
                    total_packets = len(final_df)
                    threats = final_df[final_df['Attack Prediction'] != 'BENIGN'].shape[0]
                    safe = total_packets - threats
                    
                    # System Status Indicator
                    critical_count = final_df[final_df['Severity'] == 'Critical'].shape[0]
                    high_count = final_df[final_df['Severity'] == 'High'].shape[0]
                    
                    if critical_count > 0:
                        status_html = '<div class="status-critical">🚨 CRITICAL THREATS DETECTED</div>'
                    elif high_count > 0:
                        status_html = '<div class="status-warning">⚠️ HIGH RISK DETECTED</div>'
                    else:
                        status_html = '<div class="status-safe">✅ SYSTEM SAFE</div>'
                        
                    st.markdown("### Analysis Results")
                    st.markdown(status_html, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Top Metrics
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Total Packets", total_packets)
                    m2.metric("Threats Detected", threats, delta_color="inverse")
                    m3.metric("Safe Traffic", safe)
                    
                    # Visualizations
                    row1_1, row1_2 = st.columns(2)
                    
                    with row1_1:
                        st.subheader("Attack Type Distribution")
                        fig_bar = px.bar(final_df['Attack Prediction'].value_counts(), orientation='h', 
                                         color_discrete_sequence=['#00CC96'])
                        st.plotly_chart(fig_bar, use_container_width=True)
                        
                    with row1_2:
                        st.subheader("Severity Breakdown")
                        fig_donut = px.pie(final_df, names='Severity', hole=0.5, 
                                           color='Severity',
                                           color_discrete_map={
                                               'Safe': '#00CC96', 
                                               'Medium': '#FFA15A', 
                                               'High': '#FF6692', 
                                               'Critical': '#EF553B'
                                           })
                        st.plotly_chart(fig_donut, use_container_width=True)
                    
                    # Detailed Table
                    st.subheader("Detailed Logs")
                    st.dataframe(final_df)
                    
        except Exception as e:
            st.error(f"Error processing file: {e}")

def render_health():
    st.title("🏥 System Health")
    st.write("Model Status: **Loaded**")
    st.write(f"Model Path: `{st.session_state.predictor.model_path}`")
    st.write("Prediction Engine: **v1.0**")

# --- AI Assistant ---
def run_chatbot():
    st.header("🤖 AI Security Analyst")
    st.markdown("Ask questions about the system, attacks, or how to interpret the results.")
    st.info("💡 Powered by Puter.js (No API Key Required)")

    from src.puter_bridge import render_chatbot
    render_chatbot()

def main():
    # Sidebar
    st.sidebar.title("🛡️ AI-NIDS")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio("Navigation", ["Dashboard", "Real-time Analysis", "System Health", "AI Assistant"])
    
    st.sidebar.markdown("---")
    st.sidebar.info("System Status: **Active**")
    
    predictor = load_predictor()

    if page == "Dashboard":
        render_dashboard(predictor)
    elif page == "Real-time Analysis":
        render_analysis(predictor)
    elif page == "System Health":
        render_health()
    elif page == "AI Assistant":
        run_chatbot()

if __name__ == "__main__":
    main()
