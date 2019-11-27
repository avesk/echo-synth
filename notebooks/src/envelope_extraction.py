import numpy as np
from scipy import signal as sig
import librosa


def three_step_envelope(signal, K=200, freq_cutoff=0.125, padlen=150):
    # Take the absolute value of the signal
    abs_signal = np.abs(signal)

    # Split signal into K bunches of N/K samples and take the max
    # value from each bunch
    N = len(abs_signal)
    peaks = []
    for i in range(0, N, K):
        peaks.append(np.max(abs_signal[i : i + K]))
    peaks = np.asarray(peaks)

    # Apply a LPF with a cut off of 0.125 Times the Niquist (125 Hz)
    b, a = sig.butter(8, freq_cutoff)
    lpf_peaks = sig.filtfilt(b, a, peaks, padlen=padlen)

    return lpf_peaks


def find_first_onset(signal, sr, K=200):
    onsets = []
    while len(onsets) == 0:
        approx_env = three_step_envelope(signal=signal, K=K)
        # convert envelope to Fortran-contiguous
        ftrn_env = np.asfortranarray(approx_env)

        onsets = librosa.onset.onset_detect(y=ftrn_env, sr=sr)
        print(onsets)
        K -= 10

    return onsets[0]


def attack(signal, onset, sr):
    """
    Computes attack time by taking the difference 
    of the argmax and onset and dividing by the sampling rate
    """
    return (np.argmax(np.abs(signal)) - onset) / sr


def extract_envelope(signal, sr):
    """
    Approximate envelope, Extract attack
    """
    K = 200
    approx_env = three_step_envelope(signal=signal, K=K)
    # convert envelope to Fortran-contiguous
    ftrn_env = np.asfortranarray(approx_env)

    first_onset = find_first_onset(signal, sr=sr)
    attack_t = attack(ftrn_env, first_onset, sr)

    return {"attack": attack_t, "decay": 0.5, "sustain": (1.0, 0.5), "release": 2.0}
