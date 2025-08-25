import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return result

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self):
        while self.current_char is not None:
            self.skip_whitespace()

            if self.current_char is None:
                break

            if self.current_char.isdigit():
                num = self.number()
                if self.current_char == '.':
                    self.advance()
                    num += '.'
                    num += self.number()
                    return Token('REAL', float(num))
                return Token('ENTERO', int(num))

            if self.current_char.isalpha():
                ident = self.identifier()
                if ident in ['if', 'while', 'return', 'else', 'int', 'float']:
                    return Token('TIPO', ident)  # Assuming 'tipo' maps to reserved words
                return Token('IDENTIFICADOR', ident)

            if self.current_char == '+':
                self.advance()
                return Token('opSuma', '+')
            if self.current_char == '-':
                self.advance()
                return Token('opSuma', '-')

            if self.current_char == '*':
                self.advance()
                return Token('opMul', '*')
            if self.current_char == '/':
                self.advance()
                return Token('opMul', '/')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('oplgualdad', '==')
                return Token('opAsignacion', '=')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('opRelac', '<=')
                return Token('opRelac', '<')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('opRelac', '>=')
                return Token('opRelac', '>')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('oplgualdad', '!=')
                return Token('opNot', '!')

            if self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    return Token('opAnd', '&&')
                else:
                    raise Exception("Invalid character: &")

            if self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    return Token('opOr', '||')
                else:
                    raise Exception("Invalid character: |")

            if self.current_char == '(':
                self.advance()
                return Token('parentesis', '(')
            if self.current_char == ')':
                self.advance()
                return Token('parentesis', ')')

            if self.current_char == '{':
                self.advance()
                return Token('Llave', '{')
            if self.current_char == '}':
                self.advance()
                return Token('Llave', '}')

            if self.current_char == ';':
                self.advance()
                return Token('Punto y coma', ';')

            raise Exception(f"Invalid character: {self.current_char}")

        return Token('$', None)  # End of input

# Example usage:
text = "int x = 5 + 10.5; if (x > 0) { return x; }"
lexer = Lexer(text)
token = lexer.get_next_token()
while token.type != '$':
    print(token)
    token = lexer.get_next_token()