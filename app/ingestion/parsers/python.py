from dataclasses import dataclass

import tree_sitter_python as tspython
from tree_sitter import Language, Parser


@dataclass(frozen=True)
class CodeSymbol:
    name: str
    symbol_type: str  # "class", "function", or "method"
    start_line: int
    end_line: int
    source: str
    parent_symbol: str | None


class PythonParser:
    def __init__(self) -> None:
        language = Language(tspython.language())
        self.parser = Parser(language)

    def parse(self, source: str | bytes) -> list[CodeSymbol]:
        source_bytes = source.encode("utf-8") if isinstance(source, str) else source

        tree = self.parser.parse(source_bytes)
        symbols: list[CodeSymbol] = []

        self._walk(
            node=tree.root_node,
            source_bytes=source_bytes,
            symbols=symbols,
            parent_symbol=None,
        )

        return symbols

    def _walk(
        self,
        node,
        source_bytes: bytes,
        symbols: list[CodeSymbol],
        parent_symbol: str | None,
    ) -> None:
        current_symbol = parent_symbol

        if node.type in {"class_definition", "function_definition"}:
            name_node = node.child_by_field_name("name")

            if name_node is not None:
                name = source_bytes[name_node.start_byte : name_node.end_byte].decode(
                    "utf-8"
                )

                if node.type == "class_definition":
                    symbol_type = "class"
                else:
                    # Differentiate method vs standalone function
                    symbol_type = "method" if parent_symbol is not None else "function"

                source = source_bytes[node.start_byte : node.end_byte].decode("utf-8")

                symbols.append(
                    CodeSymbol(
                        name=name,
                        symbol_type=symbol_type,
                        start_line=node.start_point.row + 1,
                        end_line=node.end_point.row + 1,
                        source=source,
                        parent_symbol=parent_symbol,
                    )
                )

                current_symbol = name

        for child in node.children:
            self._walk(
                node=child,
                source_bytes=source_bytes,
                symbols=symbols,
                parent_symbol=current_symbol,
            )
