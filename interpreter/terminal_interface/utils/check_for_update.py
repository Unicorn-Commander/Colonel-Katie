import importlib.metadata
import requests
from packaging import version


def check_for_update():
    # Fetch the latest version from the PyPI API
    response = requests.get(f"https://pypi.org/pypi/open-interpreter/json")
    latest_version = response.json()["info"]["version"]

    # Get the current version using pkg_resources
    try:
        current_version = importlib.metadata.version("open-interpreter")
    except importlib.metadata.PackageNotFoundError:
        current_version = "0.4.3-the-colonel"

    return version.parse(latest_version) > version.parse(current_version)
