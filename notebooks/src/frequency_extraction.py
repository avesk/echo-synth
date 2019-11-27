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
    front = np.argmax(audio_mag > 0.01)
    audio_mag = audio_mag[front:]
    b = audio_mag[::-1]
    back = len(b) - np.argmax(b > 0.01) - 1
    return audio[front:back]


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


def _normalize_N_top(top_N):
    max_amp = max(top_N, key=lambda x: x[1])[1]
    print(max_amp)
    top_N = [(freq, amp / max_amp) for freq, amp in top_N]
    return top_N


def extract_n_freq(N, audio, sample_rate=44100, n_fft=2048, use_stft=False):
    audio = _normalize(audio)
    audio = _clean_input(audio)
    fft_data = _get_fft_data(audio)
    bin_to_freq = librosa.fft_frequencies(sample_rate, n_fft)
    top_N = _get_n_top(fft_data, N, bin_to_freq)
    top_N = [(freq, amp) for freq, amp in top_N if freq > 40]
    top_N = _normalize_N_top(top_N)
    return top_N
