from app.ingestion.parsers.python import CodeSymbol


class CodeChunk:
    def __init__(
        self,
        content: str,
        file_path: str,
        language: str,
        symbol_name: str,
        symbol_type: str,
        parent_symbol: str | None,
        start_line: int,
        end_line: int,
    ) -> None:
        self.content = content
        self.file_path = file_path
        self.language = language
        self.symbol_name = symbol_name
        self.symbol_type = symbol_type
        self.parent_symbol = parent_symbol
        self.start_line = start_line
        self.end_line = end_line


class CodeChunker:
    def chunk(
        self,
        symbols: list[CodeSymbol],
        file_path: str,
        language: str,
    ) -> list[CodeChunk]:
        chunks: list[CodeChunk] = []

        for symbol in symbols:
            # Classes are structural context.
            # Functions and methods are our primary semantic chunks.
            if symbol.symbol_type not in {
                "function",
                "method",
            }:
                continue

            chunks.append(
                CodeChunk(
                    content=symbol.source,
                    file_path=file_path,
                    language=language,
                    symbol_name=symbol.name,
                    symbol_type=symbol.symbol_type,
                    parent_symbol=symbol.parent_symbol,
                    start_line=symbol.start_line,
                    end_line=symbol.end_line,
                )
            )

        return chunks
