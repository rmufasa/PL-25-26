from utils.AST import Node
from SymbolTable import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symtab = SymbolTable()
        self.labels = set()

    def visit(self, node):
        if not isinstance(node, Node):
            return None

        method = getattr(self, f"visit_{node.type}", self.generic)
        return method(node)

    def generic(self, node):
        for child in node.args:
            if isinstance(child, Node):
                self.visit(child)
    
    def visit_program(self, node):
        self.collect_labels(node)

        for child in node.args:
            if isinstance(child, Node):
                self.visit(child)
    
    def collect_labels(self, node):
        if not isinstance(node, Node):
            return

        if isinstance(node, Node):
            if node.type == 'stmt':
                label = node.args[0]
                if isinstance(label, int):   
                    self.labels.add(label)

            if node.type == 'do':
                self.labels.add(node.args[0])
                self.labels.add(node.args[5])

            for child in node.args:
                self.collect_labels(child)
    
    # declaration handling
    def visit_decl(self, node):
        typ = node.args[0] # INTEGER, REAL, LOGICAL
        id_list_node = node.args[1]

        names = self.extract_ids(id_list_node)

        for name_node in names:
            if isinstance(name_node, Node) and name_node.type == "id_array":
                name = name_node.args[0]

                if name == "MOD":
                    raise Exception("MOD is a built-in function and cannot be declared")

                size = self.extract_size(name_node.args[1])
                size_type = self.visit(name_node.args[1]) # INT inside expr_list
                if size_type != 'INTEGER':
                    print(size_type)
                    raise Exception("Array size must be constant integer")  
                self.symtab.declare_array(name, typ, size)
            else:
                name = self.get_name(name_node)

                if name == "MOD":
                    raise Exception("MOD is a built-in function and cannot be declared")

                self.symtab.declare_var(name, typ)
    
    def extract_size(self, node): # extract array size
        if node.type == "int":
            return node.args[0]

        if node.type == "expr_list" or node.type == "expression" or node.type == "term" or node.type == "factor":
            return self.extract_size(node.args[0])

        raise Exception("Array size must be a constant integer expression")

    def extract_ids(self, node):
        names = []

        if node.type == 'id_list':
            first_id = node.args[0]
            more_ids = node.args[1]

            names.append(first_id)
            names.extend(self.extract_ids(more_ids))
        elif node.type == 'more_ids':
            next_id = node.args[0]
            more_ids = node.args[1]

            names.append(next_id)
            names.extend(self.extract_ids(more_ids))
        elif node.type == 'empty':
            return []

        return names

    def get_name(self, node):
        if isinstance(node, Node):
            if node.type == 'id':
                return node.args[0]
            elif node.type == 'id_array':
                return node.args[0]
        return node

    # assignment checking
    def visit_assign(self, node):
        var_node = node.args[0]
        expr_node = node.args[1]

        var_name = self.get_name(var_node)
        var_info = self.symtab.lookup(var_name)

        # array vs scalar
        if var_node.type == "id_array":
            if var_info["kind"] != "array":
                raise Exception(f"{var_name} is not an array")

        elif var_node.type == "id":
            if var_info["kind"] == "array":
                raise Exception(f"{var_name} is an array (missing index)")

        else:
            raise Exception("Invalid assignment target")

        # type check
        var_type = var_info["type"]
        expr_type = self.visit(expr_node)

        if var_type == 'REAL' and expr_type == 'INTEGER':
            return

        if var_type != expr_type:
            raise Exception(f"Type error: cannot assign {expr_type} to {var_type}")          

    # expression typing
    def visit_int(self, node):
        return 'INTEGER'

    def visit_float(self, node):
        return 'REAL'

    def visit_bool(self, node):
        return 'LOGICAL'

    def visit_string(self, node):
        return 'STRING'

    def visit_id(self, node):
        name = node.args[0]
        var = self.symtab.lookup(name)

        if var["kind"] == "array":
            raise Exception(f"{name} is an array (missing index)")

        return var["type"]

    def visit_id_array(self, node):
        name = node.args[0]

        # built-in MOD (special case)
        if name == "MOD":
            args = self.flatten_exprs(node.args[1])

            if len(args) != 2:
                raise Exception("MOD expects 2 arguments")

            left = self.visit(args[0])
            right = self.visit(args[1])

            if left not in ['INTEGER', 'REAL'] or right not in ['INTEGER', 'REAL']:
                raise Exception("MOD arguments must be numeric")

            return 'INTEGER'

        index_expr = node.args[1]
        var = self.symtab.lookup(name)

        if var["kind"] != "array":
            raise Exception(f"{name} is not an array")


        index_type = self.visit(index_expr)
        if index_type != "INTEGER":
            raise Exception("Array index must be INTEGER")

        return var["type"]
    
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

    def visit_plus(self, node):
        left = self.visit(node.args[0])
        right = self.visit(node.args[1])

        if left not in ['INTEGER', 'REAL'] or right not in ['INTEGER', 'REAL']:
            raise Exception("Type error in addition")

        if 'REAL' in (left, right):
            return 'REAL'
        return 'INTEGER'

    def visit_minus(self, node):
        left = self.visit(node.args[0])
        right = self.visit(node.args[1])

        if left not in ['INTEGER', 'REAL'] or right not in ['INTEGER', 'REAL']:
            raise Exception("Type error in subtraction")

        if 'REAL' in (left, right):
            return 'REAL'
        return 'INTEGER'

    def visit_mul(self, node):
        left = self.visit(node.args[0])
        right = self.visit(node.args[1])

        if left not in ['INTEGER', 'REAL'] or right not in ['INTEGER', 'REAL']:
            raise Exception("Type error in multiplication")

        if 'REAL' in (left, right):
            return 'REAL'
        return 'INTEGER'
    
    def visit_div(self, node):
        left = self.visit(node.args[0])
        right = self.visit(node.args[1])

        if left not in ['INTEGER', 'REAL'] or right not in ['INTEGER', 'REAL']:
            raise Exception("Type error in division")

        if 'REAL' in (left, right):
            return 'REAL'
        return 'INTEGER'

    def visit_uminus(self, node):
        t = self.visit(node.args[0])
        if t not in ['INTEGER', 'REAL']:
            raise Exception("Unary minus requires numeric type")
        return t
    
    def visit_and(self, node):
        left = self.visit(node.args[0])
        right = self.visit(node.args[1])

        if left != 'LOGICAL' or right != 'LOGICAL':
            raise Exception("AND requires LOGICAL")

        return 'LOGICAL'
    
    def visit_or(self, node):
        left = self.visit(node.args[0])
        right = self.visit(node.args[1])

        if left != 'LOGICAL' or right != 'LOGICAL':
            raise Exception("OR requires LOGICAL")

        return 'LOGICAL'

    def visit_not(self, node):
        right = self.visit(node.args[0])

        if right != 'LOGICAL':
            raise Exception("NOT requires LOGICAL")

        return 'LOGICAL'

    def visit_rel(self, node):
        left = self.visit(node.args[1])
        right = self.visit(node.args[2])

        if left in ['INTEGER', 'REAL'] and right in ['INTEGER', 'REAL']:
            return 'LOGICAL'

        if left != right:
            raise Exception("Type mismatch in comparison")

        return 'LOGICAL'

    # if condition check
    def visit_if(self, node):
        condition = node.args[0]
        then_block = node.args[1]
        else_block = node.args[2]

        cond_type = self.visit(condition)

        if cond_type != 'LOGICAL':
            raise Exception("IF condition must be LOGICAL")

        self.visit(then_block)
        if else_block.type != 'empty':
            self.visit(else_block)       

    # do loop label validation
    def visit_do(self, node):
        start_label = node.args[0]
        var_name = self.get_name(node.args[1])
        start_expr = node.args[2]
        end_expr = node.args[3]
        body = node.args[4]
        end_label = node.args[5]

        var_type = self.symtab.lookup(var_name)["type"]

        if var_type != 'INTEGER':
            raise Exception(f"DO variable '{var_name}' must be INTEGER")

        start_type = self.visit(start_expr)
        end_type = self.visit(end_expr)

        if start_type not in ['INTEGER', 'REAL'] or end_type not in ['INTEGER', 'REAL']:
            raise Exception("DO bounds must be numeric")
        
        if start_label != end_label:
            raise Exception(f"DO label mismatch: {start_label} != {end_label}")

        self.visit(body)

    def visit_print(self, node):
        self.visit(node.args[0])

    def visit_read(self, node):
        names = self.extract_ids(node.args[0])
        for name_node in names:
            name = self.get_name(name_node)
            self.symtab.lookup(name)

    def visit_goto(self, node):
        label = node.args[0]

        if label not in self.labels:
            raise Exception(f"GOTO to undefined label {label}")

    # intermediates
    def visit_expression(self, node):
        return self.visit(node.args[0])

    def visit_term(self, node):
        return self.visit(node.args[0])

    def visit_factor(self, node):
        return self.visit(node.args[0])

    def visit_expr_list(self, node):
        # Usually, for array sizes, there is only one expression in the list
        return self.visit(node.args[0])