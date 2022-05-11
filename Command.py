def play(command, midi):
    midi.play()


def add_tone(command, midi):
    midi.one_more_tone()


def remove_tone(command, midi):
    midi.one_less_tone()


def add_many_tone(command, midi):
    midi.more_tone(command.args['number'])


def remove_many_tone(command, midi):
    midi.less_tone(command.args['number'])


def add_to_time(command, midi):
    midi.more_time()


def remove_to_time(command, midi):
    midi.less_time()


def pause(command, midi):
    midi.pause()


def two_notes(command, midi):
    midi.two_notes()


def add_time_two_notes(command, midi):
    midi.more_two_notes()


def remove_time_two_notes(command, midi):
    midi.less_two_notes()


def play_letter(command, midi):
    midi.letter(command.args['letter'])


def chord(command, midi):
    midi.chord()


def def_func(command, midi):
    midi.def_func(command)


def exec(command, midi):
    midi.save_note()
    for code in midi.function_list[command.args['name']][0]:
        code.run(midi)
    midi.load_note()


class Command:

    table = {
        "play": play,
        "add_tone": add_tone,
        "remove_tone": remove_tone,
        "add_many_tone": add_many_tone,
        "remove_many_tone": remove_many_tone,
        "add_to_time": add_to_time,
        "remove_to_time": remove_to_time,
        "pause": pause,
        "two_notes": two_notes,
        "add_time_two_notes": add_time_two_notes,
        "remove_time_two_notes": remove_time_two_notes,
        "chord": chord,
        "play_letter": play_letter,
        "def_func": def_func,
        "exec" : exec,
    }

    def __init__(self, nome, args):
        self.nome = nome
        self.args = args

    def __repr__(self):
        return f"{self.nome} => {self.args}"

    def run(self, midi):
        self.table[self.nome](self, midi)
