class NoteValue:
    def __init__(self, value_num):
        self.value_num = value_num

    def __repr__(self):
        return "{}th".format(self.value_num)

    def __int__(self):
        return self.value_num


class Note:
    lp_octave_system = {1: ",,", 2: ",", 3: "", 4: "'", 5: "''", 6: "'''", 7: "''''", 8: "'''''"}

    def __init__(self, pitch_class: str, octave: int, note_value: NoteValue = NoteValue(4)):
        pitch_class = pitch_class
        if (not self.__is_valid_pitch_class(pitch_class)) or (octave not in range(1, 9)):
            raise ValueError('Wrong pitch class or octave')

        self.pitch_class = pitch_class
        self.octave = octave
        self.note_value = note_value

    def __repr__(self):
        return "{}{} - {}th".format(self.pitch_class, self.octave, int(self.note_value))

    def to_lilypond(self) -> str:
        return '{}{}{}'.format(self.pitch_class.lower(),
                               self.lp_octave_system[self.octave],
                               int(self.note_value))


    @staticmethod
    def __is_valid_pitch_class(pitch_class: str) -> bool:
        flag = pitch_class in ['A', 'Bis', 'B', 'C', 'Dis', 'D', 'Eis', 'E', 'F', 'Gis', 'G', 'Ais']
        return flag


class FrequencyBlock:
    def __init__(self, pitch: float, length: int = 1):
        self.pitch = pitch
        self.length = length

    def __repr__(self):
        return '{} - {}'.format(self.pitch, self.length)


class NoteGrid:
    def __init__(self, n_frames):
        self.grid = [list() for i in range(n_frames)]

    def add_note(self, position: int, note: Note):
        self.grid[position].append(note)

    def remove_note(self, position: int, note: Note):
        try:
            self.grid[position].remove(note)
        except Exception:
            raise ValueError("There is no {} in this frame".format(str(note)))
