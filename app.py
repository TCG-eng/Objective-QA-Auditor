import time
import httpx
import io
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Datov Audit System")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Persistent global dictionary cache to store evaluation reports for document generation
LATEST_AUDIT_CACHE = {}

class AuditRequest(BaseModel):
    target: str

class DocumentRequest(BaseModel):
    target: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/audit")
async def run_intelligent_audit(payload: AuditRequest):
    global LATEST_AUDIT_CACHE
    start_time = time.time()
   
    # Extract clean base host domain input parameter
    target = payload.target.strip().replace("https://", "").replace("http://", "").split("/")[0]
    if not target:
        raise HTTPException(status_code=400, detail="Invalid target host structure.")

    findings = []
    score = 100

    try:
        # Execute live network request to harvest headers
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            response = await client.get(f"https://{target}")
            headers = response.headers
           
        # 1. HSTS Compliance Metric Check
        if "Strict-Transport-Security" not in headers:
            score -= 15
            findings.append({
                "title": "Missing Strict-Transport-Security (HSTS) Header",
                "severity": "high",
                "status": "fail",
                "description": "The server fails to force encrypted HTTPS browser sessions.",
                "solution": "Add this header rule to your server deployment runtime:\n`Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`"
            })
        else:
            findings.append({"title": "Strict-Transport-Security (HSTS)", "severity": "low", "status": "pass", "description": "Enforced HTTPS connection configurations are secure.", "solution": "No adjustment parameters required."})

        # 2. Content-Security-Policy Check
        if "Content-Security-Policy" not in headers:
            score -= 15
            findings.append({
                "title": "Missing Content-Security-Policy (CSP) Protection",
                "severity": "medium",
                "status": "fail",
                "description": "The ecosystem lacks origin protection boundaries to mitigate script injections.",
                "solution": "Add the baseline parameter ruleset layout to authorized headers:\n`Content-Security-Policy: default-src 'self';`"
            })
        else:
            findings.append({"title": "Content-Security-Policy (CSP)", "severity": "low", "status": "pass", "description": "Cross-site namespace verification vectors validated.", "solution": "No adjustment parameters required."})

        # 3. Server Signature Leak Check
        server_header = headers.get("Server")
        if server_header:
            score -= 10
            findings.append({
                "title": "Infrastructure System Signature Identity Discovered",
                "severity": "low",
                "status": "fail",
                "description": f"The node leaks explicit internal software framework data labels ({server_header}).",
                "solution": "Configure server variables or proxy rules to strip downstream application parameters:\n`Server Tokens = Off`"
            })
        else:
            findings.append({"title": "Infrastructure Signature Masking", "severity": "low", "status": "pass", "description": "Overt runtime signature identities remain protected.", "solution": "No adjustment parameters required."})
