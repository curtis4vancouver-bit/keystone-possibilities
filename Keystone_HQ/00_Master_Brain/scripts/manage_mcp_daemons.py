"""
MCP Daemon Manager (Stub)
==========================

The bootstrap skill references ``manage_mcp_daemons.py`` to start local
MCP servers.  In the current architecture, MCP servers are managed by
Antigravity's ``mcp_config.json`` and start automatically.  This script
exists as a no-op stub so the bootstrap doesn't crash on import.

If Wayne later runs self-hosted MCP servers (e.g., Qdrant, custom tools),
this script will be expanded to manage their lifecycle.
"""

import sys
from config import logger


def start():
    """Check MCP daemon availability (stub)."""
    logger.info("MCP daemons are managed by Antigravity mcp_config.json.")
    logger.info("No manual daemon management needed.")


def stop():
    """Stop MCP daemons (stub)."""
    logger.info("Daemons are process-managed by Antigravity. No action taken.")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "start"
    if action == "start":
        start()
    elif action == "stop":
        stop()
    else:
        logger.warning("Unknown action: %s (use 'start' or 'stop')", action)
