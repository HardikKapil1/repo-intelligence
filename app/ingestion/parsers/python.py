import tree_sitter_python as tspython
from tree_sitter import Language, Node, Parser


class PythonParser:
    def __init__(self) -> None:
        # Load the Python language grammar into tree-sitter
        self._language = Language(tspython.language())
        self._parser = Parser(self._language)

    def parse(self, source_code: bytes) -> Node:
        """Parses Python source code bytes into a Tree-sitter AST root node."""
        tree = self._parser.parse(source_code)
        return tree.root_node
