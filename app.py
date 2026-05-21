import streamlit as st
import pandas as pd
import requests
from google import genai
from google.genai import types
import time

# 1. System Layout & Window Customization
st.set_page_config(
    page_title="Datov Enterprise System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Corporate Dark-Theme CSS Inject
st.markdown("""
    <style>
    .metric-card { background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; text-align: center; }
    .metric-val { font-size: 28px; font-weight: bold; color: #38bdf8; }
    .file-card { background-color: #0f172a; padding: 12px; border-radius: 6px; border-left: 4px solid #38bdf8; margin-bottom: 10px; }
    .page-header { color: #38bdf8; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Navigation and Configuration Panel
with st.sidebar:
    st.title("🌐 Datov Portal")
   
    # NEW MULTI-PAGE NAVIGATION INTERFACE
    current_page = st.radio(
        "📂 Select Platform Module",
        ["🛡️ QA Audit Hub", "📚 Procedures Library", "📈 Analytics History"]
    )
   
    st.divider()
    st.header("⚙️ Core Engine Settings")
   
    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = ""
       
    api_input = st.text_input("🔑 Gemini API Key", type="password", value=st.session_state["gemini_api_key"])
    if api_input:
        st.session_state["gemini_api_key"] = api_input

    st.divider()
    st.subheader("📋 Active Profile")
    project_uid = st.text_input("System Identifier", value="DATOV_CORE_MODULE")
    target_model = st.selectbox("AI Model Core", ["gemini-2.5-flash", "gemini-2.5-pro"])
    temperature = st.slider("Strictness Variance", min_value=0.0, max_value=1.0, value=0.05, step=0.05)


# =========================================================================
# PAGE 1: CORE QA AUDIT HUB
# =========================================================================
if current_page == "🛡️ QA Audit Hub":
    st.title("🛡️ Datov Enterprise QA Audit Platform")
    st.caption("Industrial Automated Metric Verification, Regression Mapping, and Technical Solution Blueprint Engine.")
    st.markdown("---")

    col_inputs, col_results = st.columns([1, 1.3], gap="large")

    with col_inputs:
        st.subheader("📥 Data Intake Engine")
        st.markdown("### 📋 System Requirements Criteria")
       
        # If user has saved a procedure in session state, load it automatically
        default_specs = st.session_state.get("selected_sop_text", "Example:\nREQ-1: Auth tokens must be encrypted.\nREQ-2: Gateway latency must remain under 200ms.")
        expected_specs = st.text_area(
            "Define Objective Engineering Standards / Acceptance Criteria:",
            value=default_specs,
            height=180,
            key="specs_input"
        )
       
        st.divider()
        st.markdown("### 📂 Document Upload Portal")
        uploaded_files = st.file_uploader(
            "Batch drag-and-drop log files here (.txt, .log, .json, .csv)",
            type=["txt", "log", "json", "csv"],
            accept_multiple_files=True
        )
       
        manual_logs = st.text_area(
            "Or manually input raw terminal log entries here:",
            placeholder="Enter manual data here...",
            height=120,
            key="logs_input"
        )
       
        parsed_logs_payload = ""
        if uploaded_files:
            st.markdown("###### 📦 Active File Inventory Manifest")
            for f in uploaded_files:
                file_contents = f.read().decode("utf-8")
                parsed_logs_payload += f"\n--- SOURCE FILE: {f.name} ---\n{file_contents}\n"
                st.markdown(f'<div class="file-card"><strong>📄 {f.name}</strong><br><small style="color:#94a3b8;">Size: {round(f.size/1024, 2)} KB</small></div>', unsafe_allow_html=True)
        else:
            parsed_logs_payload = manual_logs

        st.divider()
        execute_btn = st.button("🚀 Run Comprehensive Datov QA Audit", use_container_width=True, type="primary")

    with col_results:
        st.subheader("📊 Datov Execution Readouts")
       
        if execute_btn:
            if not st.session_state["gemini_api_key"]:
                st.error("🔒 Security Key Required: Please enter your valid Gemini API Key inside the sidebar configuration window before running the audit pipeline.")
            elif not expected_specs.strip() or not parsed_logs_payload.strip():
                st.error("🛑 Intake System Mismatch: Both requirements criteria and log inputs are required.")
            else:
                with st.status("Analyzing system telemetry alignment...", expanded=True) as status_container:
                    client = genai.Client(api_key=st.session_state["gemini_api_key"])
                   
                    system_instructions = (
                        "You are an elite automated system QA auditor working inside the Datov Ecosystem.\n"
                        "Evaluate the data and structure your response with clear Markdown headers:\n\n"
                        "### 1. Requirements Discrepancy Matrix\n"
                        "(Provide a Markdown table: Requirement ID | Expected | Observed | Status [PASSED/FAILED])\n\n"
                        "### 2. Technical Engineering Solutions\n"
                        "(Provide copy-pasteable script or config blocks to fix any failures)\n\n"
                        "### 3. Formal System Documentation\n"
                        "(A brief professional summary tracking compliance recommendations)"
                    )
                   
                    user_payload = f"Project Context: {project_uid}\n\n[CRITERIA]:\n{expected_specs}\n\n[LOGS]:\n{parsed_logs_payload}"
                   
                    try:
                        status_container.update(label="Engaging Gemini generative reasoning arrays...", state="running")
                        start_time = time.time()
                       
                        response = client.models.generate_content(
                            model=target_model,
                            contents=user_payload,
                            config=types.GenerateContentConfig(
                                system_instruction=system_instructions,
                                temperature=temperature,
                            ),
                        )
                       
                        execution_delta = round(time.time() - start_time, 2)
                        raw_audit_report = response.text
                       
                        status_container.update(label="Analysis Pipeline Completed!", state="complete")
                       
                        m_col1, m_col2 = st.columns(2)
                        with m_col1:
                            st.markdown(f'<div class="metric-card"><small style="color:#94a3b8;">COMPUTE LATENCY</small><div class="metric-val">{execution_delta}s</div></div>', unsafe_allow_html=True)
                        with m_col2:
                            st.markdown(f'<div class="metric-card"><small style="color:#94a3b8;">PARSED RUN PACKETS</small><div class="metric-val">{len(uploaded_files) if uploaded_files else 1} Source(s)</div></div>', unsafe_allow_html=True)
                           
                        st.success("🎉 Compliance evaluation concluded successfully.")
                        st.markdown("---")
                        st.markdown(raw_audit_report)
                       
                        st.divider()
                        st.download_button(
                            label="📥 Download Enterprise Markdown Audit Report Manifest (.md)",
                            data=raw_audit_report,
                            file_name=f"DATOV_QA_REPORT_{project_uid}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                       
                    except Exception as e:
                        status_container.update(label="Critical System Interrupt", state="error")
                        st.error(f"Ecosystem Evaluation Pipeline Interrupted: {str(e)}")
        else:
            st.info("💡 System Awaiting Inbound Data Feed. Populate your criteria specifications and drop your files on the left panel, then hit the run button to stream your analysis report.")

# =========================================================================
# PAGE 2: PROCEDURES LIBRARY DATABASE
# =========================================================================
elif current_page == "📚 Procedures Library":
    st.title("📚 Datov Standard Operating Procedures (SOP) Database")
    st.caption("Store, manage, and load permanent corporate manuals or compliance checklist requirements.")
    st.markdown("---")
  
    st.subheader("📁 Central Requirements Repository")
  
    # EXISTING MOCK DATABASE
    mock_sop_db = {
        "ISO-9001 Quality Management Standards": (
            "SOP-ISO-01: Document tracking validation must register owner IDs.\n"
            "SOP-ISO-02: All sub-system code deployment cycles require continuous data backups.\n"
            "SOP-ISO-03: Security auditing protocols must flag plain-text credentials."
        ),
        "SOC2 Compliance Security Protocol": (
            "SOP-SOC-01: Network infrastructure routes must force SSL/TLS endpoint encryption.\n"
            "SOP-SOC-02: Data at rest inside relational tables must obscure user email addresses.\n"
            "SOP-SOC-03: System failure log blocks must generate active telemetry tracing alerts."
        ),
        "Standard Developer Release Checklist": (
            "SOP-DEV-01: API request execution time must remain consistently beneath 200ms.\n"
            "SOP-DEV-02: All incoming request payloads must pass standard JSON validation filters."
        )
    }
  
    selected_sop = st.selectbox("Select a Procedure to inspect or load:", list(mock_sop_db.keys()))
  
    st.markdown("### 📋 Rulebook Content Preview")
    st.code(mock_sop_db[selected_sop], language="text")
  
    if st.button("⚡ Inject Selected Procedure into Active Audit Hub Workspace", type="primary", use_container_width=True):
        st.session_state["selected_sop_text"] = mock_sop_db[selected_sop]
        st.success(f"✅ Success! '{selected_sop}' has been loaded into your working memory. Click on '🛡️ QA Audit Hub' in the sidebar to view it.")

    # ADDITION: GitHub Assets Repository
    st.markdown("---")
    st.subheader("🌐 GitHub Assets Repository")
   
    # Ensure 'requests' is imported at the top of your app.py
    api_url = "https://api.github.com/repos/TCG-eng/Objective-QA-Auditor/contents/assets"
    response = requests.get(api_url)
   
    if response.status_code == 200:
        files = response.json()
        docs = {f['name']: f['download_url'] for f in files if f['name'].endswith(('.txt', '.md'))}
       
        selected_git = st.selectbox("Select document from GitHub:", list(docs.keys()))
       
        if st.button("📥 Load GitHub Document"):
            content_resp = requests.get(docs[selected_git])
            st.session_state["selected_sop_text"] = content_resp.text
            st.success(f"✅ '{selected_git}' loaded from GitHub!")
           
        if st.button("🔄 Reset Workspace"):
            st.session_state.pop("selected_sop_text", None)
            st.rerun()
    else:
        st.error(f"GitHub connection failed with status: {response.status_code}. Ensure the 'assets' folder exists at the root of your repo.")
# =========================================================================
# PAGE 3: ANALYTICS PERFORMANCE HISTORY
# =========================================================================
elif current_page == "📈 Analytics History":
    st.title("📈 Datov Compliance Analytics & Operations Metrics")
    st.caption("Monitor real-time system performance, historical success distributions, and audit cycle volumes.")
    st.markdown("---")
   
    # Metric cards display
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="metric-card"><small style="color:#94a3b8;">TOTAL COMPLETED AUDITS</small><div class="metric-val">142 Runs</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="metric-card"><small style="color:#94a3b8;">GLOBAL SYSTEM COMPLIANCE RATE</small><div class="metric-val" style="color:#10b981;">91.4%</div></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="metric-card"><small style="color:#94a3b8;">AVG ENGINE COMPUTE VELOCITY</small><div class="metric-val" style="color:#a78bfa;">1.44s</div></div>', unsafe_allow_html=True)
   
    st.divider()
    st.subheader("📊 Audit Volume Trends (Last 7 Days)")
   
    # Basic DataFrame to generate an interactive bar chart readout
    chart_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Audit Runs Completed": [12, 18, 15, 22, 29, 8, 3]
    })
   
    st.bar_chart(chart_data, x="Day", y="Audit Runs Completed", color="#38bdf8")
