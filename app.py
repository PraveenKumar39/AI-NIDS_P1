import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from src.predict import NIDSPredictor
import plotly.express as px
import plotly.graph_objects as go
from src.puter_bridge import render_chatbot

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

# Helper Functions (Renderers)

def render_dashboard(predictor):
    st.markdown("## 🚀 Mission Control Center")
    st.markdown("---")
    
    # 1. Top Metrics Cards
    # In a real app, fetch these from DB. Mocking for UI demo.
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">System Status</div>
            <div class="status-safe">Active</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Threats Blocked (24h)</div>
            <div class="metric-value" style="color: #EF553B;">12</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Events Processed</div>
            <div class="metric-value">14.5K</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Current Threat Level</div>
            <div class="status-warning" style="color: black;">ELEVATED</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Main Visuals & Alerts
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("📊 Attack Trend & Severity")
        # Mock Data for Chart
        dates = pd.date_range(end=datetime.now(), periods=7).strftime("%m-%d")
        chart_data = pd.DataFrame({
            "Date": dates,
            "Attacks": [12, 19, 15, 25, 22, 30, 18],
            "Normal": [200, 220, 210, 240, 230, 250, 240]
        })
        fig = px.area(chart_data, x="Date", y=["Normal", "Attacks"], 
                      color_discrete_map={"Normal": "#00CC96", "Attacks": "#EF553B"},
                      template="plotly_dark")
        fig.update_layout(height=350,  margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True, key="attack_trend_chart")
        
    with col_side:
        st.subheader("🚨 Active Correlations")
        try:
            from src.intelligence.correlation import CorrelationEngine
            mock_events = [
                 {"source_ip": "192.168.1.100", "event": "Logon Failed"},
                 {"source_ip": "192.168.1.100", "action": "DENY"},
                 {"source_ip": "10.0.0.55", "event": "Malware Detected"}
            ]
            engine = CorrelationEngine()
            alerts = engine.correlate(mock_events)
            
            if alerts:
                for alert in alerts:
                    st.error(f"**{alert['name']}**")
                    st.caption(f"IP: {alert['source_ip']} | {alert['severity']}")
                    with st.expander("Details"):
                        st.write(alert['details'])
                        if st.button("Investigate", key=alert['source_ip']):
                             st.session_state['page'] = 'SOAR & Response' # Theoretical navigation
                             st.rerun()
            else:
                st.info("No active correlation alerts.")
                
        except Exception as e:
            st.error(f"Correlation Engine Error: {e}")
            
    # 3. Recent Activity Table
    st.subheader("Recent High-Severity Events")
    mock_log_data = pd.DataFrame({
        "Timestamp": [datetime.now().strftime("%H:%M:%S"), "10 mins ago", "1 hour ago"],
        "Source": ["Firewall", "EDR", "Auth"],
        "Event": ["Block 192.168.1.100", "Malware Quarantined", "Admin Login Failed"],
        "Severity": ["High", "Critical", "Medium"]
    })
    st.dataframe(mock_log_data, use_container_width=True, hide_index=True)

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
    st.markdown("---")
    st.subheader("GenAI Alert Analysis")
    
    col_ai1, col_ai2 = st.columns(2)
    
    with col_ai1:
        alert_type = st.selectbox("Select Alert to Analyze", ["Brute Force Attack", "Malware Detection", "Data Exfiltration"])
        # Mock context based on selection
        context = {}
        if "Brute Force" in alert_type:
            context = {"ip": "192.168.1.100", "user": "admin", "count": 15}
        elif "Malware" in alert_type:
            context = {"host": "WORKSTATION-01", "file": "invoice.exe.vbs"}
        else:
            context = {"ip": "45.33.22.11", "user": "bob", "size": "5GB"}
            
        st.json(context)
        
    with col_ai2:
        if st.button("Generate Analysis"):
            with st.spinner("Analyzing with GenAI..."):
                try:
                    from src.intelligence.genai_analyst import GenAIAnalyst
                    analyst = GenAIAnalyst()
                    analysis = analyst.generate_analysis(alert_type, context)
                    
                    st.success("Analysis Complete")
                    st.markdown(f"**Explanation:** {analysis['summary']}")
                    st.markdown("**Remediation Steps:**")
                    for step in analysis['steps']:
                        st.markdown(f"- {step}")
                except Exception as e:
                    st.error(f"GenAI Error: {e}")

    st.markdown("---")
    st.info("💡 Powered by Puter.js (No API Key Required)")
    from src.puter_bridge import render_chatbot
    render_chatbot()

    st.markdown("---")
    st.subheader("Compliance Reporting")
    
    if st.button("Generate Daily Security Report (HTML)"):
        try:
            from src.reporting.generator import ReportGenerator
            import os
            
            # Mock data for report
            mock_alerts = [
                {"severity": "High", "name": "Brute Force", "source_ip": "192.168.1.100", "timestamp": "2026-02-14 18:30:00"},
                {"severity": "Critical", "name": "Malware C2", "source_ip": "10.0.0.55", "timestamp": "2026-02-14 14:20:00"}
            ]
            mock_actions = [
                {"action": "Block_IP", "target": "192.168.1.100", "status": "Success", "executor": "System_Auto"},
                {"action": "Isolate_Host", "target": "WORKSTATION-01", "status": "Success", "executor": "Admin_User"}
            ]
            
            report_gen = ReportGenerator()
            report_path = report_gen.generate_html_report(mock_alerts, mock_actions)
            
            with open(report_path, "rb") as file:
                btn = st.download_button(
                    label="Download Report",
                    data=file,
                    file_name=os.path.basename(report_path),
                    mime="text/html"
                )
            st.success(f"Report generated: {os.path.basename(report_path)}")
            
        except Exception as e:
            st.error(f"Reporting Error: {e}")
    st.markdown("---")
    st.markdown("Ask questions about the system, attacks, or how to interpret the results.")
    st.info("💡 Powered by Puter.js (No API Key Required)")

    from src.puter_bridge import render_chatbot
    render_chatbot()

