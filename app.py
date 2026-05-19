import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import time

# 1. System Layout & Window Customization
st.set_page_config(
    page_title="Datov Enterprise QA Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Corporate Dark-Theme CSS Inject
st.markdown("""
    <style>
    .metric-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #334155;
        text-align: center;
    }
    .metric-val {
        font-size: 28px;
        font-weight: bold;
        color: #38bdf8;
    }
    .file-card {
        background-color: #0f172a;
        padding: 12px;
        border-radius: 6px;
        border-left: 4px solid #38bdf8;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Branding Header
st.title("🛡️ Datov Enterprise QA Audit Platform")
st.caption("Industrial Automated Metric Verification, Regression Mapping, and Technical Solution Blueprint Engine.")
st.markdown("---")

# 2. Sidebar Administration Panel
with st.sidebar:
    st.header("⚙️ Core Engine Settings")
   
    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = ""
       
    api_input = st.text_input("🔑 Gemini API Key", type="password", value=st.session_state["gemini_api_key"])
    if api_input:
        st.session_state["gemini_api_key"] = api_input

    st.divider()
    st.subheader("📋 Audit Blueprint Profiles")
    project_uid = st.text_input("System Identifier", value="DATOV_CORE_MODULE")
    target_model = st.selectbox("AI Model Core", ["gemini-2.5-flash", "gemini-2.5-pro"])
    temperature = st.slider("Strictness / Precision Variance", min_value=0.0, max_value=1.0, value=0.05, step=0.05)
   
    st.divider()
    st.markdown("### 🔍 Filter Scope Vectors")
    v1 = st.checkbox("Performance Latency Checks", value=True)
    v2 = st.checkbox("Security / PII Encryption Checks", value=True)
    v3 = st.checkbox("Functional Logical Gaps", value=True)
   
    active_vectors = []
    if v1: active_vectors.append("Performance Latency")
    if v2: active_vectors.append("Security & PII Mapping")
    if v3: active_vectors.append("Functional Gaps")

# 3. Security Access Lock
if not st.session_state["gemini_api_key"]:
    st.warning("🔒 Datov Cluster Awaiting Authentication: Please enter a valid Gemini API Key in the sidebar settings panel to launch core compute pipelines.")
else:
    client = genai.Client(api_key=st.session_state["gemini_api_key"])

    # 4. Two-Column System Splitter
    col_inputs, col_results = st.columns([1, 1.3], gap="large")

    # ==================== LEFT PANEL: DATA FEED PIPELINE ====================
    with col_inputs:
        st.subheader("📥 Data Intake Engine")
       
        tab_spec, tab_upload = st.tabs(["📋 System Requirements Criteria", "📂 Multi-File Telemetry Intake"])
       
        with tab_spec:
            expected_specs = st.text_area(
                "Define Objective Engineering Standards / Acceptance Criteria:",
                placeholder="Example:\nREQ-1: Auth tokens must be encrypted.\nREQ-2: Gateway latency must remain under 200ms.",
                height=300,
                key="specs_input"
            )
       
        with tab_upload:
            st.markdown("##### Advanced Upload Capabilities")
            uploaded_files = st.file_uploader(
                "Batch drag-and-drop log files here (.txt, .log, .json, .csv)",
                type=["txt", "log", "json", "csv"],
                accept_multiple_files=True
            )
           
            manual_logs = st.text_area(
                "Or manually input raw terminal log entries here:",
                placeholder="[DEBUG] Payload mismatch detected...",
                height=150,
                key="logs_input"
            )
           
            parsed_logs_payload = ""
            if uploaded_files:
                st.markdown("###### 📦 Active File Inventory Manifest")
                for f in uploaded_files:
                    file_contents = f.read().decode("utf-8")
                    parsed_logs_payload += f"\n--- SOURCE FILE: {f.name} ---\n{file_contents}\n"
                   
                    st.markdown(f"""
                        <div class="file-card">
                            <strong>📄 {f.name}</strong><br>
                            <small style="color:#94a3b8;">Size: {round(f.size/1024, 2)} KB | Ready for Ingestion</small>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                parsed_logs_payload = manual_logs

        st.divider()
        execute_btn = st.button("🚀 Run Comprehensive Datov QA Audit", use_container_width=True, type="primary")

    # ==================== RIGHT PANEL: DATOV RESULTS SHOWCASE ====================
    with col_results:
        st.subheader("📊 Datov Execution Readouts")
       
        if execute_btn:
            if not expected_specs.strip() or not parsed_logs_payload.strip():
                st.error("🛑 Intake System Mismatch: Both requirements criteria and log inputs are required.")
            else:
                with st.status("Analyzing system telemetry alignment...", expanded=True) as status_container:
                   
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
                   
                    user_payload = f"Project Context: {project_uid}\nScope: {', '.join(active_vectors)}\n\n[CRITERIA]:\n{expected_specs}\n\n[LOGS]:\n{parsed_logs_payload}"
                   
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
                       
                        # High-impact metric widgets
                        m_col1, m_col2 = st.columns(2)
                        with m_col1:
                            st.markdown(f'<div class="metric-card"><small style="color:#94a3b8;">COMPUTE LATENCY</small><div class="metric-val">{execution_delta}s</div></div>', unsafe_allow_html=True)
                        with m_col2:
                            st.markdown(f'<div class="metric-card"><small style="color:#94a3b8;">PARSED RUN PACKETS</small><div class="metric-val">{len(uploaded_files) if uploaded_files else 1} Source(s)</div></div>', unsafe_allow_html=True)
                           
                        st.success("🎉 Compliance evaluation concluded successfully.")
                        st.markdown("---")
                       
                        # Display the complete generated audit report directly
                        st.markdown(raw_audit_report)
                       
                        # Data Asset Exporter Module
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
            st.info("💡 System Awaiting Inbound Data Feed. Populate the requirements and upload files on the left panel, then hit the run button to stream your report layout here.")
