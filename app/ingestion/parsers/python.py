# app/ingestion/parsers/python.py
from dataclasses import dataclass

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor


@dataclass(frozen=True)
class CodeSymbol:
    name: str
    symbol_type: str
    start_line: int
    end_line: int
    source: str
    parent_symbol: str | None


MAX_SOURCE_BYTES = 1_000_000


class PythonParser:
    def __init__(self) -> None:
        language = Language(tspython.language())

        self.parser = Parser(language)

        self.query = Query(
            language,
            """
            (class_definition) @class
            (function_definition) @function
            """,
        )

    def parse(self, source: str | bytes) -> list[CodeSymbol]:
        source_bytes = source.encode("utf-8") if isinstance(source, str) else source

        tree = self.parser.parse(source_bytes)

        cursor = QueryCursor(self.query)
        captures = cursor.captures(tree.root_node)

        symbols: list[CodeSymbol] = []

        # Classes
        for node in captures.get("class", []):
            symbol = self._build_symbol(
                node=node,
                source_bytes=source_bytes,
                symbol_type="class",
            )

            if symbol is not None:
                symbols.append(symbol)

        # Functions
        for node in captures.get("function", []):
            symbol = self._build_symbol(
                node=node,
                source_bytes=source_bytes,
                symbol_type="function",
            )

            if symbol is not None:
                symbols.append(symbol)

        symbols.sort(
            key=lambda symbol: (
                symbol.start_line,
                symbol.end_line,
            )
        )

        return symbols

    @staticmethod
    def _build_symbol(
        node,
        source_bytes: bytes,
        symbol_type: str,
    ) -> CodeSymbol | None:

        name_node = node.child_by_field_name("name")

        if name_node is None:
            return None

        name = source_bytes[name_node.start_byte : name_node.end_byte].decode("utf-8")

        source_text = source_bytes[node.start_byte : node.end_byte].decode("utf-8")

        start_line = node.start_point.row + 1

        # Calculate from actual source text.
        end_line = start_line + source_text.count("\n")

        # Guard against tree-sitter node metadata corruption
        # (rare, seen after deeply nested function definitions):
        # produces insane start_line values that blow past any
        # real file's line count and overflow DB integer columns.
        max_lines = source_bytes.count(b"\n") + 1
        if start_line < 1 or start_line > max_lines or end_line < start_line:
            return None

        return CodeSymbol(
            name=name,
            symbol_type=symbol_type,
            start_line=start_line,
            end_line=end_line,
            source=source_text,
            parent_symbol=None,
        )
