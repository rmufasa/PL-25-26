import sys
import os

sys.path.append("../src")

from f77_parser import parser
from f77_lexer import build_lexer
from SemanticAnalyzer import SemanticAnalyzer
from CodeGenerator import CodeGenerator


def main():
    if len(sys.argv) != 2:
        print("Usage: python run_tests.py <program.f>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)

    # read source
    with open(input_file, "r") as f:
        source = f.read()

    # parse
    lexer = build_lexer()
    ast = parser.parse(source, lexer=lexer)

    # semantic analysis
    sem = SemanticAnalyzer()
    sem.visit(ast)

    # code generation
    codegen = CodeGenerator(sem.symtab)
    vm_code = codegen.generate(ast)

    # output path
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join("vm", base_name + ".vm")

    # ensure vm folder exists
    os.makedirs("vm", exist_ok=True)

    # write VM code
    with open(output_file, "w") as f:
        f.write("\n".join(vm_code))

    print(f"VM code generated: {output_file}")


if __name__ == "__main__":
    main()