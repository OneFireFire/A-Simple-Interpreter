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

    ##########################################################
    # Lex analyzer                                           #
    ##########################################################

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

    ##########################################################
    # Syntax analyzer                                        #
    ##########################################################

    def eat(self, token_type):
        # eat like a pointer to token
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        current_token = self.current_token
        self.eat(INTEGER)
        return current_token.value

    def expr(self):
        self.current_token = self.get_next_token()
        
        self.result = self.term()
        while self.current_token.type in (PLUS, SUB):
            current_token=self.current_token
            
            if current_token.type == PLUS:
                self.eat(PLUS)
                self.result += self.term()
            elif current_token.type == SUB:
                self.eat(SUB)
                self.result -= self.term()

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
