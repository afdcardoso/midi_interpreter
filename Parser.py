# Parser.py
import sys
import ply.yacc as yacc
from Lexer import Lexer
from Command import Command
from MIDI import MIDI


class Parser:
    tokens = Lexer.tokens

    def __init__(self):
        self.parser = None
        self.lexer = None
        self.funcs = {}
        self.midi = MIDI()
        self.last_midi = None


    def Parse(self, data, **kwargs):
        self.lexer = Lexer()
        self.lexer.Build(data, **kwargs)
        self.parser = yacc.yacc(module=self, **kwargs)
        program = self.parser.parse(lexer=self.lexer.lexer)

        self.midi.start_midi()
        self.execute(program)
        self.midi.end_midi()

    def execute(self, program):
        for command in program:
            command.run(self.midi)

    def p_error(self, t):
        print("Syntax error", file=sys.stderr)
        next_token = self.parser.token()
        if next_token:
            print(f"Got unexpected token {next_token}", file=sys.stderr)
        exit(1)

    def p_program0(self, p):
        """  program  :   command  """
        p[0] = [p[1]]

    def p_program1(self, p):
        """  program  :  program command  """
        lst = p[1]
        lst.append(p[2])
        p[0] = lst

    def p_command_def_func(self, p):
        """  command  : FUNCNAME  '='  LFUNC   program   RFUNC   """
        p[0] = Command("def_func", {"name": p[1], "code": p[4]})

    def p_duration0(self, p):
        """  duration  :  TIMEUP """
        p[0] = Command("remove_to_time", None)

    def p_duration1(self, p):
        """  duration  :  TIMEDOWN """
        p[0] = Command("add_to_time", None)

    def p_command0(self, p):
        """   command : duration   """
        p[0] = p[1]

    def p_command1(self, p):
        """   command : PAUSE   """
        p[0] = Command("pause", None)

    def p_command2(self, p):
        """  command  :  COMMENT """
        pass

    def p_play0(self, p):
        """  play  :  PLAY """
        p[0] = Command("play", None)

    def p_play1(self, p):
        """ play : PLAY TIL PLAY"""
        p[0] = Command("two_notes", None)

    def p_play2(self, p):
        """  play  :  PLAY TIL TIMEUP PLAY """
        p[0] = Command("add_time_two_notes", None)

    def p_play3(self, p):
        """  play  :  PLAY TIL TIMEDOWN PLAY """
        p[0] = Command("remove_time_two_notes", None)

    def p_play4(self, p):
        """  play  :  CHORD """
        p[0] = Command("chord", None)

    def p_play_exec(self, p):
        """  play  :  EXEC FUNCNAME """
        p[0] = Command("exec", {'name': p[2]})

    def p_command_play(self, p):
        """  command  :  play """
        p[0] = p[1]

    def p_tone0(self, p):
        """  tone  :  NOTEUP """
        p[0] = Command("add_tone", None)

    def p_tone1(self, p):
        """  tone  :  NOTEDOWN """
        p[0] = Command("remove_tone", None)

    def p_tone2(self, p):
        """  tone  :  NOTEUP LBRACKET INT RBRACKET """
        p[0] = Command("add_many_tone", {"number": p[3]})

    def p_tone3(self, p):
        """  tone  :  NOTEDOWN LBRACKET INT RBRACKET """
        p[0] = Command("remove_many_tone", {"number": p[3]})

    def p_command_tone(self, p):
        """  command  :  tone """
        p[0] = p[1]

    def p_command_letter(self, p):
        """  command  :  NOTE """
        p[0] = Command("play_letter", {"letter": p[1]})
