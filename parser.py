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
                s += f"\n    {line}"
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


def process(node):
    """
    process takes some ast object and determines which process function needs to be called. This function is
    present to simplify the structure of all the process functions since they will often need to call a variety of
    other process functions within themselves. Every process function should have an entry within this handler function.

    Parameters:
        node (ast.AST): The type of this AST object will be used to determine which process function needs to be called
    Returns:
        string (the output of the called process function)
    """
    node_type = type(node)
    if node_type == ast.Module:
        s = f"Unpacked representation:"
        for element in node.body:
            for line in process(element).splitlines():
                s += f"\n    {line}"
        return s
    elif node_type == ast.ClassDef:
        return process_class_def(node)
    elif node_type == ast.FunctionDef:
        return process_function_def(node)
    elif node_type == ast.For:
        return process_for(node)
    elif node_type == ast.If:
        return process_if(node)
    elif node_type == ast.Assign:
        return process_assign(node)
    elif node_type == ast.AugAssign:
        return process_aug_assign(node)
    elif node_type == ast.Expr:
        return process_expr(node)
    elif node_type == ast.Call:
        return process_call(node)
    elif node_type == ast.Return:
        return process_return(node)
    elif node_type == ast.Constant:
        return process_constant(node)
    elif node_type == ast.Name:
        return process_name(node)
    elif node_type == ast.Attribute:
        return process_attribute(node)
    elif node_type == ast.JoinedStr:
        return process_joined_string(node)
    elif node_type == ast.FormattedValue:
        return process_formatted_value(node)
    elif node_type == ast.List or node_type == ast.Tuple:
        return process_list(node)
    elif node_type == ast.BinOp:
        return process_bin_op(node)
    elif node_type == ast.BoolOp:
        return process_bool_op(node)
    elif node_type in [ast.Add, ast.Sub, ast.Mult, ast.Div]:
        return process_bin_op_token(node)
    elif node_type in [ast.And, ast.Or]:
        return process_bool_op_token(node)
    elif node_type == ast.Compare:
        return process_compare(node)
    else:
        return "<unimplemented>"


def process_class_def(node):
    # TODO add information about decorators
    s = f"Class definition: {node.name}"
    if len(node.bases) > 0:
        s += f"\nBase classes:"
        for base in node.bases:
            s += f"\n    {base}"
    for element in node.body:
        for line in process(element).splitlines():
            s += f"\n    {line}"
    return s


def process_function_def(node):
    # TODO add information about all argument types (not just args and vararg)
    # TODO add information about decorators
    # TODO add information about the return value? (this technically shows up in the function body)
    s = f"Function definition -> {node.name}"
    if len(node.args.args) > 0 or node.args.vararg is not None:
        s += f"\n    arguments:"
        for argument in node.args.args:
            s += f"\n        {argument.arg}"
        if node.args.vararg is not None:
            s += f"\n        *{node.args.vararg.arg}"
    for element in node.body:
        for line in process(element).splitlines():
            s += f"\n    {line}"
    return s


def process_for(node):
    s = f"For Loop: {process(node.target)} in {process(node.iter)}"
    for element in node.body:
        for line in process(element).splitlines():
            s += f"\n    {line}"
    return s


def process_if(node):
    # THIS IS RELATIVELY COMPLICATED, THERE ARE LOTS OF LOGIC POSSIBILITIES FOR AN IF STATEMENT AND THERE ARE
    # MULTIPLE NODES THAT CAN SHOW UP IN THE TEST ATTRIBUTE OF AN ast.If OBJECT
    print(type(node.test))
    print(process(node.test))
    s = f"If Statement: {process(node.test)}"
    for element in node.body:
        for line in process(element).splitlines():
            s += f"\n    {line}"
    return s


def process_assign(node):
    s = "Assignment: "
    s += process(node.targets[0])
    s += " -> "
    s += process(node.value)
    return s


def process_aug_assign(node):
    s = "Assignment: "
    s += process(node.target)
    s += f" {process(node.op)}= "
    s += process(node.value)
    return s


def process_expr(node):
    s = process_call(node.value)
    return s


def process_call(node):
    s = f"Expression: {process(node.func)}("
    s += ", ".join((process(arg)) for arg in node.args)
    s += ")"
    return s


def process_return(node):
    return f"Function Return: {process(node.value)}"


def process_constant(node):
    value = node.value
    if type(value) == str:
        if "\n" in value:
            value = value.replace("\n", "\\n")
        s = f"\"{value}\""
        return s
    # TODO decide if type should be included with constants or if this hurts readability
    # s = f"{str(value)} {type(value)}"
    s = str(value)
    return s


def process_name(node):
    return f"{node.id}"


def process_attribute(node):
    return f"{node.attr}"


def process_joined_string(node):
    s = ""
    for value in node.values:
        s += process(value)
    return s


def process_list(node):
    elements = []
    for element in node.elts:
        elements.append(process(element))
    s = "["
    s += ", ".join(str(element) for element in elements)
    s += "]"
    return s


def process_formatted_value(node):
    s = "{"
    s += process(node.value)
    s += "}"
    return s


def process_bin_op(node):
    s = process(node.left)
    s += " "
    s += process(node.op)
    s += " "
    s += process(node.right)
    return s


def process_bool_op(node):
    s = process(node.values[0])
    s += f" {process(node.op)}"
    s += f" {process(node.values[1])}"
    return s


def process_bool_op_token(node):
    node_type = type(node)
    if node_type == ast.And:
        return "and"
    elif node_type == ast.Or:
        return "or"
    else:
        return "<unimplemented>"


def process_bin_op_token(node):
    node_type = type(node)
    if node_type == ast.Add:
        return "+"
    elif node_type == ast.Sub:
        return "-"
    elif node_type == ast.Mult:
        return "*"
    elif node_type == ast.Div:
        return "/"
    else:
        return "<unimplemented>"


def process_compare(node):
    s = f"{process(node.left)} {process_comparators(node.ops[0])} {process(node.comparators[0])}"
    return s


def process_comparators(node):
    node_type = type(node)
    if node_type == ast.Eq:
        return "=="
    elif node_type == ast.NotEq:
        return "!="
    elif node_type == ast.Lt:
        return "<"
    elif node_type == ast.LtE:
        return "<="
    elif node_type == ast.Gt:
        return ">"
    elif node_type == ast.GtE:
        return ">="
    elif node_type == ast.Is:
        return "is"
    elif node_type == ast.IsNot:
        return "is not"
    elif node_type == ast.In:
        return "in"
    elif node_type == ast.NotIn:
        return "not in"
    else:
        return "<unimplemented>"


print(process(tree))
