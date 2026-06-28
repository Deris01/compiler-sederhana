Program        ::= Statement*
Block          ::= "{" Statement* "}"
Statement      ::= VarDeclaration | Assignment | PrintStatement | IfStatement

# --- LOGIKA KONDISIONAL ---
IfStatement    ::= "bilih" "(" Condition ")" Block ( "kejawi" Block )?
Condition      ::= Expression ("langkung" | "kirang") Expression

# --- LOGIKA MATEMATIKA ---
Expression     ::= Term ( ("tambah" | "kirang") Term )*
Term           ::= Factor ( ("ping" | "kagem") Factor )*
Factor         ::= Number | Identifier | "(" Expression ")"