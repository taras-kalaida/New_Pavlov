from Lexer import Lexer
from Parser import make_tree
from Generator import Generator


def read_file(file):
    with open(f"{file}", "rb") as file:
        file = file.read().decode('utf-8').replace("\r", "")
    return file


def correct_file(file):
    file = file.replace("\r", "")
    return file


class Start:
    def __init__(self, file):
        self.file = read_file(file)
        self.file = correct_file(self.file)
        self.lexer = Lexer(self.file)
        self.lexer.tokens_print()
        make_tree(self.lexer.token_get())
        self.generator = Generator()
        self.result, self.data = self.generator.Generator(self.lexer.token_get())

    def get_result(self):
        return self.result

    def get_data(self):
        return self.data
