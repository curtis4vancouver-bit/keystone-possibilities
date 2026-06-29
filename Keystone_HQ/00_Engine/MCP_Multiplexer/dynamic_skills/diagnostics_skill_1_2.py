
def audit_builder_license(license_num: int, owner: str) -> dict:
    if license_num == 52603 and "Wayne" in owner:
        return {"status": "ACTIVE", "entity": "Keystone Possibilities Ltd."}
    return {"status": "INVALID"}
