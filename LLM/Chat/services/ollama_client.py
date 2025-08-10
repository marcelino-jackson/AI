from __future__ import annotations
import json
import shutil
import subprocess
from typing import List


def _ollama_available() -> bool:
    return shutil.which("ollama") is not None


def list_models() -> List[str]:
    """Return a list of installed Ollama model names.

    Uses `ollama list --json` (NDJSON). Falls back to `ollama list` table parse.
    Raises CalledProcessError on CLI failure.
    """
    # Prefer JSON (newline-delimited JSON objects)
    try:
        result = subprocess.run(["ollama", "list", "--json"], capture_output=True, text=True, check=True)
        names: List[str] = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            name = obj.get("name")
            if name:
                names.append(name)
        if names:
            return names
    except Exception:
        pass

    # Fallback: parse the human table output
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
    lines = [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]
    # Skip header if present (e.g., NAME SIZE MODIFIED)
    if lines and lines[0].lower().startswith("name"):
        lines = lines[1:]
    return [ln.split()[0] for ln in lines]


def list_models_safe() -> List[str]:
    if not _ollama_available():
        return ["(ollama not found)"]
    try:
        models = list_models()
        return models or ["(no models installed)"]
    except Exception as exc:  # pragma: no cover
        return [f"(error: {exc})"]