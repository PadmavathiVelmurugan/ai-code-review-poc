import javalang

def extract_method_body(lines, start_line):
    """
    Tracks matching curly braces from a given starting line 
    to extract a complete, isolated method block.
    """
    method_lines = []
    brace_count = 0
    started = False
    
    # Iterate through the code lines starting from the method definition
    for i in range(start_line - 1, len(lines)):
        line = lines[i]
        method_lines.append(line)
        
        # Count curly brackets to track the method block boundaries
        for char in line:
            if char == '{':
                brace_count += 1
                started = True
            elif char == '}':
                brace_count -= 1
        
        # Once the brackets balance back to zero, the method block is complete
        if started and brace_count <= 0:
            break
            
    return "\n".join(method_lines)


def chunk_java_ast(code):
    """
    Splits Java code into precise method-level chunks using AST parsing.
    
    Returns:
        chunks: A list of isolated method strings
        metadata: A list of dicts containing method names and their line positions
    """
    try:
        tree = javalang.parse.parse(code)
    except Exception as e:
        print(f"AST Parsing failed: {e}. Falling back to full file chunk.")
        # Fallback safety: return full file if it is an invalid or partial Java snippet
        return [code], [{"method": "FullFileFallback", "line": 1}]

    chunks = []
    metadata = []
    lines = code.splitlines()

    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        # Extract metadata
        start_line = node.position.line if node.position else 0
        
        if start_line == 0:
            continue
            
        # Isolate the exact method code block
        method_code = extract_method_body(lines, start_line)
        
        metadata.append({
            "method": node.name,
            "line": start_line
        })
        chunks.append(method_code)

    # Secondary Fallback: If the file is valid Java but contains no methods (e.g., a pure Interface)
    if not chunks:
        return [code], [{"method": "ClassBodyOrInterface", "line": 1}]

    return chunks, metadata
