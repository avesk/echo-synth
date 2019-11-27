import soundfile as sf
import IPython.display as ipd
import numpy as np
import math as math
import matplotlib.pyplot as plt
import scipy
from librosa.display import specshow
import librosa


def _clean_input(audio):
    audio_mag = np.abs(audio)
    audio_mag = audio_mag[np.argmax(audio_mag > 0.1):]
    b = audio_mag[::-1]
    i = len(b) - np.argmax(b > 0.1) - 1
    audio_mag = audio_mag[:i]
    return audio_mag


def _normalize(audio_signal):
    audio_signal = audio_signal.astype(np.float32) / 32767.0
    return (0.9 / max(audio_signal)) * audio_signal


def _group_close_indices(bin_indices):
    bin_indices.sort()
    new_list = [bin_indices[0]]
    for i in range(1, len(bin_indices)):
        if(bin_indices[i] - 1 == bin_indices[i - 1]):
            if(isinstance(new_list[-1], list)):
                new_list[-1].append(bin_indices[i])
            else:
                new_list[-1] = [new_list[-1], bin_indices[i]]
        else:
            new_list.append(bin_indices[i])
    return new_list


def _bin_to_freq_mag(indices, bin_to_freq, fftdata):
    output = []
    for idx in indices:
        if(isinstance(idx, list)):
            freqs = bin_to_freq[idx]
            mags = fftdata[idx]
            output.append((np.mean(freqs), np.mean(mags)))
        else:
            output.append((bin_to_freq[idx], fftdata[idx]))
    return output


def _get_n_top(fftdata, N, bin_to_freq):
    """ return frequency, amplitude"""
    indices = np.argpartition(fftdata, -N)[-N:]
    grouped_indices = _group_close_indices(indices)
    return _bin_to_freq_mag(grouped_indices, bin_to_freq, fftdata)


def _get_fft_data(audio, n_fft=2048, use_stft=False):
    if(use_stft):
        frame_n = 5
        D = np.abs(librosa.stft(audio, n_fft=n_fft,
                                hop_length=2048, win_length=2048))
        frame = D[:, frame_n]
    else:
        D = np.abs(scipy.fft(audio, n=n_fft))
        frame = D[:len(D)//2]
    return frame


def extract_n_freq(N, audio, sample_rate=44100, n_fft=2048, use_stft=False):
    audio = _normalize(audio)
    audio = _clean_input(audio)
    fft_data = _get_fft_data(audio)
    bin_to_freq = librosa.fft_frequencies(sample_rate, n_fft)
    top_N = _get_n_top(fft_data, N, bin_to_freq)
    return top_N
