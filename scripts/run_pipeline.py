"""
Utility CLI to orchestrate the synthetic e-commerce pipeline.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"


def run_script(script: str) -> None:
    script_path = SCRIPTS_DIR / script
    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")
    subprocess.run([sys.executable, str(script_path)], check=True)


def run_all() -> None:
    run_script("generate_data.py")
    run_script("ingest_data.py")
    run_script("query_data.py")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run stages of the e-commerce data pipeline.",
    )
    parser.add_argument(
        "stage",
        choices=["generate", "ingest", "query", "all"],
        help="Pipeline stage to execute.",
    )
    args = parser.parse_args()

    if args.stage == "generate":
        run_script("generate_data.py")
    elif args.stage == "ingest":
        run_script("ingest_data.py")
    elif args.stage == "query":
        run_script("query_data.py")
    else:
        run_all()


if __name__ == "__main__":
    main()

