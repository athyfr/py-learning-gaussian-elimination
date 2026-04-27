"""A module that loads the ``matrix_test_cases.json`` file."""
import json
from pathlib import Path

matrices: dict[str, dict]
with Path("matrix_test_cases.json").open() as f:
    matrices: dict[str, dict] = json.load(f)