def render_siem(predictor):
    st.title("🔎 SIEM Explorer")
    st.markdown("Analyze raw logs from various sources (Firewall, Windows, etc.)")
    
    # Tabs for different sources
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Firewall", "Windows Events", "Identity (Auth)", "Web Server", "Database", 
        "Cloud Audit", "Security Tools", "Collaboration"
    ])
    
    with tab1:
        st.subheader("Firewall Traffic")
        try:
            from src.collectors.network.firewall import FirewallCollector
            collector = FirewallCollector(log_path="firewall.log")
            logs = collector.collect()
            if logs:
                df = pd.DataFrame(logs)
                
                # Filters
                with st.expander("🔍 Filter Logs", expanded=True):
                    c1, c2 = st.columns(2)
                    actions = ["All"] + list(df['action'].unique())
                    selected_action = c1.selectbox("Action", actions)
                    
                    if selected_action != "All":
                        df = df[df['action'] == selected_action]
                        
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No firewall logs found.")
        except Exception as e:
            st.error(f"Error: {e}")

    with tab2:
        st.subheader("Windows Security Events")
        try:
            from src.collectors.endpoint.windows import WindowsEventCollector
            import platform
            if platform.system() != "Windows":
                st.warning("Windows Event Logs are only available on Windows hosts.")
            else:
                collector = WindowsEventCollector()
                logs = collector.collect()
                if logs:
                    st.dataframe(pd.DataFrame(logs), use_container_width=True)
                else:
                    st.info("No recent security events found or permission denied.")
        except Exception as e:
            st.error(f"Error loading Windows logs: {e}")

    with tab3:
        st.subheader("Identity & Access Management")
        try:
            from src.collectors.auth.ad_collector import AuthCollector
            collector = AuthCollector()
            logs = collector.collect()
            if logs:
                df = pd.DataFrame(logs)
                st.dataframe(df, use_container_width=True)
                
                # Metrics
                failed = len(df[df['event'] == 'Logon Failed'])
                st.metric("Failed Logins", failed, delta_color="inverse")
            else:
                st.info("No auth logs collected yet.")
        except Exception as e:
            st.error(f"Error: {e}")

    with tab4:
        st.subheader("Web Server Access Logs")
        try:
            from src.collectors.application.web_collector import WebLogCollector
            collector = WebLogCollector()
            logs = collector.collect()
            if logs:
                df = pd.DataFrame(logs)
                st.dataframe(df, use_container_width=True)
                
                # Status Code Chart
                fig = px.pie(df, names='status', title='HTTP Status Codes')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No web logs collected yet.")
        except Exception as e:
            st.error(f"Error: {e}")

    with tab5:
        st.subheader("Database Audit Logs")
        try:
            from src.collectors.data.db_collector import DatabaseCollector
            collector = DatabaseCollector()
            logs = collector.collect()
            if logs:
                st.dataframe(pd.DataFrame(logs), use_container_width=True)
            else:
                st.info("No database logs collected yet.")
        except Exception as e:
            st.error(f"Error: {e}")

    with tab6:
        st.subheader("Cloud Audit (AWS/Azure/GCP)")
        try:
            from src.collectors.cloud.cloud_audit import CloudCollector
            collector = CloudCollector()
            logs = collector.collect()
            if logs:
                df = pd.DataFrame(logs)
                st.dataframe(df, use_container_width=True)
                # Cloud Map
                st.map(pd.DataFrame({'lat': [37.77, 51.50, 19.07], 'lon': [-122.41, -0.12, 72.87]})) # Mock locations for implemented regions
            else:
                st.info("No cloud logs collected yet.")
        except Exception as e:
            st.error(f"Error: {e}")

    with tab7:
        st.subheader("Security Tools (EDR/AV)")
        try:
            from src.collectors.security.edr_collector import SecurityToolCollector
            collector = SecurityToolCollector()
            logs = collector.collect()
            if logs:
                df = pd.DataFrame(logs)
                st.dataframe(df, use_container_width=True)
                
                # Critical Threats
                critical = df[df['action_taken'] == 'Alert Only']
                if not critical.empty:
                    st.error(f"⚠️ {len(critical)} Threats Require Immediate Attention!")
            else:
                st.info("No security alerts collected (System Safe).")
        except Exception as e:
            st.error(f"Error: {e}")

    with tab8:
        st.subheader("Email & Collaboration")
        try:
            from src.collectors.collaboration.email_collector import CollaborationCollector
            collector = CollaborationCollector()
            logs = collector.collect()
            if logs:
                st.dataframe(pd.DataFrame(logs), use_container_width=True)
            else:
                st.info("No collaboration logs collected yet.")
        except Exception as e:
            st.error(f"Error: {e}")
    st.markdown("Ask questions about the system, attacks, or how to interpret the results.")
    st.info("💡 Powered by Puter.js (No API Key Required)")

    from src.puter_bridge import render_chatbot
    render_chatbot()

    # --- Response & Intel Modules ---
    
