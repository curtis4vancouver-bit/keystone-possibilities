import os
import sys
import json

# Fix CWD for Multiplexer subprocess spawning
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from mcp.server.fastmcp import FastMCP
from research_agent import KeystoneResearchAgent

# Initialize the FastMCP server
mcp = FastMCP("Keystone Deep Research & Competitor Intelligence")
agent = KeystoneResearchAgent()

@mcp.tool()
def run_seo_indexation_audit(target_url: str) -> str:
  """
  Audits sitemap indexing speed and analyzes crucial Knowledge Panel schema markup elements on the target URL.
  Args:
      target_url: The target sitemap or page URL to analyze.
  """
  try:
    report = agent.run_seo_audit(target_url)
    return json.dumps(report, indent=2)
  except Exception as e:
    return f"Error running sitemap index audit: {str(e)}"

@mcp.tool()
def compile_competitor_keyword_report() -> str:
  """
  Reads the competitor intelligence database and compiles an aggregated frequency report of top B2B builder keywords and YouTube tags.
  """
  try:
    report = agent.get_competitor_keyword_report()
    return json.dumps(report, indent=2)
  except Exception as e:
    return f"Error compiling keyword report: {str(e)}"

if __name__ == "__main__":
  mcp.run()
