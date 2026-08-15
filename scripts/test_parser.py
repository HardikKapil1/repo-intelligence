from app.ingestion.chunking import CodeChunker
from app.ingestion.parsers.python import PythonParser


def main():
    parser = PythonParser()
    chunker = CodeChunker()

    sample_code = """
def standalone_func():
    return "I am a function"

class AuthService:
    def login(self, username, password):
        return True

    def verify_token(self, token):
        return True
"""

    symbols = parser.parse(sample_code)

    print("--- Extracted Code Symbols ---")
    for symbol in symbols:
        print(
            f"[{symbol.symbol_type.upper()}] {symbol.name} "
            f"(Lines {symbol.start_line}-{symbol.end_line}) "
            f"Parent: {symbol.parent_symbol}"
        )

    file_path = "src/auth.py"
    language = "python"
    chunks = chunker.chunk(symbols, file_path=file_path, language=language)

    print("\n--- Generated Code Chunks ---")
    for idx, chunk in enumerate(chunks, 1):
        parent_info = f"{chunk.parent_symbol}." if chunk.parent_symbol else ""
        print(
            f"Chunk #{idx} | [{chunk.symbol_type.upper()}] {parent_info}{chunk.symbol_name} "
            f"({chunk.file_path}:{chunk.start_line}-{chunk.end_line})"
        )


if __name__ == "__main__":
    main()
