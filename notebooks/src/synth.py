import numpy as np
from .oscillator import oscillator
from .envelope_extraction import extract_envelope
from .envelope_construction import envelope_amplitude
from .frequency_extraction import extract_n_freq

# 3. build out get_signal


class Synth:
    def __init__(self, signal=[], srate=44100):

        self.signal = signal
        self.srate = srate
        self.frequencies = []
        self.duration = 0
        self.srate = srate
        self.envelope = {
            "attack": 0.0,
            "decay": 0.0,
            "sustain": (0.0, 0.0),
            "release": 0.0,
        }
        self.oscillators = []


    def set_srate(self, srate):
        self.srate = srate

    def get_srate(self):
        return self.srate

    def set_envelope(self, envelope):
        sustain_time, sustain_power = envelope["sustain"]
        self.duration = (
            envelope["attack"] + envelope["decay"] +
            envelope["release"] + sustain_time
        )
        self.envelope = envelope

    def get_envelope(self):
        return self.envelope

    def extract_envelope(self):
        return extract_envelope(self.signal, self.srate)

    def get_duration(self):
        return self.duration

    def get_oscillators(self):
        return self.oscillators
    
    def set_frequencies(self, signal=[]):
        self.oscillators = []
        
        if signal == []:
            signal = self.signal
        
        freqs = self.extract_n_freq(5)
        
        self.frequencies = freqs
        for freq in freqs:
            self.oscillators.append({
                    'freq': freq[0],
                    'amp': freq[1],
                    'wave_type': 'sinusoid',
                    'phase': 0
                     }
                )

        return freqs

    def get_frequencies(self):
        return self.frequencies

    def extract_n_freq(self, n):
        return extract_n_freq(n, self.signal, sample_rate=self.srate)

    def envelope_amp_track(self):
        return envelope_amplitude(self.envelope, self.srate)

    def oscillator(
        self,
        freq=440.0,
        dur=1.0,
        srate=44100.0,
        amp=1.0,
        phase=0.0,
        wave_type="sinusoid",
    ):
        return oscillator(
            freq=freq, dur=dur, srate=srate, amp=amp, phase=phase, wave_type=wave_type
        )

    def set_oscillator(self, index, value):
        self.oscillators[index] = value

    def set_signal(self, signal):
        self.signal = signal

    def get_signal(self):
        return self.signal

    def set_srate(self, srate):
        self.srate = srate

    def get_srate(self):
        return self.srate

    def get_output(self, oscillators=[]):
        output = np.zeros(int(self.srate * self.duration))

        for osc in self.oscillators:
            output += oscillator(
                freq=osc["freq"],
                dur=self.duration,
                amp=osc["amp"],
                phase=osc["phase"],
                wave_type=osc["wave_type"],
            )
        amp_track, length = envelope_amplitude(self.envelope, self.srate)

        return output[:length] * amp_track
