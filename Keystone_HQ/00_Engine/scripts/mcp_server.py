import subprocess
import os
import sys
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Keystone Self-Healing MCP Engine")

class CommandPayload(BaseModel):
    command: str
    context_id: str

def execute_in_sandbox(cmd: str) -> dict:
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"status": "failed", "stderr": "Execution timed out.", "returncode": -1}

def diagnose_and_heal(failed_cmd: str, stderr: str) -> str:
    """
    Sends the error directly to the Gemini 3.5 Flash API to generate a working patch script.
    """
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-3.5-flash")
    
    prompt = f"""
    The following terminal command failed inside our Antigravity Docker environment:
    Command: {failed_cmd}
    Error output: {stderr}
    
    Write a lightweight, functional Python patch script or terminal command to resolve this.
    Provide ONLY the code/command inside a markdown block. No conversational text.
    """
    response = model.generate_content(prompt)
    return response.text.strip().replace("```python", "").replace("```", "")

@app.post("/execute")
async def execute_command(payload: CommandPayload):
    # Step 1: Run the command in the sandbox
    exec_res = execute_in_sandbox(payload.command)
    
    if exec_res["status"] == "success":
        return {"output": exec_res["stdout"], "healed": False}
    
    # Step 2: If failed, execute the self-healing loop
    print(f"Command failed. Initiating self-healing loop for context: {payload.context_id}")
    patch_code = diagnose_and_heal(payload.command, exec_res["stderr"])
    
    # Write the patch to a temporary file
    patch_path = f"/tmp/patch_{payload.context_id}.py"
    with open(patch_path, "w") as f:
        f.write(patch_code)
        
    # Execute the healing patch
    patch_res = execute_in_sandbox(f"python {patch_path}") # changed to python for windows compat in test
    
    if patch_res["status"] == "success":
        # Register the healed solution as a permanent skill
        skill_payload = {
            "skill_name": f"healed_{payload.context_id}",
            "original_command": payload.command,
            "solution_script": patch_code
        }
        skill_dir = "C:/Users/Curtis/.gemini/config/skills/healed_skills/" # updated for windows config
        os.makedirs(skill_dir, exist_ok=True)
        with open(os.path.join(skill_dir, f"healed_{payload.context_id}.json"), "w") as sf:
            json.dump(skill_payload, sf, indent=4)
            
        return {
            "output": "Self-healing successful. Skill registered.",
            "healed": True,
            "patch_used": patch_code
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Self-healing failed. Original error: {exec_res['stderr']}. Patch error: {patch_res['stderr']}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8642)
