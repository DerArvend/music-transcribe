from os import system, remove
from subprocess import call
import analysis

def generate_lilypond_source(lp_note_list: list, filename: str = 'untitled'):
    lp_string = '\\version "2.18.2"\n{{}}'.format(' '.join(lp_note_list))

    try:
        f = open(filename + ".ly", "x")
    except:
        f = open(filename + ".ly", "w")

    f.write(lp_string)
    f.close()
    call(["lilypond.exe", "{}{}".format(filename, '.ly')])

    remove(filename + ".ly")



def get_lp_note_list(note_list: list):
    return [note.to_lilypond() for note in note_list]

