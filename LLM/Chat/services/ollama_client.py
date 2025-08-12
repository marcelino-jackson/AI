from __future__ import annotations
import json
import shutil
import subprocess
from typing import Callable, Iterable, List, Optional


def _ollama_available() -> bool:
    return shutil.which("ollama") is not None


def list_models() -> List[str]:
    """Return a list of installed Ollama model names.

    Tries `ollama list --json` (NDJSON). Falls back to parsing table output.
    """
    # Prefer JSON (newline-delimited)
    try:
        result = subprocess.run(
            ["ollama", "list", "--json"],
            capture_output=True,
            text=True,
            check=True,
        )
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

    # Fallback: human table
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = [ln.strip() for ln in result.stdout.splitlines() if ln.strip()]
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


# ---------- Synchronous (blocking) full generation ----------
def generate(model: str, prompt: str, timeout: Optional[int] = None) -> str:
    """Run `prompt` against `model` using the Ollama CLI and return full text."""
    if not _ollama_available():
        raise RuntimeError("Ollama is not installed or not on PATH.")
    if not model or model.startswith("("):
        raise ValueError("Please select a valid model in the sidebar.")

    result = subprocess.run(
        ["ollama", "run", model, prompt],
        text=True,
        capture_output=True,
        check=True,
        timeout=timeout,
    )
    return (result.stdout or "").strip()


# ---------- Streaming (line/chunk) generation ----------
def generate_stream(model: str, prompt: str) -> Iterable[str]:
    """Yield chunks (stdout lines) as Ollama streams output."""
    if not _ollama_available():
        raise RuntimeError("Ollama is not installed or not on PATH.")
    if not model or model.startswith("("):
        raise ValueError("Please select a valid model in the sidebar.")

    # Popen with prompt as an argument streams tokens to stdout
    proc = subprocess.Popen(  # nosec - local CLI call
        ["ollama", "run", model, prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    try:
        if proc.stdout is not None:
            for line in proc.stdout:
                if line:
                    yield line
        proc.wait()
        if proc.returncode != 0:
            err = (proc.stderr.read() if proc.stderr else "") or "Unknown error"
            raise RuntimeError(err.strip())
    finally:
        try:
            if proc.stdout:
                proc.stdout.close()
            if proc.stderr:
                proc.stderr.close()
        except Exception:
            pass


def generate_with_progress(
    model: str, prompt: str, on_chunk: Optional[Callable[[str], None]] = None
) -> str:
    """Stream chunks, call `on_chunk` for each, and return the full text."""
    out: List[str] = []
    for chunk in generate_stream(model, prompt):
        out.append(chunk)
        if on_chunk:
            on_chunk(chunk)
    return "".join(out).strip()