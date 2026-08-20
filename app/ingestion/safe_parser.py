# app/ingestion/safe_parser.py

import base64
import json
import subprocess
import sys

_WORKER_SCRIPT = """
import sys, base64, json

def main():
    encoded = sys.stdin.readline()
    source_bytes = base64.b64decode(encoded)
    try:
        from app.ingestion.parsers.python import PythonParser
        parser = PythonParser()
        symbols = parser.parse(source_bytes)
        result = {
            "status": "ok",
            "symbols": [
                {
                    "name": s.name,
                    "symbol_type": s.symbol_type,
                    "start_line": s.start_line,
                    "end_line": s.end_line,
                    "source": s.source,
                    "parent_symbol": s.parent_symbol,
                }
                for s in symbols
            ],
        }
    except Exception as exc:
        result = {"status": "error", "message": str(exc)}

    print(json.dumps(result))

if __name__ == "__main__":
    main()
"""


def safe_parse_python(source: str | bytes, timeout: int = 30):
    """
    Parses Python source in a completely separate OS process
    (via `python -c`) so a tree-sitter C-level crash cannot kill
    the main server, and so uvicorn's --reload watcher / spawn
    re-import behavior on Windows cannot cause a deadlock.
    """
    from app.ingestion.parsers.python import CodeSymbol

    source_bytes = source.encode("utf-8") if isinstance(source, str) else source
    encoded = base64.b64encode(source_bytes).decode("ascii")

    try:
        proc = subprocess.run(
            [sys.executable, "-c", _WORKER_SCRIPT],
            input=encoded + "\n",
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return ("crash", f"Parsing timed out after {timeout}s")

    if proc.returncode != 0:
        return (
            "crash",
            f"Parser process exited with code {proc.returncode} (likely segfault)",
        )

    if not proc.stdout.strip():
        return ("crash", "Parser process produced no output")

    try:
        result = json.loads(proc.stdout.strip().splitlines()[-1])
    except json.JSONDecodeError:
        return ("crash", f"Could not parse worker output: {proc.stdout[:200]}")

    if result["status"] == "error":
        return ("error", result["message"])

    symbols = [
        CodeSymbol(
            name=s["name"],
            symbol_type=s["symbol_type"],
            start_line=s["start_line"],
            end_line=s["end_line"],
            source=s["source"],
            parent_symbol=s["parent_symbol"],
        )
        for s in result["symbols"]
    ]
    return ("ok", symbols)
