import os
import sys
import json

# Fix CWD for Multiplexer subprocess spawning
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from mcp.server.fastmcp import FastMCP
from health_agent import KeystoneHealthAgent

# Initialize the FastMCP server
mcp = FastMCP("Keystone Health Protocols")
agent = KeystoneHealthAgent()

@mcp.tool()
def search_pubmed(query: str, max_results: int = 3) -> str:
    """
    Search NCBI PubMed database for peptide or health studies.
    Args:
        query: The search term or query (e.g. 'BPC-157 tissue healing').
        max_results: The maximum number of papers to return. Default is 3.
    """
    try:
        results = agent.search_pubmed(query, max_results=max_results)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error searching PubMed: {str(e)}"

@mcp.tool()
def compile_peptide_profile(peptide: str) -> str:
    """
    Compile a comprehensive biological profile of a target peptide,
    pulling from PubMed and applying strict YouTube YMYL compliance rules.
    Args:
        peptide: The target peptide for profiling (e.g. 'BPC-157', 'TB-500', 'Tirzepatide').
    """
    try:
        profile = agent.compile_peptide_profile(peptide)
        return json.dumps(profile, indent=2)
    except Exception as e:
        return f"Error compiling peptide profile: {str(e)}"

@mcp.tool()
def save_peptide_report(peptide: str) -> str:
    """
    Compiles and saves a peptide profile report as a YMYL-safe Markdown file.
    Args:
        peptide: The target peptide name.
    """
    try:
        profile = agent.compile_peptide_profile(peptide)
        filepath = agent.save_report(profile)
        return f"Success: Peptide profile report for '{peptide}' compiled and saved to: {filepath}"
    except Exception as e:
        return f"Error saving peptide report: {str(e)}"

@mcp.tool()
def scrub_ymyl_health(text: str) -> str:
    """
    Scrub text to enforce strict YouTube YMYL guidelines, replacing high-risk medical terms with educational/scientific alternatives.
    Args:
        text: The draft script or text to scrub.
    """
    try:
        scrubbed = agent.scrub_ymyl(text)
        return scrubbed
    except Exception as e:
        return f"Error scrubbing text: {str(e)}"

if __name__ == "__main__":
    mcp.run()
