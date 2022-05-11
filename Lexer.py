# Lexer.py
import ply.lex as lex
import sys


class Lexer:
    # literals = "^_{}<>~:="
    literals = "="
    t_ignore = " \t\r\n"
    tokens = ("COMMENT", "EXEC", "INT", "FUNCNAME", "NOTE", "PAUSE", "PLAY", "LFUNC", "RFUNC",
              "NOTEUP", "NOTEDOWN", "LBRACKET", "RBRACKET", "TIMEUP", "TIMEDOWN", "CHORD", "TIL")

    def t_COMMENT(self, t):
        r"\#.*\n"
        pass

    def t_EXEC(self, t):
        r"\\"
        return t

    def t_INT(self, t):
        r"[0-9]+"
        t.value = int(t.value)
        return t

    def t_FUNCNAME(self, t):
        r"[A-Z]+"
        return t

    def t_NOTE(self, t):
        r"[a-g]"
        return t

    def t_PAUSE(self, t):
        r"\*"
        return t

    def t_PLAY(self, t):
        r"\."
        return t

    def t_LFUNC(self, t):
        r"\["
        return t

    def t_RFUNC(self, t):
        r"\]"
        return t

    def t_NOTEUP(self, t):
        r"\^"
        return t

    def t_NOTEDOWN(self, t):
        r"_"
        return t

    def t_LBRACKET(self, t):
        r"{"
        return t

    def t_RBRACKET(self, t):
        r"}"
        return t

    def t_TIMEUP(self, t):
        r"<"
        return t

    def t_TIMEDOWN(self, t):
        r">"
        return t

    def t_TIL(self, t):
        r"~"
        return t

    def t_CHORD(self, t):
        r":"
        return t

    def t_error(self, t):
        print(f"Parser error. Unexpected char: {t.value[0]}", file=sys.stderr)
        exit(1)

    def __init__(self):
        self.lexer = None

    def Build(self, data, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.input(data)
