from Parser import Parser

with open('exemplos/exemplo6.in', mode='r') as fh:
    contents = fh.read()

parser = Parser()
parser.Parse(contents)