def render_intelligence():
    st.title("🧠 Threat Intelligence Feeds")
    st.markdown("Query internal and external threat databases.")
    
    col_q1, col_q2 = st.columns(2)
    
    with col_q1:
        search_term = st.text_input("Enter IP, Domain, or Hash")
        
    with col_q2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("Check Reputation", type="primary")
        
    if search_btn and search_term:
        try:
            from src.intelligence.threat_intel import ThreatIntel
            intel = ThreatIntel()
            
            # Simple heuristic detection for demo
            if "." in search_term and not search_term.replace(".", "").isdigit():
                result = intel.check_domain(search_term)
            else:
                result = intel.check_ip(search_term)
                
            if result['match']:
                st.error(f"❌ Malicious Indicator Found: {result['type']}")
                st.write(f"**Severity:** {result['severity']}")
                st.write(f"**Details:** {result['details']}")
            else:
                st.success("✅ No Threat Found in Database")
                
        except Exception as e:
            st.error(f"Intel Error: {e}")
            
    st.markdown("### 📋 Known Threats Feed")
    # Mock feed display
    st.dataframe(pd.DataFrame([
        {"IOC": "192.168.1.55", "Type": "C2", "Confidence": "High", "Source": "Internal"},
        {"IOC": "evil-bank-login.com", "Type": "Phishing", "Confidence": "Critical", "Source": "External"},
        {"IOC": "45.33.22.11", "Type": "Botnet", "Confidence": "Medium", "Source": "CrowdStrike"}
    ]), use_container_width=True)

    st.markdown("---")
    st.info("💡 Powered by Puter.js (No API Key Required)")
    from src.puter_bridge import render_chatbot
    render_chatbot()

