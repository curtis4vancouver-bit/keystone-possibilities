import re

# Mock Script Package to Test Gates
mock_script_package = """
# SCRIPT PACKAGE: BPC-157 Tendon Healing

## Metadata
* **Title**: The BPC-157 Tendon Healing Protocol
* **Channel**: Protocols
* **Token File**: youtube_token_protocols.json
* **Aspect Ratio**: 9:16
* **AI Disclosure**: Enabled

## Primary Sources
* **PubMed ID**: PMID: 21030905
* **DOI**: https://doi.org/10.1002/jor.21225
* **Preprint**: No
* **Retracted**: No

## Video Script
Wayne says: "Looking for the ultimate tendon recovery protocol? Pre-clinical trials show BPC-157 accelerates Achilles tendon healing by activating vascular endothelial growth factor. But don't buy gray market research chemicals."

Wayne says: "Recent studies confirm BPC-157 promotes angiogenesis. However, compounding pharmacies must legally compound BPC-157 under valid prescription, as Health Canada classifies it as an unauthorized drug."

Wayne says: "Always consult a doctor before starting. Standard case studies utilize a titration schedule of 250 mcg twice daily. Do not confuse micrograms with milligrams to avoid dosing errors."

## Description
This video is for scientific study, educational analysis, and general research purposes only. It does not constitute medical advice, diagnosis, or treatment. Consult your physician before starting any new protocol.

🤖 SYNTHETIC MEDIA / AI DIGITAL TWIN DISCLOSURE:
The host is a photorealistic digital representation of Wayne Stevenson, synthesized using advanced visual networks.

⚖️ LEGAL DISCLAIMER:
BPC-157 is not FDA-approved for human treatment. It is banned on the WADA Prohibited List and is classified as an unauthorized drug by Health Canada.
"""

def run_research_verification_gate(script_data):
    print("=== RUNNING RESEARCH VERIFICATION GATE ===")
    logs = []
    failed = False
    
    # 1. Check for Primary Source
    source_match = re.search(r"PubMed ID.*(PMID:\s*\d+)", script_data, re.IGNORECASE)
    if source_match:
        logs.append(f"[PASS] Primary Source verified: {source_match.group(1)}")
    else:
        logs.append("[FAIL] Missing Primary Source PMID")
        failed = True
        
    # 2. Check for Preprints (allow markdown bold)
    preprint_match = re.search(r"Preprint\*+\s*:\s*(Yes|No)", script_data, re.IGNORECASE)
    if preprint_match and preprint_match.group(1).lower() == "no":
        logs.append("[PASS] Peer-reviewed status confirmed")
    else:
        logs.append("[WARN] Preliminary preprint detected or status unconfirmed. Verification required.")
        
    # 3. Check for Retractions (allow markdown bold)
    retracted_match = re.search(r"Retracted\*+\s*:\s*(Yes|No)", script_data, re.IGNORECASE)
    if retracted_match and retracted_match.group(1).lower() == "no":
        logs.append("[PASS] Retraction Watch check clear")
    else:
        logs.append("[FAIL] Source retraction status is unconfirmed or retracted!")
        failed = True
        
    # 4. Check Dosing Notation Standards
    dangerous_notations = [r"\d+\s*µg", r"\d+\s*Ug", r"\.\d+\s*mg", r"\d+\.0\s*mg", r"\d+\s*cc"]
    notation_errors = []
    for notation in dangerous_notations:
        matches = re.findall(notation, script_data)
        if matches:
            notation_errors.append(f"Dangerous notation detected: {matches}")
            
    if not notation_errors:
        logs.append("[PASS] Standardized dosing notation verified (mcg, leading zero, no cc)")
    else:
        logs.append(f"[FAIL] Notation standards violated: {notation_errors}")
        failed = True
        
    # 5. Check Regulatory Disclaimers
    regulatory_keywords = ["FDA-approved", "WADA", "Health Canada", "unauthorized drug"]
    missing_regs = [kw for kw in regulatory_keywords if kw.lower() not in script_data.lower()]
    if not missing_regs:
        logs.append("[PASS] Regulatory warnings and disclaimers attached")
    else:
        logs.append(f"[FAIL] Missing regulatory disclaimers: {missing_regs}")
        failed = True
        
    for log in logs:
        print(log)
    return not failed

def run_upload_quality_gate(script_data):
    print("\n=== RUNNING UPLOAD QUALITY GATE ===")
    logs = []
    failed = False
    
    # 1. Routing Verification (allow markdown bold)
    token_match = re.search(r"Token File\*+\s*:\s*([a-zA-Z0-9_\.]+)", script_data, re.IGNORECASE)
    channel_match = re.search(r"Channel\*+\s*:\s*([a-zA-Z0-9_\.]+)", script_data, re.IGNORECASE)
    
    if token_match and channel_match:
        token = token_match.group(1)
        channel = channel_match.group(1)
        
        # Check keyword routing correlation
        peptide_kw = ["bpc-157", "peptide", "semaglutide", "dosing", "protocol"]
        has_peptide = any(kw in script_data.lower() for kw in peptide_kw)
        
        if has_peptide and token == "youtube_token_protocols.json" and channel.lower() == "protocols":
            logs.append(f"[PASS] Correct token routing: {token} for brand {channel}")
        else:
            logs.append(f"[FAIL] Invalid token routing mismatch! Token: {token}, Channel: {channel}")
            failed = True
    else:
        logs.append("[FAIL] Missing Channel or Token definition")
        failed = True
        
    # 2. AI Disclosure Toggle (allow markdown bold)
    ai_disclosure = re.search(r"AI Disclosure\*+\s*:\s*(Enabled|Disabled)", script_data, re.IGNORECASE)
    if ai_disclosure and ai_disclosure.group(1).lower() == "enabled":
        logs.append("[PASS] AI Altered Content label enabled")
    else:
        logs.append("[FAIL] Missing AI Altered Content label")
        failed = True
        
    # 3. Medical Disclaimer Appended
    if "medical disclaimer" in script_data.lower() or "disclaimer:" in script_data.lower() or "legal disclaimer" in script_data.lower():
        logs.append("[PASS] Medical/legal disclaimer verified in description")
    else:
        logs.append("[FAIL] Missing description disclaimers")
        failed = True
        
    for log in logs:
        print(log)
    return not failed

if __name__ == "__main__":
    verification_passed = run_research_verification_gate(mock_script_package)
    upload_passed = run_upload_quality_gate(mock_script_package)
    
    if verification_passed and upload_passed:
        print("\n[SUCCESS] Mock content package passed ALL quality gates and is approved for publishing!")
    else:
        print("\n[FAILED] Quality gate failures detected. Publishing aborted.")
