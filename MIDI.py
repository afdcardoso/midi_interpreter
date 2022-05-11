from mxm.midifile import MidiOutFile


class MIDI:

    def __init__(self):
        self.midi = MidiOutFile(open('file−generated.mid', 'wb'))
        self.midi.header(format=1, nTracks=1, division=32)
        self.this_note = 60  # 60 is based note
        self.this_time = 16  # 16 is based time
        self.last_note = 0
        self.last_time = 0
        self.letter_index = 5  # 0-10 being 5 the center
        self.function_list = {}

    def next_note(self, num):
        result = [(num % 12) + self.letter_index * 12,
                  (num % 12) + (self.letter_index - 1) * 12,
                  (num % 12) + (self.letter_index + 1) * 12]

        valor = min(result, key=lambda x: abs(x - self.this_note))

        if valor > 127 or valor < 0:
            valor = self.this_note

        if valor == result[1]:
            if self.letter_index != 0:
                self.letter_index = self.letter_index - 1

        elif valor == result[2]:
            if self.letter_index != 10:
                self.letter_index = self.letter_index + 1

        self.this_note = valor
        self.play()

    def start_midi(self):
        self.midi.start_of_track()

    def end_midi(self):
        self.midi.end_of_track()

    def play(self):
        self.midi.update_time(self.this_time)
        self.midi.note_on(channel=0, note=self.this_note)
        self.midi.update_time(self.this_time)
        self.midi.note_off(channel=0, note=self.this_note)

    def one_more_tone(self):
        self.this_note += 1

    def one_less_tone(self):
        self.this_note -= 1

    def more_tone(self, n):
        self.this_note += n

    def less_tone(self, n):
        self.this_note -= n

    def more_time(self):
        self.this_time = self.this_time * 2

    def less_time(self):
        self.this_time = int(self.this_time / 2)

    def pause(self):
        self.midi.update_time(self.this_time)
        self.midi.note_on(channel=0, note=0)
        self.midi.update_time(0)
        self.midi.note_off(channel=0, note=0)

    def two_notes(self):
        self.midi.note_on(channel=0, note=self.this_note)
        self.midi.update_time(self.this_time)
        self.midi.note_on(channel=0, note=self.this_note)
        self.midi.update_time(self.this_time)
        self.midi.note_off(channel=0, note=self.this_note)
        self.midi.update_time(0)
        self.midi.note_off(channel=0, note=self.this_note)

    # dunno se self.more_time(self) funciona
    def more_two_notes(self):
        self.midi.note_on(channel=0, note=self.this_note)
        self.midi.update_time(self.this_time)
        self.midi.note_on(channel=0, note=self.this_note)
        self.more_time()
        self.midi.update_time(self.this_time)
        self.midi.note_off(channel=0, note=self.this_note)
        self.midi.update_time(0)
        self.midi.note_off(channel=0, note=self.this_note)

    def less_two_notes(self):
        self.midi.note_on(channel=0, note=self.this_note)
        self.midi.update_time(self.this_time)
        self.midi.note_on(channel=0, note=self.this_note)
        self.less_time()
        self.midi.update_time(self.this_time)
        self.midi.note_off(channel=0, note=self.this_note)
        self.midi.update_time(0)
        self.midi.note_off(channel=0, note=self.this_note)

    def chord(self):
        self.midi.update_time(self.this_time)
        self.midi.note_on(channel=0, note=self.this_note)
        self.midi.update_time(0)
        self.midi.note_on(channel=0, note=self.this_note+4)
        self.midi.note_on(channel=0, note=self.this_note+7)
        self.midi.update_time(self.this_time)
        self.midi.note_off(channel=0, note=self.this_note)
        self.midi.note_off(channel=0, note=self.this_note+4)
        self.midi.note_off(channel=0, note=self.this_note+7)

    def letter(self, letter):
        if letter == "c":
            self.next_note(0)
        elif letter == "d":
            self.next_note(2)
        elif letter == "e":
            self.next_note(4)
        elif letter == "f":
            self.next_note(5)
        elif letter == "g":
            self.next_note(7)
        elif letter == "a":
            self.next_note(9)
        elif letter == "b":
            self.next_note(11)

    def def_func(self, command):
        self.function_list[command.args['name']] = [command.args['code']]

    def save_note(self):
        self.last_note = self.this_note
        self.last_time = self.this_time

    def load_note(self):
        self.this_note = self.last_note
        self.this_time = self.last_time
