import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import json
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
    v4 = st.checkbox("API Response Structural Drift", value=False)
   
    active_vectors = []
    if v1: active_vectors.append("Performance Latency")
    if v2: active_vectors.append("Security & PII Mapping")
    if v3: active_vectors.append("Logical Gaps")
    if v4: active_vectors.append("Structural Drift")

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
                placeholder="Example:\nREQ-1: Auth tokens must be salted and encrypted using AES-256.\nREQ-2: Gateway latency metrics must remain under 200ms during query cycles.",
                height=300,
                key="specs_input"
            )
       
        with tab_upload:
            st.markdown("##### Advanced Upload capabilities")
            # EXTENSIVE CAPABILITY: Multi-File drag-and-drop system log input arrays
            uploaded_files = st.file_uploader(
                "Batch drag-and-drop log files here (.txt, .log, .json, .csv)",
                type=["txt", "log", "json", "csv"],
                accept_multiple_files=True
            )
           
            # Text area fallback parameter interface
            manual_logs = st.text_area(
                "Or manually input raw terminal log entries here:",
                placeholder="[DEBUG] 23:14:02 - Incoming route pattern payload mismatch on processing array...",
                height=150,
                key="logs_input"
            )
           
            # Extensive Multi-Source Log Parsing Matrix Pipeline
            parsed_logs_payload = ""
            if uploaded_files:
                st.markdown("###### 📦 Active File Inventory Manifest")
                for f in uploaded_files:
                    file_contents = f.read().decode("utf-8")
                    parsed_logs_payload += f"\n--- FILE MANIFEST SOURCE: {f.name} ---\n{file_contents}\n"
                   
                    # Renders a sleek visualization layout box for every individual file uploaded
                    st.markdown(f"""
                        <div class="file-card">
                            <strong>📄 {f.name}</strong><br>
                            <small style="color:#94a3b8;">Size: {round(f.size/1024, 2)} KB | Text Extraction Complete</small>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                parsed_logs_payload = manual_logs

        st.divider()
        execute_btn = st.button("🚀 Run Comprehensive Datov QA Audit", use_container_width=True, type="primary")

    # ==================== RIGHT PANEL: DATOV RESULTS SHOWCASE READOUTS ====================
    with col_results:
        st.subheader("📊 Datov Execution Readouts")
       
        if execute_btn:
            if not expected_specs.strip() or not parsed_logs_payload.strip():
                st.error("🛑 Intake System Mismatch: Both expected acceptance criteria models and evaluation run data feeds are required.")
            else:
                # Execution Progress Telemetry
                with st.status("Analyzing structured systems telemetry alignment...", expanded=True) as status_container:
                   
                    time.sleep(0.3)
                    status_container.update(label="Scanning payloads against target focus parameters...", state="running")
                   
                    system_instructions = (
                        "You are an elite automated system QA auditor working inside the Datov Ecosystem. Your objective is to explicitly map out structural regressions, "
                        "provide production-grade fixes, and build engineering documentation out of discrepancies.\n\n"
                        "You MUST evaluate the user data and respond using a highly polished, standardized architectural template. "
                        "Break your response explicitly down into these exact Markdown headers:\n\n"
                        "### 1. Requirements Discrepancy Matrix\n"
                        "(Provide an extensive Markdown table evaluating EVERY requirement: Requirement ID | Expected Behavior | Actual Observed Outcome | Compliance Status [PASSED / FAILED / UNVERIFIED])\n\n"
                        "### 2. Deep Root Cause Analysis\n"
                        "(Provide a strict architectural reason specifying WHY discrepancies occurred based on telemetry patterns)\n\n"
                        "### 3. Production Engineering Solutions\n"
                        "(Provide copy-pasteable, optimized python/bash/config script blocks or strategies to remediate every failure flagged)\n\n"
                        "### 4. Automated Datov QA Documentation\n"
                        "(A formal technical software engineering documentation brief tracking Project Name, Audit Datetime, System Status Summary, and Long-Term Preventative recommendations.)"
                    )
                   
                    user_payload = f"Project Context: {project_uid}\nActive Extraction Focus Scope: {', '.join(active_vectors)}\n\n[OBJECTIVE CONFIG CRITERIA]:\n{expected_specs}\n\n[TELEMETRY PIPELINE STREAM]:\n{parsed_logs_payload}"
                   
                    try:
                        status_container.update(label="Engaging Gemini generative reasoning arrays...", state="running")
                        start_time = time.time()
                       
                        # Generate the analytical structure
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
                       
                        status_container.update(label="Analytical Pipeline Completed. Generating Interactive Dashboard...", state="complete")
                       
                        # EXTENSIVE READOUT: High-impact visualization grid
                        st.markdown("#### ⚙️ Real-Time Telemetry Performance Metrics")
                        m_col1, m_col2, m_col3 = st.columns(3)
                        with m_col1:
                            st.markdown(f"""
                                <div class="metric-card">
                                    <small style="color:#94a3b8;">COMPUTE LATENCY</small><br>
                                    <div class="metric-val">{execution_delta}s</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with m_col2:
                            st.markdown(f"""
                                <div class="metric-card">
                                    <small style="color:#94a3b8;">PARSED RUN PACKETS</small><br>
                                    <div class="metric-val">{len(uploaded_files) if uploaded_files else 1} Sources</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with m_col3:
                            st.markdown(f"""
                                <div class="metric-card">
                                    <small style="color:#94a3b8;">SYSTEM COMPLIANCE</small><br>
                                    <div class="metric-val" style="color:#a78bfa;">Analyzed</div>
                                </div>
                            """, unsafe_allow_html=True)
                           
                        st.success("🎉 Compliance Matrix calculation phase concluded successfully.")
                        st.markdown("---")
                       
                        # EXTENSIVE READOUT: Segmented interface presentation system separating the results data
                        res_tab1, res_tab2, res_tab3 = st.tabs(["📊 Evaluation Analysis & Discrepancies", "🛠️ Actionable Code Solutions", "📜 System Documentation Brief"])
                       
                        # Extract chunks based on headers to split into separate clean tabs automatically
                        with res_tab1:
                            st.markdown("### 📋 Verification Analysis Breakdown")
                            st.markdown(raw_audit_report.split("### 3. Production Engineering Solutions")[0])
                       
                        with res_tab2:
                            st.markdown("### 💻 Engineered Deployment Remediations")
                            if "### 3. Production Engineering Solutions" in raw_audit_report:
                                codes_section = raw_audit_report.split("### 3. Production Engineering Solutions")[1].split("### 4. Automated Datov QA Documentation")[0]
                                st.markdown(codes_section)
                            else:
                                st.info("No explicit system regressions requiring software code patches were surfaced during this pipeline execution.")
                       
                        with res_tab3:
                            st.markdown("### 🗃️ Production Artifact Documentation Brief")
                            if "### 4. Automated Datov QA Documentation" in raw_audit_report:
                                doc_section = raw_audit_report.split("### 4. Automated Datov QA Documentation")[1]
                                st.markdown(doc_section)
                            else:
                                st.markdown(raw_audit_report)
                       
                        # Data Asset Exporter Matrix
                        st.divider()
                        st.subheader("💾 Export Datov System Artifact Manifests")
                       
                        st.download_button(
                            label="📥 Download Enterprise Markdown Audit Report Manifest (.md)",
                            data=raw_audit_report,
                            file_name=f"DATOV_ENTERPRISE_QA_REPORT_{project_uid}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                       
                    except Exception as e:
                        status_container.update(label="Critical System Interrupt", state="error")
                        st.error(f"Ecosystem Evaluation Pipeline Interrupted: {str(e)}")
        else:
            st.info("💡 System Awaiting Direct Intake Feed: Feed standard requirement properties or batch drop active software log assets into the ingestion console panel on the left to trigger the automated Datov analytics dashboard readout arrays.")
