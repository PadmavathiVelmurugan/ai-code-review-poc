import javalang


def get_method_metadata(code):

    tree = javalang.parse.parse(code)

    methods = []

    for _, node in tree.filter(javalang.tree.MethodDeclaration):

        methods.append(
            {
                "method": node.name,
                "line": node.position.line
            }
        )

    return methods