INTEGER, PLUS, SUB, MUL,DIV, EOF = 'INTEGER', 'PLUS', 'SUB', 'MUL','DIV','EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        
    def error(self):
        raise Exception('Error parsing input')

    def skip_whiteSpace(self):
        self.pos += 1
        
    def get_integer(self):
        result=''
        while self.pos <= len(self.text) - 1 and self.text[self.pos].isdigit():
            result += self.text[self.pos]
            self.pos += 1
            
        return int(result)
              
    def get_next_token(self):        
        # skip whitespace characters
        while self.pos <= len(self.text) - 1:
            current_char = self.text[self.pos]
            
            if current_char == ' ':
                self.skip_whiteSpace()
                continue

            if current_char.isdigit():
                return Token(INTEGER,self.get_integer())
                
            if current_char == '+':
                self.pos += 1
                return Token(PLUS, '+')
            
            if current_char == '-':
                self.pos += 1
                return Token(SUB,'-')
            
            if current_char == '*':
                self.pos += 1
                return Token(MUL,'*')
            
            if current_char == '/':
                self.pos += 1
                return Token(DIV,'/')
            
            self.error()
            
        return Token(EOF, None)
        
    
class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        
    def error(self):
        raise Exception('Invaild syntax')


    def eat(self, token_type):
        # eat like a pointer to token
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def exprA(self):
        result = self.factor()
        while self.current_token.type in (MUL, DIV):
            current_token=self.current_token
            
            if current_token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif current_token.type == DIV:
                self.eat(DIV)
                result /= self.factor()

        return result
    
    def expr(self):
        result=self.exprA()
        while self.current_token.type in (PLUS, SUB):
            current_token=self.current_token
            
            if current_token.type == PLUS:
                self.eat(PLUS)
                result += self.exprA()
            elif current_token.type == SUB:
                self.eat(SUB)
                result -= self.exprA()

        return result


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

   
if __name__ == '__main__':
    main()
