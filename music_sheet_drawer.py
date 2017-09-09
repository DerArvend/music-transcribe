from os import system, remove
from subprocess import call
import analysis
import sys


def generate_lilypond_source(lp_note_list: list, output_filename: str = 'untitled'):
    a = ' '.join(lp_note_list)
    lp_string = '\\version "2.18.2"\n{{{}}}'.format(' '.join(lp_note_list))

    try:
        f = open(output_filename + ".ly", "x")
    except:
        f = open(output_filename + ".ly", "w")

    f.write(lp_string)
    f.close()
    call(["lilypond", "{}{}".format(output_filename, '.ly')])

    remove(output_filename + ".ly")
    # remove(output_filename + ".log")


def get_lp_note_list(note_list: list):
    return [note.to_lilypond() for note in note_list]


def main():
    if len(sys.argv) < 1:
        raise IOError('script must get filepath as argument')

    filepath = 'tests\\cde-sine.wav'
    freqs = analysis.get_frequencies(filepath)
    blocks = analysis.merge_frequencies(freqs)
    notes = analysis.get_note_list(blocks)
    generate_lilypond_source(get_lp_note_list(notes))


if __name__ == '__main__':
    main()
