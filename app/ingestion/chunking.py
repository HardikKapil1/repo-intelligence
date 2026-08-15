from dataclasses import dataclass

from app.ingestion.parsers.python import CodeSymbol


@dataclass(frozen=True)
class CodeChunk:
    content: str
    file_path: str
    language: str
    symbol_name: str
    symbol_type: str
    parent_symbol: str | None
    start_line: int
    end_line: int


class CodeChunker:
    def chunk(
        self,
        symbols: list[CodeSymbol],
        file_path: str,
        language: str,
    ) -> list[CodeChunk]:
        chunks: list[CodeChunk] = []

        for symbol in symbols:
            # Standalone functions and class methods both form chunking units
            if symbol.symbol_type in {"function", "method"}:
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
