# app/ingestion/safe_parser.py
import multiprocessing
import traceback

from app.ingestion.parsers.python import CodeSymbol, PythonParser


def _parse_worker(source_bytes: bytes, result_queue) -> None:
    try:
        parser = PythonParser()
        symbols = parser.parse(source_bytes)
        result_queue.put(("ok", symbols))
    except Exception:
        result_queue.put(("error", traceback.format_exc()))


def safe_parse_python(
    source: str | bytes, timeout: int = 10
) -> tuple[str, list[CodeSymbol] | str]:
    """
    Parses Python source in a separate process so a tree-sitter
    C-level crash (segfault) cannot kill the main ingestion worker.

    Returns:
        ("ok", symbols)      -> parsing succeeded
        ("error", traceback) -> a normal Python exception occurred
        ("crash", message)   -> the subprocess died (segfault/timeout)
    """
    source_bytes = source.encode("utf-8") if isinstance(source, str) else source

    ctx = multiprocessing.get_context("spawn")
    result_queue = ctx.Queue()
    process = ctx.Process(target=_parse_worker, args=(source_bytes, result_queue))
    process.start()
    process.join(timeout=timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        return ("crash", f"Parsing timed out after {timeout}s")

    if process.exitcode != 0:
        return (
            "crash",
            f"Parser process exited with code {process.exitcode} (likely segfault)",
        )

    if result_queue.empty():
        return ("crash", "Parser process died without returning a result")

    return result_queue.get()
