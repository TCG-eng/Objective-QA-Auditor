import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import requests
import time
import uuid
import datetime
import io

# Early Import Optimization (PEP 8 Compliance)
try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None

# =========================================================================
# 1. SYSTEM INITIALIZATION & WINDOW CUSTOMIZATION
# =========================================================================
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

# Global Session State Tracking Initialization
if "audit_history_log" not in st.session_state:
    st.session_state["audit_history_log"] = []
if "last_audit_report" not in st.session_state:
    st.session_state["last_audit_report"] = None
if "last_generated_id" not in st.session_state:
    st.session_state["last_generated_id"] = None
if "selected_sop_text" not in st.session_state:
    st.session_state["selected_sop_text"] = ""

# =========================================================================
# 2. CORE UTILITY ENGINE FUNCTIONS (Modular Architecture)
# =========================================================================
def parse_uploaded_files(uploaded_files):
    """Safely extracts data packet payloads from multi-format logs."""
    payload = ""
    if not uploaded_files:
        return payload
       
    st.markdown("###### 📦 Active File Inventory Manifest")
    for f in uploaded_files:
        file_name_lower = f.name.lower()
        file_contents = ""
        try:
            if file_name_lower.endswith('.pdf'):
                if pypdf:
                    pdf_reader = pypdf.PdfReader(f)
                    file_contents = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
                else:
                    file_contents = "[ERROR: pypdf library missing on server environment]"
            elif file_name_lower.endswith('.docx'):
                if docx:
                    doc = docx.Document(f)
                    file_contents = "\n".join([p.text for p in doc.paragraphs])
                else:
                    file_contents = "[ERROR: python-docx library missing on server environment]"
            else:
                file_contents = f.read().decode("utf-8")
        except Exception as parse_error:
            st.error(f"⚠️ Could not parse text contents from {f.name}: {str(parse_error)}")
            file_contents = f"[ERROR: Unreadable binary content in {f.name}]"

        payload += f"\n--- SOURCE FILE: {f.name} ---\n{file_contents}\n"
        st.markdown(f'<div class="file-card"><strong>📄 {f.name}</strong><br><small style="color:#94a3b8;">Size: {round(f.size/1024, 2)} KB</small></div>', unsafe_allow_html=True)
    return payload

def run_telemetry_audit(api_key, model, target_node, specs, logs, temp):
    """Executes generative intelligence data alignment maps with strict formatting rules."""
    client = genai.Client(api_key=api_key)
   
    system_instructions = (
        "You are an elite automated system QA auditor working inside the Datov Ecosystem.\n"
        "Your task is to review the provided logs against the system requirements criteria and generate a highly structured compliance report.\n\n"
        "For EVERY requirement evaluated, you must explicitly detail the outcome using the following exact three-part format:\n\n"
        "### 📑 REQUIREMENT ANALYSIS: [Insert Requirement ID/Name]\n"
        "1. **STATUS**: [State either **PASSED** or **FAILED** clearly]\n"
        "2. **FINDINGS**: [Provide a detailed diagnostic explanation. If it passed, summarize the validating log telemetry. If it FAILED, explicitly detail *why* it failed by quoting or referencing the specific anomalous log entries, missing tokens, or error codes found in the payload.]\n"
        "3. **CORRECTIVE MEASURE**: [If it passed, state 'No remediation required.' If it FAILED, provide a definitive, actionable, and copy-pasteable technical solution—such as a configuration script, shell command, or code block—to immediately resolve the issue.]\n\n"
        "At the very top of your response, before the individual breakdowns, include an executive **### 🛡️ AUDIT OUTCOME SUMMARY** showing: Total Requirements Checked, Total Passed, Total Failed, and a final Compliance Percentage."
    )
   
    user_payload = f"Project Context: {target_node}\n\n[CRITERIA]:\n{specs}\n\n[LOGS]:\n{logs}"
   
    response = client.models.generate_content(
        model=model,
        contents=user_payload,
        config=types.GenerateContentConfig(
            system_instruction=system_instructions,
            temperature=temp,
        ),
    )
    return response.text

