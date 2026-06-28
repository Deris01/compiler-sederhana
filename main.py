import sys
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from generator import CodeGenerator
from ast_nodes import *

def cetak_pohon_ast(node, indent=""):
    if isinstance(node, Program):
        print(f"{indent}└── Program")
        for stmt in node.statements:
            cetak_pohon_ast(stmt, indent + "    ")
            
    elif isinstance(node, VarDeclaration):
        print(f"{indent}├── VarDeclaration (damel)")
        print(f"{indent}│   ├── ID: {node.identifier.name}")
        print(f"{indent}│   └── Value:")
        cetak_pohon_ast(node.value, indent + "│       ")
        
    elif isinstance(node, AssignmentStatement):
        print(f"{indent}├── AssignmentStatement (=)")
        print(f"{indent}│   ├── ID: {node.identifier.name}")
        print(f"{indent}│   └── Value:")
        cetak_pohon_ast(node.value, indent + "│       ")
        
    elif isinstance(node, NgendikaStatement):
        print(f"{indent}├── NgendikaStatement (ngendika)")
        print(f"{indent}│   └── Expression:")
        cetak_pohon_ast(node.expression, indent + "    └── ")
        
    elif isinstance(node, BinOp):
        print(f"{indent}├── BinOp ({node.op.value})")
        print(f"{indent}│   ├── Kiri:")
        cetak_pohon_ast(node.left, indent + "│   │   ")
        print(f"{indent}│   └── Kanan:")
        cetak_pohon_ast(node.right, indent + "│       ")
        
    elif isinstance(node, Condition):
        print(f"{indent}├── Condition ({node.op.value})")
        print(f"{indent}│   ├── Kiri:")
        cetak_pohon_ast(node.left, indent + "│   │   ")
        print(f"{indent}│   └── Kanan:")
        cetak_pohon_ast(node.right, indent + "│       ")
        
    elif isinstance(node, Block):
        print(f"{indent}├── Block {{ }}")
        for stmt in node.statements:
            cetak_pohon_ast(stmt, indent + "│   ")
            
    elif isinstance(node, IfStatement):
        print(f"{indent}├── IfStatement (bilih)")
        print(f"{indent}│   ├── Kondisi:")
        cetak_pohon_ast(node.condition, indent + "│   │   ")
        print(f"{indent}│   ├── Blok Benar:")
        cetak_pohon_ast(node.true_block, indent + "│   │   ")
        if node.false_block:
            print(f"{indent}│   └── Blok Salah (kejawi):")
            cetak_pohon_ast(node.false_block, indent + "│       ")
            
    elif isinstance(node, NumberLiteral):
        print(f"{indent}└── Number: {node.value}")
        
    elif isinstance(node, Identifier):
        print(f"{indent}└── Identifier: {node.name}")

if __name__ == "__main__":
    # Validasi Argumen
    if len(sys.argv) < 2:
        print("Error: Argumen file tidak ditemukan.")
        print("Cara penggunaan: python main.py <nama_file.jwh>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Membaca File
    try:
        with open(file_path, 'r') as file:
            kode_sumber = file.read()
    except FileNotFoundError:
        print(f"Error Fatal: File '{file_path}' mboten wonten (tidak ditemukan).")
        sys.exit(1)

    print(f"--- Kompilasi File: {file_path} ---\n")

    # 1. Fase Lexing
    print("1. Melakukan Lexing (Tokenisasi)...")
    lexer = Lexer()
    tokens = lexer.tokenize(kode_sumber)
    print(tokens)

    # 2. Fase Parsing (Membangun AST)
    print("\n2. Melakukan Parsing (Membangun AST)...")
    parser = Parser(tokens)
    ast_mentah = parser.parse()
    
    print("\n=== TAMPILAN POHON SINTAKS (AST) ===")
    cetak_pohon_ast(ast_mentah)
    print("====================================\n")

    # 3. Fase Semantik Analisis (Syarat Rubrik 10%)
    print("3. Melakukan Semantik Analisis...")
    semantic = SemanticAnalyzer()
    semantic.analyze(ast_mentah)
    print("[OK] Semantik Analisis lolos. Tidak ada variabel liar.\n")

    # 4. Fase Optimasi Kode (Syarat Rubrik 10%)
    print("4. Melakukan Optimasi Kode (Constant Folding)...")
    optimizer = Optimizer()
    ast_optimal = optimizer.optimize(ast_mentah)
    print("[OK] Operasi matematika statis berhasil dilipat.")
    print("=== POHON AST SETELAH DIOPTIMASI ===")
    cetak_pohon_ast(ast_optimal)
    print("====================================\n")

    # 5. Fase Code Generation (Syarat Rubrik 10%)
    print("5. Menghasilkan Python Code (Code Generator)...")
    generator = CodeGenerator()
    python_code = generator.generate(ast_optimal)
    print("=== KODE PYTHON HASIL TERJEMAHAN ===")
    print(python_code)
    print("====================================\n")
    
    # 6. Simpan Hasil Transpile
    output_file = "output.py"
    with open(output_file, 'w') as out_file:
        out_file.write(python_code)
        
    print(f"[SUKSES] Program berhasil dikompilasi ke '{output_file}'.")