mport streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import time

# 1. Page & Layout Configuration
st.set_page_config(
    page_title="QA Audit Engine (Gemini)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ Enterprise QA Audit System & Documentation Engine")
st.caption("Discrete automated metric matching, algorithmic structural reconciliation, and standardized artifact documentation powered by Gemini.")
st.markdown("---")

# 2. Sidebar Panel for Configuration & API Keys
with st.sidebar:
    st.header("⚙️ Core Engine Settings")
   
    # Session state initialization for the Gemini API Key
    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = ""
       
    api_input = st.text_input("🔑 Gemini API Key", type="password", value=st.session_state["gemini_api_key"])
    if api_input:
        st.session_state["gemini_api_key"] = api_input

    st.divider()
    st.subheader("📋 Audit Profiles")
    project_uid = st.text_input("Project / System ID", value="TCG_AUDIT_MODULE")
    target_model = st.selectbox("Gemini Model Vector", ["gemini-2.5-flash", "gemini-2.5-pro"])
    temperature = st.slider("Analysis Precision", min_value=0.0, max_value=1.0, value=0.1, step=0.05)
   
    st.divider()
    st.info("💡 Pro-Tip: Provide clean execution outputs or stack traces for maximum validation accuracy.")

# 3. Security Access Gate
if not st.session_state["gemini_api_key"]:
    st.warning("🔒 System Pending Access Validation: Please enter a valid Gemini API Key in the configuration sidebar to initialize.")
else:
    # Initialize the modern Google Gen AI Client natively
    client = genai.Client(api_key=st.session_state["gemini_api_key"])

    # 4. Main Two-Column User Interface Workspace
    col_inputs, col_telemetry = st.columns([1, 1.2], gap="large")

    with col_inputs:
        st.subheader("📥 Data Feed Pipeline")
       
        tab_spec, tab_runtime = st.tabs(["📄 Target System Requirements", "💻 Execution Logs / Manifests"])
       
        with tab_spec:
            expected_specs = st.text_area(
                "Define Objective Target Standards / Acceptance Criteria:",
                placeholder="Example:\nREQ-101: System must handle JWT encryption vectors.\nREQ-102: API response latency thresholds must not exceed 250ms.",
                height=250,
                key="specs_input"
            )
       
        with tab_runtime:
            execution_logs = st.text_area(
                "Provide System Execution Output / Live Telemetry Logs:",
                placeholder="Example:\n[INFO] Inbound request matching routing path /auth/token.\n[CRITICAL] PII violation detected: raw value leaked.",
                height=250,
                key="logs_input"
            )
           
        st.subheader("🛠️ Custom Verification Focus")
        focus_areas = st.multiselect(
            "Filter Extraction Vectors",
            ["Performance Anomalies", "Security Violations", "Logical Core Gaps", "Data Structural Drift"],
            default=["Performance Anomalies", "Security Violations"]
        )

        st.divider()
        execute_btn = st.button("🚀 Execute Audit & Generate Manifests", use_container_width=True, type="primary")

    with col_telemetry:
        st.subheader("📊 QA Compliance Assessment Hub")
       
        if execute_btn:
            if not expected_specs.strip() or not execution_logs.strip():
                st.error("🛑 Input Validation Failure: Both requirements schemas and runtime logs must be provided.")
            else:
                # 5. Pipeline State Tracking block
                with st.status("Initializing verification workers...", expanded=True) as status_container:
                   
                    status_container.update(label="Analyzing structural alignment anomalies...", state="running")
                   
                    # 6. Engineered System Instructions
                    system_instructions = (
                        "You are an elite automated system QA auditor. Your objective is to explicitly map out structural regressions, "
                        "provide production-grade fixes, and build engineering documentation out of discrepancies.\n\n"
                        "You MUST evaluate the user data and respond using a highly polished, standardized architectural template. "
                        "Break your response explicitly down into these exact Markdown headers:\n\n"
                        "### 1. Requirements Discrepancy Matrix\n"
                        "(Provide an extensive Markdown table evaluating EVERY requirement: Requirement ID | Expected Behavior | Actual Observed Outcome | Compliance Status [PASSED / FAILED / UNVERIFIED])\n\n"
                        "### 2. Deep Root Cause Analysis\n"
                        "(Provide a strict architectural reason specifying WHY discrepancies occurred based on telemetry patterns)\n\n"
                        "### 3. Production Engineering Solutions\n"
                        "(Provide copy-pasteable, optimized python/bash/config script blocks or strategies to remediate every failure flagged)\n\n"
                        "### 4. Automated QA System Documentation\n"
                        "(A formal technical software engineering documentation brief tracking Project Name, Audit Datetime, System Status Summary, and Long-Term Preventative recommendations.)"
                    )
                   
                    user_payload = f"Project Context: {project_uid}\nFocus Vectors: {', '.join(focus_areas)}\n\n[OBJECTIVE REQUIREMENTS]:\n{expected_specs}\n\n[RUNTIME EXECUTION TELEMETRY]:\n{execution_logs}"
                   
                    # 7. Safe Execution Block with complete exception handling closure
                    try:
                        status_container.update(label="Streaming Gemini evaluation results...", state="running")
                        start_time = time.time()
                       
                        # Modern SDK format for Google GenAI content generation
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
                       
                        status_container.update(label="QA Audit Complete. Rendered Engine Reports Below.", state="complete")
                       
                        # Render Telemetry Metrics
                        m1, m2 = st.columns(2)
                        with m1:
                            st.metric(label="Engine Latency Processing", value=f"{execution_delta}s")
                        with m2:
                            st.metric(label="Target Pipeline Strategy", value=target_model)
                       
                        st.markdown("---")
                       
                        # Output Markdown Report
                        st.markdown(raw_audit_report)
                       
                        # 8. Document Exporter Framework
                        st.divider()
                        st.subheader("💾 Export QA Technical Documentation Assets")
                       
                        st.download_button(
                            label="📥 Export Audit Specification Document (.md)",
                            data=raw_audit_report,
                            file_name=f"QA_COMPLIANCE_REPORT_{project_uid}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                       
                    except Exception as e:
                        status_container.update(label="Critical Engine Fail", state="error")
                        st.error(f"Gateway Communication Error: {str(e)}")
        else:
            st.info("💤 System Monitoring Engine Standby: Configure validation parameters and trigger the pipeline on the left workspace panel to run automated verification algorithms.")
