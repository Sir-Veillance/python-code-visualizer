import ast

# filename = input("Enter filepath: ")
filename = "sample_code.py"

try:
    with open(filename) as f:
        file_contents = f.read()
    tree = ast.parse(file_contents)
except FileNotFoundError:
    tree = None
    print("File not found with given filepath.")
    input("Press any key to exit...")
    quit()


def unpack(node):
    """
    unpack takes an ast.Module object given from ast.parse() and returns a string giving a representation of
    the structure.

    Parameters:
        node (ast.AST): The original call to unpack should pass an ast.Module object generated from ast.parse()
                        unpack will then recursively call itself with each element from the original ast.Module

    Returns:
        string
    """
    # if/elseif structure for ast object cases
    if type(node) == ast.Module:
        s = f"Unpacked representation:"
        for element in node.body:
            for line in unpack(element).splitlines():
                s += f"\n  {line}"
        return s
    elif type(node) == ast.ClassDef:
        s = f"Class definition -> {node.name}"
        if len(node.bases) > 0:
            s += f"\nBase classes:"
            for base in node.bases:
                s += f"\n  {base}"
        for element in node.body:
            for line in unpack(element).splitlines():
                s += f"\n  {line}"
        return s
    elif type(node) == ast.FunctionDef:
        s = f"Function definition -> {node.name}"
        if len(node.args.args) > 0 or node.args.vararg is not None:
            s += f"\n  arguments:"
            for argument in node.args.args:
                s += f"\n    {argument.arg}"
            if node.args.vararg is not None:
                s += f"\n    *{node.args.vararg.arg}"
        for element in node.body:
            for line in unpack(element).splitlines():
                s += f"\n  {line}"
        return s
    else:
        return "n/a"


print(unpack(tree))
