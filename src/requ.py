from typing import *


class Equation:
    def __init__(self, eq: str):
        self.eq = eq
    
    def __str__(self) -> str:
        return str(self.eq)
    



# 3x^2+cosx+1 
class Tokenizer:
    SUPPORTED_FUNCTIONS = ('sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'exp', 'log', 'ln', 'sinh', 'cosh', 'tanh', 'abs', 'ceil',
                           'floor', 'mod', 'csch', 'sech', 'coth')

    @staticmethod
    def tokenize(eq: str, wrt: str) -> None:
        tokens = []
        for _ in eq:
            tokens.append({_: Tokenizer.__parse(_, wrt)})
        tokens = Tokenizer.__check_for_functions(tokens)
        print(tokens)
        tokens = Tokenizer.__pad_operations(tokens)
        print(tokens)
    
    @staticmethod
    def __parse(char: str, wrt: str) -> str:
        if char == wrt:
            return 'VARIABLE'
        elif char in ('+', '-', '/', '*', '^'):
            return f'OPERATOR {char}'
        elif char in ('(', ')', '[', ']'):
            return f'PAREN {char}'
        elif char in (str(_) for _ in range(10)):
            return 'CONSTANT'
        else:
            return 'CHARACTER'
        
    @staticmethod
    def __check_for_functions(tokens: List[Dict]) -> List[Dict]:
        new_tokens = []

        sequence = ''
        temp = []
        for j in range(len(tokens)):
            _ = tokens[j]
            key = list(_.keys())[0]
            value = list(_.values())[0]

            if value == 'CHARACTER' or value == 'VARIABLE':
                sequence += key
                temp.append(_)
                if sequence in Tokenizer.SUPPORTED_FUNCTIONS:
                    new_tokens.append({sequence: f'FUNCTION {sequence}'})
                    temp = []
                    sequence = ''
            else:
                if len(temp) > 0:
                    new_tokens.extend(temp)
                    temp = []
                sequence = ''
                new_tokens.append(_)
        
        return new_tokens

    @staticmethod
    def __pad_operations(tokens: List[Dict]) -> List[Dict]:
        new_tokens = []

        for j in range(0, len(tokens)-1, 2):
            _ = tokens[j]
            key = list(_.keys())[0]
            value = list(_.values())[0]

            _2 = tokens[j+1]
            key2 = list(_2.keys())[0]
            value2 = list(_2.values())[0]

            if (value == 'CONSTANT' and value2 == 'VARIABLE') or (value == 'VARIABLE' and value2 == 'CONSTANT'):
                new_tokens.extend([{key: value}, {'*': 'OPERATOR *'}, {key2: value2}])
            else:
                new_tokens.extend([{key: value}, {key2: value2}])
        
        return new_tokens
            
        
# todo make functions and order of operations

if __name__ == '__main__':
    eq = '3x^2+cosx+1+exp(x)'
    Tokenizer.tokenize(eq, 'x')