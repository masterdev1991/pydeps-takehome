#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
import ast
import re
from typing import Dict, Set
import requests
import zipfile
from lib.verse import common

logging = common.logging


def download_and_extract():
    # This can call a shell script if that's preferred or can just be standalone script in `scripts/`
    """
    Download and extract required datasets
    """
    os.makedirs("static_data", exist_ok=True)

    # Download Electricity Load Diagrams
    electricity_url = (
        # "https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014.zip"
        "https://archive.ics.uci.edu/static/public/321/electricityloaddiagrams20112014.zip"
    )
    logging.info("Downloading electricity data", url=electricity_url)

    response = requests.get(electricity_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")
    with open("static_data/electricity.zip", "wb") as f:
        f.write(response.content)

    # Extract and rename
    with zipfile.ZipFile("static_data/electricity.zip", "r") as zip_ref:
        zip_ref.extractall("static_data/")

    # Rename LD2011_2014.txt to LD2011_2014.csv
    if os.path.exists("static_data/LD2011_2014.txt"):
        os.rename("static_data/LD2011_2014.txt", "static_data/LD2011_2014.csv")

    # Clean up
    os.remove("static_data/electricity.zip")
    if os.path.exists("static_data/__MACOSX"):
        import shutil

        shutil.rmtree("static_data/__MACOSX")

    # Download Enron emails
    enron_url = "https://raw.githubusercontent.com/adriancampos1/Enron_Email_Analysis/master/data/enron_emails_1702.csv"
    logging.info("downloading_enron_data", url=enron_url)

    response = requests.get(enron_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: {response.status_code}")
    with open("static_data/enron_emails_1702.csv", "wb") as f:
        f.write(response.content)

    logging.info("download_complete")


def extract_imports_from_file(file_path: str) -> Set[str]:
    """Extract import statements from Python file"""
    imports = set()
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
    except Exception as e:
        logging.warning("failed_to_parse", file=file_path, error=str(e))

    return imports


def get_package_version(package: str) -> str:
    """Get latest version of a package from PyPI"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "index", "versions", package],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            # Parse output to get latest version
            lines = result.stdout.split("\n")
            for line in lines:
                if "Available versions:" in line:
                    versions = line.split(":")[1].strip().split(",")
                    return versions[0].strip()
    except Exception as e:
        logging.warning("failed_to_get_version", package=package, error=str(e))

    # Fallback: try pip show
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if line.startswith("Version:"):
                    return line.split(":")[1].strip()
    except Exception:
        pass

    return "unknown"


def read_pyproject_dependencies() -> Dict[str, str]:
    """Read current dependencies from pyproject.toml"""
    deps = {}
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()

        # Simple regex to extract dependencies
        in_deps_section = False
        for line in content.split("\n"):
            line = line.strip()
            if line == "[project]" or line.startswith("dependencies"):
                in_deps_section = True
                continue
            if in_deps_section and line.startswith("["):
                break
            if in_deps_section and "==" in line:
                # Extract package==version
                match = re.search(r'"([^"]+)==([^"]+)"', line)
                if match:
                    deps[match.group(1)] = match.group(2)
    except Exception as e:
        logging.warning("failed_to_read_pyproject", error=str(e))

    return deps


def align_python_deps():
    """
    Inspect apps for dependency alignment and suggest updates
    """
    logging.info("analyzing_dependencies")

    # Map of known package mappings
    PACKAGE_MAPPINGS = {
        "sklearn": "scikit-learn",
        "cv2": "opencv-python",
        "PIL": "Pillow",
    }

    # Required dependencies per app
    app_dependencies = {
        "server-one": {"fastapi", "uvicorn"},
        "server-two": {"fastapi", "uvicorn", "pandas", "numpy"},
        "job-a": {"scikit-learn", "pandas", "numpy"},
        "job-b": {"sentence-transformers", "pandas"},
        "job-c": {"numpy", "pandas"},
    }

    # Current pyproject.toml dependencies
    current_deps = read_pyproject_dependencies()

    # Collect all unique dependencies
    all_deps = set()
    for deps in app_dependencies.values():
        all_deps.update(deps)

    # Check version requirements
    suggestions = []

    for package in sorted(all_deps):
        mapped_package = PACKAGE_MAPPINGS.get(package, package)

        # Special handling for numpy version conflict
        if package == "numpy":
            # job-c needs numpy>=2.3.0, check if this works for all apps
            logging.info("checking_numpy_compatibility")
            suggestions.append(
                "numpy==2.3.1  # Required by job-c, verify compatibility"
            )
            continue

        # Get latest version
        latest_version = get_package_version(mapped_package)
        if latest_version != "unknown":
            current_version = current_deps.get(mapped_package, "not_installed")
            if current_version == "not_installed":
                suggestions.append(f"{mapped_package}=={latest_version}")
            else:
                suggestions.append(
                    f"{mapped_package}=={latest_version}  # current: {current_version}"
                )

    # Print aligned dependencies
    logging.info("dependency_alignment_suggestions")
    for suggestion in suggestions:
        print(suggestion)

    logging.info("alignment_complete", total_suggestions=len(suggestions))


def main():
    parser = argparse.ArgumentParser(description="Take-home project utilities")
    parser.add_argument(
        "command", choices=["download-data", "align-deps"], help="Command to execute"
    )

    args = parser.parse_args()

    if args.command == "download-data":
        download_and_extract()
    elif args.command == "align-deps":
        align_python_deps()


if __name__ == "__main__":
    main()
