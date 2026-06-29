# git_wrapper.py
import sys
import os
import logging
from pathlib import Path

# Set up logging to a local file for debugging
log_file = Path(__file__).parent / "git_wrapper.log"
logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info(f"Command line arguments received: {sys.argv}")
logging.info(f"Current working directory: {os.getcwd()}")

def find_git_root(start_path: Path) -> Path | None:
    try:
        current = start_path.resolve()
        while current != current.parent:
            if (current / ".git").is_dir():
                return current
            current = current.parent
    except Exception as e:
        logging.error(f"Error resolving path {start_path}: {e}")
    return None

new_args = sys.argv.copy()

# Find if --repository or -r is already in arguments
repo_idx = -1
for i, arg in enumerate(new_args):
    if arg in ("--repository", "-r"):
        repo_idx = i
        break

if repo_idx != -1 and repo_idx + 1 < len(new_args):
    provided_path = Path(new_args[repo_idx + 1])
    logging.info(f"Provided repository path in args: {provided_path}")
    git_root = find_git_root(provided_path)
    if git_root:
        logging.info(f"Found git root for provided path: {git_root}")
        new_args[repo_idx + 1] = str(git_root)
    else:
        logging.warning(f"No git root found for provided path {provided_path}")
else:
    # If no repository path is provided in arguments, find git root of CWD
    cwd = Path.cwd()
    git_root = find_git_root(cwd)
    if git_root:
        logging.info(f"No repository arg provided. Found git root from CWD: {git_root}")
        new_args.extend(["--repository", str(git_root)])
    else:
        logging.warning("No git root found from CWD and no repository arg provided.")

# Log modified arguments
logging.info(f"Modified command line arguments: {new_args}")

# Update sys.argv so mcp_server_git sees the modified arguments
sys.argv = new_args

# Run the real mcp_server_git main
try:
    import mcp_server_git
    logging.info("Imported mcp_server_git successfully. Starting main...")
    mcp_server_git.main()
except Exception as e:
    logging.error(f"Failed to run mcp_server_git: {e}", exc_info=True)
    sys.exit(1)
