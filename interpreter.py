from typing import Any
from ast_nodes import *

class Interpreter:
    def __init__(self):
        self.environment = {} # Tempat menyimpan variabel di memori

    def evaluate(self, node: Any):
        # 1. EVALUASI STRUKTUR PROGRAM
        if isinstance(node, Program):
            for stmt in node.statements:
                self.evaluate(stmt)
                
        elif isinstance(node, VarDeclaration):
            # Jangan langsung ambil nilai. Evaluasi seluruh ekspresi matematika di kanan '='
            hasil_evaluasi = self.evaluate(node.value)
            self.environment[node.identifier.name] = hasil_evaluasi
            
        elif isinstance(node, NgendikaStatement):
            var_name = node.expression.name
            if var_name in self.environment:
                print(f"Output: {self.environment[var_name]}")
            else:
                raise NameError(f"Variabel '{var_name}' dereng damel (belum dibuat).")
            
        elif isinstance(node, AssignmentStatement):
            var_name = node.identifier.name
            
            # Validasi: Pastikan variabel sudah pernah di-damel (dideklarasikan)
            if var_name not in self.environment:
                raise NameError(f"Error Fatal: Variabel '{var_name}' dereng damel. Boten saged dipun ubah.")
            
            # Evaluasi ekspresi matematika baru dan timpa nilai di memori
            nilai_baru = self.evaluate(node.value)
            self.environment[var_name] = nilai_baru


        elif isinstance(node, BinOp):
            # Evaluasi sayap kiri dan kanan pohon secara rekursif
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            
            # Terjemahkan token bahasa daerah ke operasi Python sesungguhnya
            if node.op.type == 'TAMBAH':
                return left_val + right_val
            elif node.op.type == 'KIRANG':
                return left_val - right_val
            elif node.op.type == 'PING':
                return left_val * right_val
            elif node.op.type == 'KAGEM':
                # Gunakan // jika ingin pembagian bulat (integer division)
                return left_val / right_val 
                
        elif isinstance(node, NumberLiteral):
            return node.value # Kembalikan angka mentah
            
        elif isinstance(node, Identifier):
            # Jika ekspresi mengandung nama variabel (misal: hasil tambah 5)
            var_name = node.name
            if var_name in self.environment:
                return self.environment[var_name]
            else:
                raise NameError(f"Variabel '{var_name}' dereng damel.")
            
        elif isinstance(node, Block):
            for stmt in node.statements:
                self.evaluate(stmt)

        elif isinstance(node, Condition):
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            
            if node.op.type == 'LANGKUNG':
                return left_val > right_val
            elif node.op.type == 'KIRANG':
                return left_val < right_val
            
        elif isinstance(node, IfStatement):
            kondisi_terpenuhi = self.evaluate(node.condition)
            if kondisi_terpenuhi:
                self.evaluate(node.true_block)
            elif node.false_block:
                self.evaluate(node.false_block)
                