import os
import sys
import json

# Fix CWD for Multiplexer subprocess spawning
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from mcp.server.fastmcp import FastMCP
from dev_agent import KeystoneDevAgent

# Initialize the FastMCP server
mcp = FastMCP("Keystone PWA & DB Developer")
agent = KeystoneDevAgent()

@mcp.tool()
def run_pwa_diagnostics() -> str:
  """
  Runs a comprehensive environment audit of the local construction PWA workspace.
  Checks paths, subfolders, and flags any developer architecture issues.
  """
  try:
    report = agent.run_diagnostics()
    return json.dumps(report, indent=2)
  except Exception as e:
    return f"Error running developer diagnostics: {str(e)}"

@mcp.tool()
def generate_supabase_trigger_hotfix() -> str:
  """
  Generates and saves the Supabase SQL database recovery script to restore the public profile auto-creation trigger.
  Returns the file path where the patch was saved.
  """
  try:
    path = agent.generate_supabase_hotfix()
    return f"Success: Supabase trigger patch written to: {path}\nCopy and execute this file inside your Supabase SQL Editor."
  except Exception as e:
    return f"Error generating Supabase trigger patch: {str(e)}"

@mcp.tool()
def package_capacitor_android_apk() -> str:
  """
  Runs the android-cli Capacitor packaging and Gradle build routine to compile the hybrid Next.js/Vite PWA into a physical app-release.apk.
  """
  try:
    log = agent.build_android_apk()
    return log
  except Exception as e:
    return f"Error compiling Android platform: {str(e)}"

if __name__ == "__main__":
  mcp.run()
