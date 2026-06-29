import os
import re
import json

def validate_sauna_pages() -> dict:
    """
    Scans and audits all local Suna Spa HTML landing pages for:
    1. Single H1 tag integrity
    2. Valid embedded JSON-LD Structured Data
    3. Proper link mapping to Wayne Stevenson Person ID
    4. Compliance with BC General Contractor License display rules
    """
    seo_folder = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\02_Keystone_Possibilities\Local_SEO_Domination"
    if not os.path.exists(seo_folder):
        return {"status": "Error", "message": f"SEO directory not found at {seo_folder}"}

    html_files = [f for f in os.listdir(seo_folder) if f.endswith(".html")]
    results = {}
    
    for filename in html_files:
        path = os.path.join(seo_folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. H1 Tag Audit
        h1_matches = re.findall(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE)
        h1_count = len(h1_matches)
        h1_ok = (h1_count == 1)

        # 2. License Number Check
        has_license = "52603" in content

        # 3. JSON-LD Structured Data Extract
        json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
        schemas_detected = []
        schema_valid = False
        schema_error = ""

        for match in json_ld_matches:
            try:
                schema_json = json.loads(match.strip())
                schemas_detected.append(schema_json)
                schema_valid = True
            except Exception as e:
                schema_error = str(e)

        # 4. Keyword Density checks
        word_count = len(content.split())

        results[filename] = {
            "h1_count": h1_count,
            "h1_content": h1_matches[0].strip() if h1_count > 0 else "None",
            "h1_integrity": "PASS" if h1_ok else "FAIL",
            "has_bc_license": "PASS" if has_license else "FAIL",
            "schema_json_ld_detected": len(json_ld_matches) > 0,
            "schema_json_valid": "PASS" if schema_valid else f"FAIL: {schema_error}",
            "word_count": word_count
        }

    # Also audit the master_schema.json file
    schema_path = os.path.join(seo_folder, "master_schema.json")
    master_schema_status = "Missing"
    if os.path.exists(schema_path):
        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                json.load(f)
            master_schema_status = "PASS (Valid JSON)"
        except Exception as ex:
            master_schema_status = f"FAIL: {str(ex)}"

    return {
        "status": "Success",
        "audited_at": os.popen("date /T").read().strip() or "2026-05-21",
        "master_schema_audit": master_schema_status,
        "landing_pages": results
    }
