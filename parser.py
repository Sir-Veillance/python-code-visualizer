import ast


with open("sample_code.py") as f:
    file_contents = f.read()
test_object = ast.parse(file_contents)

for node in test_object.body:
    if type(node) == ast.FunctionDef:
        print(f"Found a function definition for function named: {node.name}")
        print("  Function arguments:")
        for argument in node.args.args:
            print(f"    {argument.arg}")

