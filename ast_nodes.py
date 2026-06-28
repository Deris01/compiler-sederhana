class Program:
    def __init__(self, statements):
        self.statements = statements

class VarDeclaration:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

class NgendikaStatement:  # Representasi AST untuk 'print'
    def __init__(self, expression):
        self.expression = expression

class Identifier:
    def __init__(self, name):
        self.name = name

class NumberLiteral:
    def __init__(self, value):
        self.value = value

class BinOp:
    def __init__(self, left, op, right):
        self.left = left    # Bisa berupa NumberLiteral, atau BinOp lainnya
        self.op = op        # Token operator (misal: Token(TAMBAH, 'tambah'))
        self.right = right  # Bisa berupa NumberLiteral, atau BinOp lainnya

class AssignmentStatement:
    def __init__(self, identifier, value_expression):
        self.identifier = identifier
        self.value = value_expression

class Block:
    def __init__(self, statements):
        self.statements = statements # Berisi list dari statement

class Condition:
    def __init__(self, left, op, right):
        self.left = left    # Sisi kiri (misal: umur)
        self.op = op        # Token operator (misal: Token(LANGKUNG, 'langkung'))
        self.right = right  # Sisi kanan (misal: 30)

class IfStatement:
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition   # Objek dari class Condition
        self.true_block = true_block # Objek dari class Block (dieksekusi jika benar)
        self.false_block = false_block # Objek dari class Block (opsional, dieksekusi jika salah)