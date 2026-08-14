from app.ingestion.parsers.python import PythonParser


def print_node(node, indent=0):
    """Recursively prints Tree-sitter AST nodes with indentation."""
    # Format line range for readability
    line_start, col_start = node.start_point
    line_end, col_end = node.end_point
    location = f"[{line_start}:{col_start} - {line_end}:{col_end}]"

    print(f"{'  ' * indent}└─ {node.type} {location}")

    for child in node.children:
        print_node(child, indent + 1)


def main():
    sample_code = b"""class AuthService:
    def login(self, username, password):
        return True

    def verify_token(self, token):
        return True
"""

    parser = PythonParser()
    root_node = parser.parse(sample_code)

    print("--- Tree-sitter AST Root Node ---")
    print(f"Root Type: {root_node.type}\n")

    print("--- Full Syntax Tree ---")
    print_node(root_node)


if __name__ == "__main__":
    main()
