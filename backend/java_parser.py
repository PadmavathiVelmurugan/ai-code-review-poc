import javalang


def parse_java_file(java_code: str):
    """
    Parses a Java source file and extracts:
      - Package
      - Type (class/interface/enum)
      - Name
      - Annotations
      - Methods
      - Implements
      - Extends
      - Uses
      - Calls
    """

    try:
        tree = javalang.parse.parse(java_code)

    except Exception as e:
        print("Parse Error:", e)
        return None

    result = {
        "package": None,
        "type": None,
        "name": None,
        "annotations": [],
        "methods": [],
        "implements": [],
        "extends": [],
        "uses": [],
        "calls": {}
    }

    # -------------------------
    # Package
    # -------------------------

    if tree.package:
        result["package"] = tree.package.name

    # -------------------------
    # Find the Java Type
    # -------------------------

    declaration = None

    for _, node in tree.filter(javalang.tree.ClassDeclaration):
        declaration = node
        result["type"] = "class"
        break

    if declaration is None:
        for _, node in tree.filter(javalang.tree.InterfaceDeclaration):
            declaration = node
            result["type"] = "interface"
            break

    if declaration is None:
        for _, node in tree.filter(javalang.tree.EnumDeclaration):
            declaration = node
            result["type"] = "enum"
            break

    if declaration is None:
        return None

    result["name"] = declaration.name

    # -------------------------
    # Annotations
    # -------------------------

    result["annotations"] = [
        ann.name
        for ann in declaration.annotations
    ]

    # -------------------------
    # Methods
    # -------------------------

    result["methods"] = [
        method.name
        for method in declaration.methods
    ]

    # -------------------------
    # Implements
    # -------------------------

    if isinstance(declaration, javalang.tree.ClassDeclaration):

        if declaration.implements:

            result["implements"] = [
                impl.name if hasattr(impl, "name") else str(impl)
                for impl in declaration.implements
            ]


    # -------------------------
    # Extends
    # -------------------------

    if declaration.extends:

        if isinstance(declaration.extends, list):

            result["extends"] = [
                item.name
                for item in declaration.extends
            ]

        else:

            result["extends"] = [
                declaration.extends.name
            ]

    # -------------------------
    # USES
    # (field types)
    # -------------------------

    uses = set()

    for field in declaration.fields:

        if hasattr(field.type, "name"):
            uses.add(field.type.name)

    # -------------------------
    # Method parameter types
    # -------------------------

    for method in declaration.methods:

        for parameter in method.parameters:

            if hasattr(parameter.type, "name"):
                uses.add(parameter.type.name)

    # -------------------------
    # Local variable types
    # -------------------------

    for _, node in declaration.filter(
            javalang.tree.LocalVariableDeclaration):

        if hasattr(node.type, "name"):
            uses.add(node.type.name)

    result["uses"] = sorted(list(uses))

    # -------------------------
    # CALLS
    # -------------------------

    calls = {}

    for method in declaration.methods:

        invoked_methods = []

        for _, invocation in method.filter(
                javalang.tree.MethodInvocation):

            invoked_methods.append(invocation.member)

        calls[method.name] = sorted(list(set(invoked_methods)))

    result["calls"] = calls

    return result