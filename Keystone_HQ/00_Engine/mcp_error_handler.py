import sys
import os
import functools
import traceback
from datetime import datetime

# Add scripts directory to path to import config
SCRIPTS_DIR = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts"
if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

try:
    from config import ERROR_TYPES, logger
except ImportError:
    ERROR_TYPES = {}
    import logging
    logger = logging.getLogger("mcp_error")

def safe_mcp_tool(func):
    """
    Decorator that wraps MCP tool functions to provide structured error responses
    and prevent raw stack traces from being exposed to the LLM.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_msg = str(e).lower()
            error_type = "unknown"
            
            # Simple heuristic mapping to taxonomy
            if "timeout" in err_msg:
                error_type = "timeout"
            elif "auth" in err_msg or "credentials" in err_msg or "token" in err_msg:
                error_type = "auth"
            elif "rate" in err_msg or "429" in err_msg or "quota" in err_msg:
                error_type = "rate_limit"
            elif "permission" in err_msg or "access denied" in err_msg:
                error_type = "permission_denied"
            elif "not found" in err_msg or "404" in err_msg:
                error_type = "not_found"
            elif "connection" in err_msg or "network" in err_msg or "socket" in err_msg:
                error_type = "network_error"
                
            taxonomy = ERROR_TYPES.get(error_type, {"retryable": False, "action": "log_and_notify"})
            
            # Log full stack trace internally
            logger.error(f"MCP Tool Error in {func.__name__}: {traceback.format_exc()}")
            
            # Return structured response to LLM
            return {
                "isError": True,
                "error_type": error_type,
                "message": str(e),
                "suggestion": f"Recommended action: {taxonomy.get('action', 'check logs')}",
                "retry_after_seconds": taxonomy.get("base_s", 5) if taxonomy.get("retryable") else 0,
                "retryable": taxonomy.get("retryable", False)
            }
            
    return wrapper
