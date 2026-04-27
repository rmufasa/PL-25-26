class SymbolTable:
    def __init__(self):
        self.table = {}

    def declare(self, name, typ):
        if name in self.table:
            raise Exception(f"Variable '{name}' already declared")
        self.table[name] = typ

    def lookup(self, name):
        if name not in self.table:
            raise Exception(f"Variable '{name}' not declared")
        return self.table[name]