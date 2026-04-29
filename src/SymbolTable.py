class SymbolTable:
    def __init__(self):
        self.table = {}
        self.counter = 0 # next free memory slot, abstracted memory / slots

    def declare_var(self, name, typ):
        if name in self.table:
            raise Exception(f"Variable '{name}' already declared")

        self.table[name] = {
            "kind": "var",
            "type": typ,
            "addr": self.counter
        }
        self.counter += 1
    
    def declare_array(self, name, typ, size):
        if name in self.table:
            raise Exception(f"Variable '{name}' already declared")

        self.table[name] = {
            "kind": "array",
            "type": typ,
            "addr": self.counter,
            "size": size
        }
        self.counter += size

    def lookup(self, name):
        if name not in self.table:
            raise Exception(f"Variable '{name}' not declared")
        return self.table[name]