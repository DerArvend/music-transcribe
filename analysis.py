import numpy as np
import soundfile
import json
from music_classes import *


def get_frequencies(file_path: str, fft_window_size: int = 4096, filtered=True, filter_window_size=1):
    freqencies_list = []

    file = soundfile.SoundFile(file_path)
    blocks = file.blocks(blocksize=fft_window_size, always_2d=True)

    fft_data = [np.fft.fft(block[:, 0]) for block in blocks]
    power_spectrums = [[abs(value) ** 2 for value in frameset] for frameset in fft_data]

    for spectrum in power_spectrums:
        peak_power = max(spectrum[:fft_window_size // 2])

        if filtered:
            if peak_power < 1000:
                continue

        pitch = spectrum.index(peak_power) * (file.samplerate / fft_window_size)
        freqencies_list.append(pitch)

    if filtered:
        filter_pitch_list(freqencies_list, filter_window_size)

    return freqencies_list


def filter_pitch_list(freq_list: list, filter_window_size: int = 1):
    if filter_window_size >= len(freq_list) // 2:
        raise Exception('Filter window size must be less than half of list length')

    if filter_window_size < 1:
        raise Exception('Filter window must be positive integer')

    if filter_window_size == 1:
        filter_pitch_list_simple(freq_list)
        return

    indexes_to_remove = list()

    for i in range(filter_window_size, len(freq_list) - filter_window_size):

        slice = freq_list[i - filter_window_size:i + filter_window_size]
        if len(set(slice)) != 1:
            indexes_to_remove.append(i)

    freq_list = [freq_list[i] for i in range(len(freq_list)) if not i in indexes_to_remove]


def filter_pitch_list_simple(freq_list: list):
    shift = 0

    for i in range(1, len(freq_list) - 1):
        if freq_list[i - shift] != freq_list[i - shift - 1] and freq_list[i - shift] != freq_list[i - shift + 1]:
            freq_list.pop(i - shift)
            shift += 1


def merge_frequencies(freq_list: list) -> list:
    freq_blocks_list = list()

    repetitions = 1
    for i in range(len(freq_list) - 1):
        if freq_list[i] == freq_list[i + 1]:
            repetitions += 1
        else:
            freq_blocks_list.append(FrequencyBlock(freq_list[i], length=repetitions))
            repetitions = 1

    return freq_blocks_list



def get_note_list(freq_blocks_list) -> list:
    notes_list = list()

    pitches_dict = {float(freq): note for freq, note in json.load(open('pitches.json')).items()}

    for block in freq_blocks_list:
        pitch = min(pitches_dict.keys(), key=lambda x: abs(x - block.pitch))
        pitch_class = pitches_dict[pitch][:-1]
        octave = pitches_dict[pitch][-1]

        notes_list.append(Note(pitch_class, int(octave)))

    return notes_list
