import re
from typing import List, Any 

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    # Definisi Regex untuk bahasa Jawa Halus
    RULES = [
        ('DAMEL', r'\bdamel\b'),          # Deklarasi
        ('NGENDIKA', r'\bngendika\b'),    # Print
        ('BILIH', r'\bbilih\b'),          # IF
        ('KEJAWI', r'\bkejawi\b'),        # ELSE
        ('TAMBAH', r'\btambah\b'),        # Plus
        ('KIRANG', r'\bkirang\b'),        # Minus / Kurang Dari
        ('LANGKUNG', r'\blangkung\b'),    # Lebih Dari
        ('PING', r'\bping\b'),            # Kali
        ('KAGEM', r'\bkagem\b'),          # Bagi
        ('NUMBER', r'\d+'),               # Angka
        ('ID', r'[a-zA-Z_]\w*'),          # Variabel
        ('ASSIGN', r'='),                 # =
        ('LPAREN', r'\('),                # (
        ('RPAREN', r'\)'),                # )
        ('LBRACE', r'\{'),                # {
        ('RBRACE', r'\}'),                # }
        ('SEMI', r';'),                   # ;
        ('WHITESPACE', r'[ \t\n]+'),      # Spasi (buang)
        ('MISMATCH', r'.')                # HARUS DI BAWAH!
    ]

    def tokenize(self, code: str) -> List[Token]:
        tokens = []
        pos = 0
        while pos < len(code):
            match = None
            for token_type, regex in self.RULES:
                pattern = re.compile(regex)
                match = pattern.match(code, pos)
                if match:
                    val = match.group(0)
                    if token_type != 'WHITESPACE':
                        tokens.append(Token(token_type, val))
                    pos = match.end()
                    break
            if not match or token_type == 'MISMATCH':
                raise SyntaxError(f"Karakter tidak dikenal di posisi {pos}: {code[pos]}")
        return tokens