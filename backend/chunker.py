import javalang


def chunk_java_ast(code):
    """
    Splits Java code into method-level chunks using AST.
    Returns:
        chunks: list of method code (currently placeholders)
        metadata: method names and line numbers
    """

    tree = javalang.parse.parse(code)

    chunks = []
    metadata = []

    lines = code.splitlines()

    for _, node in tree.filter(javalang.tree.MethodDeclaration):

        metadata.append({
            "method": node.name,
            "line": node.position.line if node.position else 0
        })

        # Placeholder: stores the full file for now
        # Later you can extract the exact method body
        chunks.append("\n".join(lines))

    return chunks, metadata