from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code = []

    def current_indent(self):
        return "    " * self.indent_level

    def generate(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.code.append(self.generate_node(stmt))
            return "\n".join(self.code)

    def generate_node(self, node):
        if isinstance(node, VarDeclaration) or isinstance(node, AssignmentStatement):
            return f"{self.current_indent()}{node.identifier.name} = {self.generate_expression(node.value)}"
            
        elif isinstance(node, NgendikaStatement):
            return f"{self.current_indent()}print({node.expression.name})"
            
        elif isinstance(node, IfStatement):
            kondisi = self.generate_expression(node.condition)
            hasil = f"{self.current_indent()}if {kondisi}:\n"
            
            self.indent_level += 1
            hasil += self.generate_node(node.true_block)
            self.indent_level -= 1
            
            if node.false_block:
                hasil += f"\n{self.current_indent()}else:\n"
                self.indent_level += 1
                hasil += self.generate_node(node.false_block)
                self.indent_level -= 1
                
            return hasil
            
        elif isinstance(node, Block):
            statements_code = [self.generate_node(stmt) for stmt in node.statements]
            return "\n".join(statements_code) if statements_code else f"{self.current_indent()}pass"
            
        return ""

    def generate_expression(self, node):
        if isinstance(node, NumberLiteral):
            return str(node.value)
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, BinOp):
            op_map = {'TAMBAH': '+', 'KIRANG': '-', 'PING': '*', 'KAGEM': '//'}
            return f"({self.generate_expression(node.left)} {op_map[node.op.type]} {self.generate_expression(node.right)})"
        elif isinstance(node, Condition):
            op_map = {'LANGKUNG': '>', 'KIRANG': '<'}
            return f"({self.generate_expression(node.left)} {op_map[node.op.type]} {self.generate_expression(node.right)})"