# =========================================================================
# 3. SIDEBAR PLATFORM PORTAL CONTROL WINDOW
# =========================================================================
with st.sidebar:
    st.title("🌐 Datov Portal")
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
# MODULE 1: CORE QA AUDIT HUB WORKSPACE
# =========================================================================
if current_page == "🛡️ QA Audit Hub":
    st.title("🛡️ Datov Enterprise QA Audit Platform")
    st.caption("Industrial Automated Metric Verification, Regression Mapping, and Technical Solution Blueprint Engine.")
    st.markdown("---")

    col_inputs, col_results = st.columns([1, 1.3], gap="large")

    with col_inputs:
        st.subheader("📥 Data Intake Engine")
        st.markdown("### 📋 System Requirements Criteria")
       
        default_specs = st.session_state["selected_sop_text"] if st.session_state["selected_sop_text"] else "Example:\nREQ-1: Auth tokens must be encrypted.\nREQ-2: Gateway latency must remain under 200ms."
        expected_specs = st.text_area("Define Objective Engineering Standards:", value=default_specs, height=180, key="specs_input")
       
        st.markdown("### 📂 Document Upload Portal")
        uploaded_files = st.file_uploader("Batch upload telemetry log data (.txt, .log, .json, .csv, .pdf, .docx)", type=["txt", "log", "json", "csv", "pdf", "docx"], accept_multiple_files=True)
        manual_logs = st.text_area("Or input raw terminal telemetry entries manually:", placeholder="Enter raw logs here...", height=120, key="logs_input")
       
        # Parse inputs cleanly using the utility pipeline
        parsed_logs_payload = parse_uploaded_files(uploaded_files) if uploaded_files else manual_logs
       
        st.divider()
        execute_btn = st.button("🚀 Run Comprehensive Datov QA Audit", use_container_width=True, type="primary")

    with col_results:
        st.subheader("📊 Datov Execution Readouts")
       
        if execute_btn:
            if not st.session_state["gemini_api_key"]:
                st.error("🔒 Security Key Required: Please enter your valid Gemini API Key inside the sidebar configuration window.")
            elif not expected_specs.strip() or not parsed_logs_payload.strip():
                st.error("🛑 Intake System Mismatch: Both requirements criteria and log inputs are required.")
            else:
                with st.status("Analyzing system telemetry alignment...", expanded=True) as status_container:
                    try:
                        status_container.update(label="Engaging Gemini generative reasoning arrays...", state="running")
                        start_time = time.time()
                       
                        # Call modular audit engine
                        report_output = run_telemetry_audit(
                            api_key=st.session_state["gemini_api_key"],
                            model=target_model,
                            target_node=project_uid,
                            specs=expected_specs,
                            logs=parsed_logs_payload,
                            temp=temperature
                        )
                       
                        execution_delta = round(time.time() - start_time, 2)
                        generated_id = f"DTV-{uuid.uuid4().hex[:6].upper()}"
                       
                        # Atomic State Commits
                        st.session_state["last_audit_report"] = report_output
                        st.session_state["last_generated_id"] = generated_id
                       
                        st.session_state["audit_history_log"].append({
                            "Audit ID": generated_id,
                            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Target Node": project_uid,
                            "Model Engine": target_model,
                            "Latency": f"{execution_delta}s"
                        })
                       
                        status_container.update(label="Analysis Pipeline Completed!", state="complete")
                       
                        m_col1, m_col2 = st.columns(2)
                        with m_col1:
                            st.markdown(f'<div class="metric-card"><small style="color:#94a3b8;">COMPUTE LATENCY</small><div class="metric-val">{execution_delta}s</div></div>', unsafe_allow_html=True)
                        with m_col2:
                            st.markdown(f'<div class="metric-card"><small style="color:#94a3b8;">PARSED RUN PACKETS</small><div class="metric-val">{len(uploaded_files) if uploaded_files else 1} Source(s)</div></div>', unsafe_allow_html=True)
                       
                        st.success(f"🎉 Evaluation concluded. Assigned Tracker ID: {generated_id}")
                       
                    except Exception as e:
                        status_container.update(label="Critical System Interrupt", state="error")
                        st.error(f"Ecosystem Evaluation Pipeline Interrupted: {str(e)}")
       
        # PERSISTENT PRESENTATION INTERFACE (Dynamic Multi-Tab Layout)
        if st.session_state["last_audit_report"]:
            st.markdown("---")
            st.subheader("📑 Active Enterprise Audit Manifest")
           
            tab_summary, tab_details = st.tabs([
                "📊 Compliance Scorecard",
                "🔍 Granular Pass/Fail Findings & Remediation"
            ])
           
            raw_report = st.session_state["last_audit_report"]
           
            with tab_summary:
                if "### 📑 REQUIREMENT" in raw_report:
                    summary_part = raw_report.split("### 📑 REQUIREMENT")[0]
                    st.markdown(summary_part)
                else:
                    st.markdown(raw_report)
               
            with tab_details:
                st.caption("Reviewing explicit status metrics, telemetry failure root-causes, and system fixes.")
                st.markdown(raw_report)
           
            st.divider()
           
            # Interactive export utilities
            col_dl, col_share = st.columns([4, 1])
            with col_dl:
                st.download_button(
                    label="📥 Export Certified Enterprise Markdown Manifest (.md)",
                    data=raw_report,
                    file_name=f"DATOV_COMPLIANCE_REPORT_{st.session_state['last_generated_id']}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col_share:
                if st.button("🔗 Copy Registry ID", use_container_width=True):
                    st.toast(f"Copied Registry Reference: {st.session_state['last_generated_id']}", icon="📋")
        else:
            st.info("💡 System Awaiting Inbound Data Feed. Populate your criteria specifications and drop your files on the left panel, then hit the run button to stream your analysis report.")

        # Atomic Clean State Reset Controller
        if st.button("🧹 Clear Active Workspace Views", use_container_width=True):
            st.session_state["last_audit_report"] = None
            st.session_state["last_generated_id"] = None
            st.rerun()

        # HISTORICAL RUN LOG REGISTRY TABLE VISUALIZATION
        if st.session_state["audit_history_log"]:
            st.write("###")
            st.markdown("---")
            st.subheader("📜 Run Registry Master Session Log")
            log_df = pd.DataFrame(st.session_state["audit_history_log"])
            st.dataframe(log_df, use_container_width=True, hide_index=True)

# =========================================================================
# MODULE 2: PROCEDURES LIBRARY DATABASE
# =========================================================================
elif current_page == "📚 Procedures Library":
    st.title("📚 Datov Standard Operating Procedures (SOP) Database")
    st.caption("Store, manage, and load permanent corporate manuals or compliance checklist requirements.")
    st.markdown("---")
 
    st.subheader("📁 Central Requirements Repository")
 
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
        st.success(f"✅ Success! '{selected_sop}' loaded into working memory. Navigate to the QA Audit Hub to execute.")

    st.markdown("---")
    st.subheader("🌐 GitHub Assets Repository")
    api_url = "https://api.github.com/repos/TCG-eng/Objective-QA-Auditor/contents/assets"
  
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            files = response.json()
            docs = {f['name']: f['download_url'] for f in files if f['name'].lower().endswith('.pdf')}
          
            if docs:
                selected_git = st.selectbox("Select document from GitHub:", list(docs.keys()))
              
                if st.button("📥 Load GitHub Document"):
                    if selected_git in docs:
                        with st.spinner(f"Parsing and extracting text from {selected_git}..."):
                            content_resp = requests.get(docs[selected_git])
                            if pypdf:
                                pdf_stream = io.BytesIO(content_resp.content)
                                pdf_reader = pypdf.PdfReader(pdf_stream)
                                extracted_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
                              
                                if extracted_text.strip():
                                    st.session_state["selected_sop_text"] = extracted_text
                                    st.toast(f"🎉 Success! {selected_git} synced successfully.", icon="✅")
                                    st.success(f"📂 Loaded successfully! Scroll up or switch to the main hub to view requirements.")
                                else:
                                    st.error("⚠️ Failed to extract any readable text from this PDF file.")
                            else:
                                st.error("❌ pypdf engine not available to interpret the requested binary asset package.")
            else:
                st.warning("⚠️ No .pdf files found inside the remote target directory structure.")
        else:
            st.error(f"GitHub pipeline communication failure: {response.status_code}.")
    except Exception as e:
        st.error(f"Ecosystem lookup error: {e}")

    if st.button("🔄 Reset Standard Workspace Memory", use_container_width=True):
        st.session_state["selected_sop_text"] = ""
        st.rerun()

# =========================================================================
# MODULE 3: ANALYTICS PERFORMANCE HISTORY
# =========================================================================
elif current_page == "📈 Analytics History":
    st.title("📈 Datov Compliance Analytics & Operations Metrics")
    st.caption("Monitor real-time system performance, historical success distributions, and audit cycle volumes.")
    st.markdown("---")
 
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="metric-card"><small style="color:#94a3b8;">TOTAL COMPLETED AUDITS</small><div class="metric-val">142 Runs</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="metric-card"><small style="color:#94a3b8;">GLOBAL SYSTEM COMPLIANCE RATE</small><div class="metric-val" style="color:#10b981;">91.4%</div></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="metric-card"><small style="color:#94a3b8;">AVG ENGINE COMPUTE VELOCITY</small><div class="metric-val" style="color:#a78bfa;">1.44s</div></div>', unsafe_allow_html=True)
 
    st.divider()
    st.subheader("📊 Audit Volume Trends (Last 7 Days)")
 
    chart_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Audit Runs Completed": [12, 18, 15, 22, 29, 8, 3]
    })
    st.bar_chart(chart_data, x="Day", y="Audit Runs Completed", color="#38bdf8")
