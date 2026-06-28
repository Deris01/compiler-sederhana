from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self):
        self.declared_variables = set()

    def analyze(self, node):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.analyze(stmt)
                
        elif isinstance(node, VarDeclaration):
            self.analyze(node.value)
            self.declared_variables.add(node.identifier.name)
            
        elif isinstance(node, AssignmentStatement):
            if node.identifier.name not in self.declared_variables:
                raise NameError(f"Error Semantik: Variabel '{node.identifier.name}' dereng damel.")
            self.analyze(node.value)
            
        elif isinstance(node, NgendikaStatement):
            if node.expression.name not in self.declared_variables:
                raise NameError(f"Error Semantik: Variabel '{node.expression.name}' dereng damel.")
                
        elif isinstance(node, Identifier):
            if node.name not in self.declared_variables:
                raise NameError(f"Error Semantik: Variabel '{node.name}' dereng damel.")
                
        elif isinstance(node, BinOp) or isinstance(node, Condition):
            self.analyze(node.left)
            self.analyze(node.right)
            
        elif isinstance(node, IfStatement):
            self.analyze(node.condition)
            self.analyze(node.true_block)
            if node.false_block:
                self.analyze(node.false_block)
                
        elif isinstance(node, Block):
            for stmt in node.statements:
                self.analyze(stmt)