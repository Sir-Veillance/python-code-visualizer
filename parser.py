import ast

# filename = input("Enter filepath: ")
filename = "testcode/sample_code.py"

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
        s = process_class_def(node)
        return s
    elif type(node) == ast.FunctionDef:
        s = process_function_def(node)
        return s
    elif type(node) == ast.Assign:
        s = process_assign(node)
        return s
    else:
        return "<unimplemented>"


def process_class_def(node):
    # TODO add information about decorators
    s = f"Class definition: {node.name}"
    if len(node.bases) > 0:
        s += f"\nBase classes:"
        for base in node.bases:
            s += f"\n  {base}"
    for element in node.body:
        for line in unpack(element).splitlines():
            s += f"\n  {line}"
    return s


def process_function_def(node):
    # TODO add information about all argument types (not just args and vararg)
    # TODO add information about decorators
    # TODO add information about the return value? (this technically shows up in the function body)
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


def process_assign(node):
    s = "Assignment: "
    # handle possible target types
    target_type = type(node.targets[0])
    if target_type == ast.Name:
        s += f"{node.targets[0].id} -> "
    elif target_type == ast.Attribute:
        s += f"self.{node.targets[0].attr} -> "
    elif target_type == ast.Tuple:
        targets = []
        for target in node.targets[0].elts:
            if type(target) == ast.Name:
                targets.append(target.id)
            elif type(target) == ast.Attribute:
                targets.append(target.attr)
            else:
                targets.append("<unimplemented>")
        s += ", ".join(str(target) for target in targets)
        s += " -> "
    else:
        s += "<unimplemented> -> "
    # handle possible value types
    value_type = type(node.value)
    if value_type == ast.Name:
        s += f"{node.value.id} (variable)"
    elif value_type == ast.Constant:
        s += f"{node.value.value} {type(node.value.value)}"
    elif value_type == ast.Tuple:
        values = []
        for value in node.value.elts:
            if type(value) == ast.Name:
                values.append(f"{value.id} (variable)")
            elif type(value) == ast.Constant:
                values.append(f"{value.value} {type(value.value)}")
            else:
                values.append("<unimplemented>")
        s += ", ".join(str(value) for value in values)
    else:
        s += "<unimplemented>"
    return s


def process_constant(constant):
    value = constant.value
    s = f"{str(value)} {type(value)}"
    return s


print(unpack(tree))
