from utils.AST import Node

class CodeGenerator:
    def __init__(self, symtab):
        self.symtab = symtab # symbol table
        self.code = [] # instructions
        self.temp_counter = 0
        self.label_counter = 0

    def emit(self, instr):
        self.code.append(instr)

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def generate(self, node):
        self.visit(node)
        return self.code

    def visit(self, node):
        if not isinstance(node, Node):
            return

        method = getattr(self, f"visit_{node.type}", self.generic)
        return method(node)

    def generic(self, node):
        for child in node.args:
            self.visit(child)
    
    def visit_program(self, node):
        self.emit("START")
        for child in node.args:
            self.visit(child)
        self.emit("STOP")
    
    def visit_decl(self, node):
        names = self.flatten_ids(node.args[1])

        for name_node in names:
            if name_node.type == "id_array":
                name = name_node.args[0]
                size = self.symtab.lookup(name)["size"]
                addr = self.symtab.lookup(name)["addr"]

                self.emit(f"PUSHI {size}")
                self.emit("ALLOCN")
                self.emit(f"STOREG {addr}")

            else:
                name = name_node.args[0]
                addr = self.symtab.lookup(name)["addr"]
                self.emit("PUSHI 0")
                self.emit(f"STOREG {addr}")
    
    def visit_stmt(self, node):
        label = node.args[0]
        body = node.args[1]

        if not (isinstance(label, Node) and label.type == "empty"):
            self.emit(f"{label}:")

        self.visit(body)
    
    def visit_id(self, node):
        name = node.args[0]
        addr = self.symtab.lookup(name)["addr"]
        self.emit(f"PUSHG {addr}")
    
    def visit_id_array(self, node):
        name = node.args[0]
        index = node.args[1]
        
        if name == "MOD":
            args = self.flatten_exprs(index)

            self.visit(args[0])  # n
            self.visit(args[1])  # m
            self.emit("MOD")
        else:
            addr = self.symtab.lookup(name)["addr"]

            self.emit(f"PUSHG {addr}")   # heap address
            self.visit(index)            # index
            self.emit("PUSHI 1") # subtract 1 to get 0-based index
            self.emit("SUB")
            self.emit("PADD")
            self.emit("LOAD 0")

    def visit_int(self, node):
        self.emit(f"PUSHI {node.args[0]}")

    def visit_float(self, node):
        self.emit(f"PUSHF {node.args[0]}")

    def visit_string(self, node):
        self.emit(f'PUSHS "{node.args[0]}"')

    def visit_bool(self, node):
        val = 1 if node.args[0] == '.TRUE.' else 0
        self.emit(f"PUSHI {val}") 

    def visit_assign(self, node):
        var = node.args[0]
        expr = node.args[1]

        if var.type == "id":
            self.visit(expr)
            addr = self.symtab.lookup(var.args[0])["addr"]
            self.emit(f"STOREG {addr}")

        elif var.type == "id_array":
            name = var.args[0]
            index = var.args[1]

            addr = self.symtab.lookup(name)["addr"]

            self.emit(f"PUSHG {addr}")   # address FIRST
            self.visit(index)            # index
            self.emit("PUSHI 1") # subtract 1 to get 0-based index
            self.emit("SUB")
            self.emit("PADD")  # base + (i-1) 
            self.visit(expr)   # value

            self.emit("STORE 0")

    def visit_plus(self, node):
        self.visit(node.args[0])
        self.visit(node.args[1])
        self.emit("ADD")

    def visit_minus(self, node):
        self.visit(node.args[0])
        self.visit(node.args[1])
        self.emit("SUB")
    
    def visit_mul(self, node):
        self.visit(node.args[0])
        self.visit(node.args[1])
        self.emit("MUL")

    def visit_div(self, node):
        self.visit(node.args[0])
        self.visit(node.args[1])
        self.emit("DIV")
    
    def visit_print(self, node):
        exprs = self.flatten_exprs(node.args[0])

        for expr in exprs:
            self.visit(expr)

            if isinstance(expr, Node) and expr.type == "string":
                self.emit("WRITES")
            else:
                self.emit("WRITEI")

        self.emit("WRITELN")  # optional but nice
    
    def visit_read(self, node):
        ids = self.flatten_ids(node.args[0])

        for var in ids:
            if var.type == "id":
                name = var.args[0]
                entry = self.symtab.lookup(name)
                addr = entry["addr"]
                typ = entry["type"]

                self.emit("READ")

                if typ == "INTEGER":
                    self.emit("ATOI")

                elif typ == "REAL":
                    self.emit("ATOF")

                elif typ == "LOGICAL":
                        self.emit("ATOI")  
                
                self.emit(f"STOREG {addr}")
            elif var.type == "id_array":
                name = var.args[0]
                index = var.args[1]

                entry = self.symtab.lookup(name)
                addr = entry["addr"]
                typ = entry["type"]

                # compute address properly
                self.emit(f"PUSHG {addr}")
                self.visit(index)
                self.emit("PUSHI 1") # subtract 1 to get 0-based index
                self.emit("SUB")
                self.emit("PADD")  # base + (i-1)

                self.emit("READ")

                if typ == "INTEGER":
                    self.emit("ATOI")
                elif typ == "REAL":
                    self.emit("ATOF")

                self.emit("STORE 0")

            else:
                raise Exception(f"Unsupported READ type: {typ}")
    

    def flatten_ids(self, node):
        names = []

        if node.type == "id_list":
            names.append(node.args[0])
            names.extend(self.flatten_ids(node.args[1]))

        elif node.type == "more_ids":
            names.append(node.args[0])
            names.extend(self.flatten_ids(node.args[1]))

        elif node.type == "empty":
            return []

        return names
    
    def flatten_exprs(self, node):
        exprs = []

        if node.type == "expr_list":
            exprs.append(node.args[0])
            exprs.extend(self.flatten_exprs(node.args[1]))

        elif node.type == "more_exprs":
            exprs.append(node.args[0])
            exprs.extend(self.flatten_exprs(node.args[1]))

        elif node.type == "empty":
            return []

        return exprs

    def visit_and(self, node):
        self.visit(node.args[0])
        self.visit(node.args[1])
        self.emit("AND")

    def visit_or(self, node):
        self.visit(node.args[0])
        self.visit(node.args[1])
        self.emit("OR")

    def visit_not(self, node):
        self.visit(node.args[0])
        self.emit("NOT")

    def visit_rel(self, node):
        self.visit(node.args[1])
        self.visit(node.args[2])

        op = node.args[0]

        if op == ".EQ.":
            self.emit("EQUAL")
        elif op == ".NE.":
            self.emit("EQUAL")
            self.emit("NOT")
        elif op == ".LT.":
            self.emit("INF")
        elif op == ".LE.":
            self.emit("INFEQ")
        elif op == ".GT.":
            self.emit("SUP")
        elif op == ".GE.":
            self.emit("SUPEQ")
    
    def visit_if(self, node):
        cond = node.args[0]
        then_block = node.args[1]
        else_block = node.args[2]

        else_label = self.new_label()
        end_label = self.new_label()

        # condition
        self.visit(cond)
        self.emit(f"JZ {else_label}")

        # then
        self.visit(then_block)
        self.emit(f"JUMP {end_label}")

        # else
        self.emit(f"{else_label}:")
        if else_block.type != "empty":
            self.visit(else_block)

        # end
        self.emit(f"{end_label}:")
    
    def visit_do(self, node):
        start_label = self.new_label()
        end_label = self.new_label()

        var = node.args[1]
        start_expr = node.args[2]
        end_expr = node.args[3]
        body = node.args[4]

        # initialize variable
        self.visit(start_expr)
        name = var.args[0]
        addr = self.symtab.lookup(name)["addr"]
        self.emit(f"STOREG {addr}")

        # loop start
        self.emit(f"{start_label}:")

        # condition check (I <= end)
        name = var.args[0]
        addr = self.symtab.lookup(name)["addr"]
        self.emit(f"PUSHG {addr}")
        self.visit(end_expr)
        self.emit("INFEQ")            # I <= end
        self.emit(f"JZ {end_label}")

        # body
        self.visit(body)

        # increment I = I + 1
        name = var.args[0]
        addr = self.symtab.lookup(name)["addr"]
        self.emit(f"PUSHG {addr}")
        self.emit("PUSHI 1")
        self.emit("ADD")
        name = var.args[0]
        addr = self.symtab.lookup(name)["addr"]
        self.emit(f"STOREG {addr}")

        # jump back
        self.emit(f"JUMP {start_label}")

        # end
        self.emit(f"{end_label}:")
    
    def visit_goto(self, node):
        label = node.args[0]
        self.emit(f"JUMP {label}")