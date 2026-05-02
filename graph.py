"""Convenience import for running the app.

Allows: `from graph import compiled_workflow` from anywhere when the current
working directory is the `pydantic/` project root.

This repo keeps the actual LangGraph definition in `scripts/graph.py`.
"""

from __future__ import annotations

import sys
import runpy
from pathlib import Path


_SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

_globals = runpy.run_path(str(_SCRIPTS_DIR / "graph.py"))
compiled_workflow = _globals["compiled_workflow"]
