
class Node:
    def __init__(self, t, *args):
        self.type = t
        self.args = args

    def __str__(self):
        return self._pretty()

    def _pretty(self, level=0):
        indent = "  " * level
        s = f"{indent}{self.type}\n"
        for a in self.args:
            if isinstance(a, Node):
                s += a._pretty(level + 1)
            else:
                s += f"{indent}  {a}\n"
        return s