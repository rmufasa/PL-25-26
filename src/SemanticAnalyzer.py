from utils import Node
from SymbolTable import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symtab = SymbolTable()

    def visit(self, node):
        # handle raw values
        if not isinstance(node, Node):
            if isinstance(node, str):
                try: # try variable lookup first
                    return self.symtab.lookup(node)
                except Exception: # fallback to literal
                    return self.infer_literal_type(node)
            return self.infer_literal_type(node)

        method = getattr(self, f"visit_{node.type}", self.generic)
        return method(node)

    def generic(self, node):
        for child in node.args:
            if isinstance(child, Node):
                self.visit(child)
    
    def visit_program(self, node):
        for child in node.args:
            if isinstance(child, Node):
                self.visit(child)
    
    # declaration handling
    def visit_decl(self, node):
        typ = node.args[0]          # 'INTEGER', 'REAL', 'LOGICAL'
        id_list_node = node.args[1]

        names = self.extract_ids(id_list_node)

        for name in names:
            self.symtab.declare(name, typ)

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

    # assignment checking
    def visit_assign(self, node):
        var_name = node.args[0]
        expr_node = node.args[1]

        # check variable exists
        var_type = self.symtab.lookup(var_name)

        # evaluate expression type
        expr_type = self.visit(expr_node)

        if var_type == 'REAL' and expr_type == 'INTEGER':
            return

        # check compatibility
        if var_type != expr_type:
            raise Exception(f"Type error: cannot assign {expr_type} to {var_type}")            

    # expression typing
    def visit_INT(self, node):
        return 'INTEGER'

    def visit_FLOAT(self, node):
        return 'REAL'

    def visit_BOOL(self, node):
        return 'LOGICAL'

    def infer_literal_type(self, value):
        if isinstance(value, int):
            return 'INTEGER'
        elif isinstance(value, float):
            return 'REAL'
        elif isinstance(value, str):
            if value in ['.TRUE.', '.FALSE.']:
                return 'LOGICAL'
            return 'STRING'

    def visit_factor(self, node): # variables inside expressions
        value = node.args[0]

        return self.visit(value)

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
        self.visit(else_block)       

    # do loop label validation
    def visit_do(self, node):
        start_label = node.args[0]
        var_name = node.args[1]
        start_expr = node.args[2]
        end_expr = node.args[3]
        body = node.args[4]
        end_label = node.args[5]

        var_type = self.symtab.lookup(var_name)

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
        for name in names:
            self.symtab.lookup(name)

    