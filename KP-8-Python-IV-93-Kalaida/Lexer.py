from rply import *
import sys


def form_dict(values, keys):
    dictionary = dict()
    if len(values) == len(keys):
        for i in range(len(values)):
            dictionary.update({keys[i]: values[i]})
    return dictionary


class Lexer:
    __names = ["number", "incrementing", "return", "function", "if", "cycle", "else", "function_name", "variable",
               "open parentheses", "close parentheses", "coma", "colon", "==", "=", ">", "!=",
               '-', "+", "*"]
    __values = [r'\d+', r'\+', r'return', r'def', r'if', r'while', r'else', r'func\_\w+', r'\w+', r'\(', r'\)', r'\,',
                r'\:', "\==", r'\=', r'\>', r'\!=', r'\-', r'\+', r"\*", ]
    mass = []

    def __init__(self, string):
        self.lg = LexerGenerator()
        self.lg.ignore(r'\s+')
        self.dictionary = form_dict(self.__values, self.__names)
        self.form_chunks(self.dictionary)
        self.build = self.lg.build()
        self.tokens = self.form_tokens(string)

    def form_chunks(self, dictionary):

        self.lg.add("string", "'\w+'")
        self.lg.add("negative", "-\d+")
        self.lg.add("/", "\/")
        self.lg.add("*", "\*")
        for i, j in dictionary.items():
            self.lg.add(f"{i}", rf'{j}')

    def form_tokens(self, string):
        mass = []
        string = string.split("\n")
        count = 0
        for i in range(len(string)):
            mass.append([])

            for j in self.build.lex(string[i]):
                mass[i].append(j)
            count += 1

        mass = [i for i in mass if i != []]
        return mass

    def tokens_print(self):
        for i in self.token_get():
            for j in i:
                print(f"{j.name} : {j.value}")

    def token_get(self):
        return self.tokens
