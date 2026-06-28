from ast_nodes import *

class Optimizer:
    def optimize(self, node):
        if isinstance(node, Program):
            return Program([self.optimize(stmt) for stmt in node.statements])
            
        elif isinstance(node, VarDeclaration):
            return VarDeclaration(node.identifier, self.optimize(node.value))
            
        elif isinstance(node, AssignmentStatement):
            return AssignmentStatement(node.identifier, self.optimize(node.value))
            
        elif isinstance(node, BinOp):
            left_opt = self.optimize(node.left)
            right_opt = self.optimize(node.right)
            
            # CONSTANT FOLDING: Jika kiri dan kanan sama-sama angka, langsung hitung
            if isinstance(left_opt, NumberLiteral) and isinstance(right_opt, NumberLiteral):
                if node.op.type == 'TAMBAH': return NumberLiteral(left_opt.value + right_opt.value)
                if node.op.type == 'KIRANG': return NumberLiteral(left_opt.value - right_opt.value)
                if node.op.type == 'PING': return NumberLiteral(left_opt.value * right_opt.value)
                if node.op.type == 'KAGEM': return NumberLiteral(left_opt.value // right_opt.value)
            
            # Jika bukan angka mati, kembalikan node aslinya
            return BinOp(left_opt, node.op, right_opt)
            
        elif isinstance(node, Condition):
            return Condition(self.optimize(node.left), node.op, self.optimize(node.right))
            
        elif isinstance(node, IfStatement):
            false_block_opt = self.optimize(node.false_block) if node.false_block else None
            return IfStatement(self.optimize(node.condition), self.optimize(node.true_block), false_block_opt)
            
        elif isinstance(node, Block):
            return Block([self.optimize(stmt) for stmt in node.statements])
            
        # Node lain (NumberLiteral, Identifier, NgendikaStatement) tidak bisa dioptimasi matematika
        return node