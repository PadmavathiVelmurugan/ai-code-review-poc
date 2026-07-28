import javalang


def extract_method_body(lines, start_line):

    method_lines = []

    brace_count = 0
    started = False


    for i in range(start_line - 1, len(lines)):

        line = lines[i]

        method_lines.append(line)


        for char in line:

            if char == "{":

                brace_count += 1
                started = True


            elif char == "}":

                brace_count -= 1


        if started and brace_count == 0:

            break


    return "\n".join(method_lines)



def chunk_java_ast(code):

    try:

        tree = javalang.parse.parse(code)


    except Exception as e:

        print(
            "AST parsing failed:",
            e
        )


        return (
            [code],
            [
                {
                    "method": "FullFile",
                    "line": 1
                }
            ]
        )



    chunks = []

    metadata = []


    lines = code.splitlines()



    for _, node in tree.filter(
        javalang.tree.MethodDeclaration
    ):


        if not node.position:

            continue



        start_line = node.position.line



        method_code = extract_method_body(
            lines,
            start_line
        )



        chunks.append({
           "name": node.name,
           "code": method_code,
           "start_line": start_line,
           "end_line": start_line + method_code.count("\n")})

        metadata.append(
            {
                "method": node.name,
                "line": start_line
            }
        )



    if not chunks:

     chunks.append({
        "name": "ClassBody",
        "code": code,
        "start_line": 1,
        "end_line": code.count("\n") + 1
     })

     metadata.append({
        "method": "ClassBody",
        "line": 1,
        "end_line": code.count("\n") + 1
     })



    print("==============================")
    print("AST CHUNKS")


    for meta in metadata:

        print(meta)


    print("==============================")



    return chunks, metadata