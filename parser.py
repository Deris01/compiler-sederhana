from typing import List
from lexer import Token
from ast_nodes import *

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type):
        token = self.current_token()
        if token and token.type == expected_type:
            self.pos += 1
            return token
        raise SyntaxError(f"Sintaks error: Diharapkan {expected_type}, tapi mendapat {token.type if token else 'EOF'}")

    def parse(self):
        statements = []
        while self.current_token() is not None:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token = self.current_token()
        if token.type == 'DAMEL':
            return self.parse_var_declaration()
        elif token.type == 'NGENDIKA':
            return self.parse_ngendika_statement()
        elif token.type == 'ID':
            return self.parse_assignment()
        elif token.type == 'BILIH':
            return self.parse_if_statement()
        else:
            raise SyntaxError(f"Perintah tidak valid: {token.value}")
    
    def parse_assignment(self):
        id_token = self.consume('ID')
        self.consume('ASSIGN')
        expr_node = self.parse_expression() 
        
        self.consume('SEMI')
        return AssignmentStatement(Identifier(id_token.value), expr_node)

    def parse_var_declaration(self):
        self.consume('DAMEL')
        id_token = self.consume('ID')
        self.consume('ASSIGN')
        expr_node = self.parse_expression() 
        
        self.consume('SEMI')
        return VarDeclaration(Identifier(id_token.value), expr_node)

    def parse_ngendika_statement(self):
        self.consume('NGENDIKA')
        id_token = self.consume('ID')
        self.consume('SEMI')
        return NgendikaStatement(Identifier(id_token.value))
    
    def parse_expression(self):
        node = self.parse_term() # Cek perkalian/pembagian dulu
        
        while self.current_token() and self.current_token().type in ('TAMBAH', 'KIRANG'):
            op_token = self.consume(self.current_token().type)
            right = self.parse_term()
            node = BinOp(node, op_token, right) # Rangkai jadi Tree
            
        return node
        
    def parse_factor(self):
        token = self.current_token()
        
        if token.type == 'NUMBER':
            self.consume('NUMBER')
            return NumberLiteral(int(token.value))
            
        elif token.type == 'ID':
            self.consume('ID')
            return Identifier(token.value)
            
        elif token.type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression() # Evaluasi ulang yang ada di dalam kurung
            self.consume('RPAREN')
            return expr
            
        else:
            raise SyntaxError(f"Sintaks error: Diharapkan angka atau variabel, mendapat {token.value}")
        
    def parse_term(self):
        node = self.parse_factor() # Cek angka/kurung dulu
        
        while self.current_token() and self.current_token().type in ('PING', 'KAGEM'):
            op_token = self.consume(self.current_token().type)
            right = self.parse_factor()
            node = BinOp(node, op_token, right)
            
        return node
    
    def parse_block(self):
        self.consume('LBRACE')
        statements = []
        while self.current_token() and self.current_token().type != 'RBRACE':
            statements.append(self.parse_statement())
        self.consume('RBRACE')
        return Block(statements)
    
    def parse_condition(self):
        left = self.parse_expression() # Ambil nilai kiri
        
        token = self.current_token()
        if token and token.type in ('LANGKUNG', 'KIRANG'):
            op_token = self.consume(token.type)
        else:
            raise SyntaxError("Diharapkan operator 'langkung' atau 'kirang' di dalam kondisi.")
            
        right = self.parse_expression() # Ambil nilai kanan
        
        return Condition(left, op_token, right)
    
    def parse_if_statement(self):
        self.consume('BILIH')
        self.consume('LPAREN')
        condition = self.parse_condition()
        self.consume('RPAREN')
        
        true_block = self.parse_block()
        false_block = None
        
        # Cek apakah ada 'kejawi' (ELSE). Jika tidak ada, biarkan false_block = None
        if self.current_token() and self.current_token().type == 'KEJAWI':
            self.consume('KEJAWI')
            false_block = self.parse_block()
            
        return IfStatement(condition, true_block, false_block)