def render_soar():
    st.title("🛡️ SOAR Orchestration")
    st.markdown("Execute automated responses and track remediation actions.")
    
    # Init SOAR State
    if 'soar_manager' not in st.session_state:
        try:
            from src.response.actions import ResponseManager
            st.session_state.soar_manager = ResponseManager()
        except Exception as e:
            st.error(f"Failed to init SOAR: {e}")
            return

    manager = st.session_state.soar_manager
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("🚀 Execute Playbook")
        action = st.selectbox("Select Action", ["Block_IP", "Disable_User", "Isolate_Host"])
        target = st.text_input("Target (IP/User/Host)")
        
        if st.button("Execute Response"):
            if target:
                with st.spinner("Executing Playbook..."):
                    time.sleep(1) # Sim
                    res = manager.execute_action(action, target, "Admin_Console")
                    if res['status'] == "Success":
                        st.success(res['message'])
                    else:
                        st.error(res['message'])
            else:
                st.warning("Please specify a target.")
                
    with c2:
        st.subheader("📜 Action History")
        history = manager.get_history()
        if history:
            st.dataframe(pd.DataFrame(history), use_container_width=True)
        else:
            st.info("No actions recorded yet.")

    st.markdown("---")
    st.info("💡 Powered by Puter.js (No API Key Required)")
    from src.puter_bridge import render_chatbot
    render_chatbot()

def main():
    # Sidebar
    st.sidebar.title("🛡️ AI-NIDS")
    st.sidebar.markdown("---")
    
    # Load Predictor Globally
    predictor = load_predictor()
    
    # --- Phase 8: Self-Defense Modules ---
    
    # 1. Integrity Monitor (Runs on Startup)
    if 'integrity_checked' not in st.session_state:
         try:
             from src.security.integrity import IntegrityMonitor
             monitor = IntegrityMonitor()
             if not monitor.baseline: 
                 monitor.build_baseline()
             compromised = monitor.check_integrity()
             st.session_state['integrity_checked'] = True
             if compromised:
                 st.error("🚨 CRITICAL SYSTEM ALTERATION DETECTED!")
                 for issue in compromised:
                     st.warning(f"File {issue['status']}: {issue['file']}")
         except Exception as e:
             st.error(f"Security Module Error: {e}")

    # 2. Login Rate Limiting (Simulation)
    if 'auth_guard' not in st.session_state:
        from src.security.auth import AuthGuard
        st.session_state.auth_guard = AuthGuard()
        
    with st.sidebar.expander("🔐 Admin Login (Simulated)"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            ip = "192.168.1.55" 
            guard = st.session_state.auth_guard
            is_locked, remaining = guard.is_locked_out(ip)
            if is_locked:
                st.error(f"⛔ IP Locked! Try again in {int(remaining)}s")
            else:
                if username == "admin" and password == "secure123":
                    st.success("Access Granted")
                    guard.record_attempt(ip, True)
                else:
                    st.error("Invalid Credentials")
                    should_lock = guard.record_attempt(ip, False)
                    if should_lock:
                         st.error(f"⛔ Locked!")

    st.sidebar.info("System Status: **Active**")
    
    # 3. Internal Honeypot
    if st.sidebar.button("⚙️ Admin Backup (Legacy)", help="Do not touch"):
        st.sidebar.error("🚨 HONEYPOT TRIGGERED! IP BANNED.")

    st.sidebar.markdown("---")
    
    # --- Main Navigation ---
    
    # Use session state to track current page if needed, but for now simple radio is fine.
    # We use a top-level selection for Mode, then sub-selection for View.
    
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        selected_section = st.radio("Section", ["Overview", "Investigation", "Response"], label_visibility="collapsed")
        
        st.markdown("---")
        
    if selected_section == "Overview":
        st.sidebar.markdown("### 📡 Views")
        view = st.sidebar.radio("Go to", ["Mission Control", "Live Traffic", "System Health"])
        
        if view == "Mission Control":
            render_dashboard(predictor)
        elif view == "Live Traffic":
            render_analysis(predictor)
        elif view == "System Health":
            render_health()
            
    elif selected_section == "Investigation":
        st.sidebar.markdown("### 🔍 Views")
        view = st.sidebar.radio("Go to", ["SIEM Explorer", "Threat Intel"])
        
        if view == "SIEM Explorer":
            render_siem(predictor)
        elif view == "Threat Intel":
            render_intelligence()
            
    elif selected_section == "Response":
        st.sidebar.markdown("### 🛡️ Views")
        view = st.sidebar.radio("Go to", ["SOAR Operations", "AI Analyst"])
        
        if view == "SOAR Operations":
            render_soar()
        elif view == "AI Analyst":
            run_chatbot()
            
    # Global Footer / Chatbot
    st.markdown("---")
    render_chatbot()

if __name__ == "__main__":
    main()
