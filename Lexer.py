import re, collections

class Lexer(object):

    WHITESPACE = r'(?P<WHITESPACE>\s+)'
    COMMENT = r'(?P<COMMENT>{[^}]*})'
    READ = r'(?P<READ>\bread\b)'
    WRITE = r'(?P<WRITE>\bwrite\b)'
    IF = r'(?P<IF>\bif\b)'
    THEN = r'(?P<THEN>\bthen\b)'
    ELSE = r'(?P<ELSE>\belse\b)'
    END = r'(?P<END>\bend\b)'
    REPEAT = r'(?P<REPEAT>\brepeat\b)'
    UNTIL = r'(?P<UNTIL>\buntil\b)'
    PLUS = r'(?P<PLUS>\+)'
    MINUS = r'(?P<MINUS>\-)'
    MULTIPLICATION = r'(?P<MULTIPLICATION>\*)'
    DIVISION = r'(?P<DIVISION>\/)'
    GREATER = r'(?P<GREATER>\>)'
    SMALLER = r'(?P<SMALLER>\<)'
    ASSIGN = r'(?P<ASSIGN>:=)'
    IDENTIFIER = r'(?P<IDENTIFIER>[a-z]+)'
    NUMBER = r'(?P<NUMBER>\d+)'
    SEMICOLON = r'(?P<SEMICOLON>;)'
    LEFT_PAREN = r'(?P<OPENBRACKET>\()'
    RIGHT_PAREN = r'(?P<CLOSEBRACKET>\))'
    EQUAL = r'(?P<EQUAL>=)'

    regex = re.compile('|'.join([
        WHITESPACE,
        LEFT_PAREN,
        RIGHT_PAREN,
        COMMENT,
        READ,
        WRITE,
        IF,
        THEN,
        ELSE,
        END,
        REPEAT,
        UNTIL,
        PLUS,
        MINUS,
        MULTIPLICATION,
        DIVISION,
        GREATER,
        SMALLER,
        ASSIGN,
        IDENTIFIER,
        NUMBER,
        SEMICOLON,
        EQUAL
        ]))

    def __init__ (self, TINY):
        def generate_tokens(text):
            Token = collections.namedtuple('Token', ['type','value'])
            scanner = Lexer.regex.finditer(text)
            last_end = 0
            for m in scanner:
                start = m.start()
                end = m.end()
                if start != last_end:
                    # skipped over text to find the next token implies that there was unrecognizable text or an "error token"
                    text = text[last_end:start]
                    # print(text)
                    token = Token('ERROR', text)
                    yield token
                last_end = end
                token = Token(m.lastgroup, m.group())
                # print(token)
                if token.type != 'WHITESPACE':
                    # if token.type == "READ" or token.type == "WRITE" or token.type == "IF" or token.type == "THEN" or token.type == "ELSE" or token.type == "END" or token.type == "REPEAT" or token.type == "UNTIL":
                    #     token = Token('Reserved Word', token.value)
                    # elif token.type == "OPERATOR":
                    #     token = Token('Special Symbol', token.value)
                    yield token
            yield Token('EOF', '<end-of-file>')



        self._token_generator = generate_tokens(TINY)

    def next_token(self):
        # if you call this past the "EOF" token you will get a StopIteration exception
        return self._token_generator.__next__()
