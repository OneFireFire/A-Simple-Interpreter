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


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.result = 0
        self.op=PLUS

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

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()
        while self.current_token.type != 'EOF':
            current_token=self.current_token
            print(self.current_token)
            
            if current_token.type == INTEGER:
                if self.op == 'PLUS':
                    self.result += self.current_token.value
                if self.op == 'SUB':
                    self.result -= self.current_token.value
                if self.op == 'MUL':
                    self.result *= self.current_token.value
                if self.op == 'DIV':
                    self.result /= self.current_token.value
                self.eat(INTEGER)  
            elif current_token.type == PLUS:
                self.op=PLUS
                self.eat(PLUS)
            elif current_token.type == SUB:
                self.op=SUB
                self.eat(SUB)
            elif current_token.type == MUL:
                self.op=MUL
                self.eat(MUL)
            elif current_token.type == DIV:
                self.op=DIV
                self.eat(DIV)

                       
        return self.result


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
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()