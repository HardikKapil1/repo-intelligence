from pathlib import Path

from app.ingestion.parsers.python import PythonParser

REPOSITORY_ID = "6774d8f9-4ca9-4b23-bab6-ba8aad9d9812"

FILE_PATH = Path("data/test_slice.py")


def main() -> None:
    print(f"Testing: {FILE_PATH}", flush=True)

    source = FILE_PATH.read_text(
        encoding="utf-8",
        errors="replace",
    )

    print(
        f"Characters: {len(source)}",
        flush=True,
    )

    print("[DEBUG] Creating parser", flush=True)

    parser = PythonParser()

    print("[DEBUG] Parser created", flush=True)

    print("[DEBUG] Calling parse()", flush=True)

    symbols = parser.parse(source)

    print(
        f"[DEBUG] parse() returned {len(symbols)} symbols",
        flush=True,
    )

    print("\n=== SYMBOLS ===", flush=True)

    for symbol in symbols:
        parent = f" Parent: {symbol.parent_symbol}" if symbol.parent_symbol else ""

        print(
            f"[{symbol.symbol_type.upper()}] "
            f"{symbol.name} "
            f"{symbol.start_line}-{symbol.end_line}"
            f"{parent}",
            flush=True,
        )


if __name__ == "__main__":
    main()
