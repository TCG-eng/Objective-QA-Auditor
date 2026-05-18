import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal
from pypdf import PdfReader
from openai import OpenAI

app = FastAPI()

class ComplianceRule(BaseModel):
    rule_id: str = Field(description="Section code")
    parameter_name: str = Field(description="Metric name")
    comparison_operator: Literal["LESS_THAN", "GREATER_THAN", "EQUALS"]
    target_value: float = Field(description="Numeric threshold")

class MasterComplianceProfile(BaseModel):
    rules: List[ComplianceRule]

class ExecutedMetric(BaseModel):
    corresponding_rule_id: str = Field(description="Matching section code")
    actual_measured_value: float = Field(description="Recorded number")

class UploadedExecutionLog(BaseModel):
    metrics: List[ExecutedMetric]

def extract_pdf_text(file_bytes) -> str:
    reader = PdfReader(from_bytes:=bytes(file_bytes))
    return "".join([page.extract_text() for page in reader.pages])

@app.post("/audit")
async def run_audit(scale_file: UploadFile = File(...), material_file: UploadFile = File(...)):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    scale_text = extract_pdf_text(await scale_file.read())
    material_text = extract_pdf_text(await material_file.read())

    scale_comp = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Extract rules:\n{scale_text}"}],
        response_format=MasterComplianceProfile,
    )
    material_comp = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Extract metrics:\n{material_text}"}],
        response_format=UploadedExecutionLog,
    )

    log_map = {m.corresponding_rule_id: m.actual_measured_value for m in material_comp.choices.message.parsed.metrics}
    matrix = []
    system_pass = True

    for rule in scale_comp.choices.message.parsed.rules:
        if rule.rule_id not in log_map:
            system_pass = False
            matrix.append({"rule_id": rule.rule_id, "verdict": "FAIL", "reason": "Missing"})
            continue

        actual = log_map[rule.rule_id]
        passed = False
        if rule.comparison_operator == "EQUALS" and actual == rule.target_value: passed = True
        elif rule.comparison_operator == "LESS_THAN" and actual <= rule.target_value: passed = True
        elif rule.comparison_operator == "GREATER_THAN" and actual >= rule.target_value: passed = True

        if not passed: system_pass = False
        matrix.append({"rule_id": rule.rule_id, "parameter": rule.parameter_name, "verdict": "PASS" if passed else "FAIL", "expected": rule.target_value, "actual": actual})

    return {"status": "COMPLIANT" if system_pass else "NON_COMPLIANT", "matrix": matrix}
