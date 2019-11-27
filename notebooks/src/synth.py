from .oscillator import oscillator

class Synth():
    
    def __init__(self):

        self.signal = []
        self.frequencies = []
        self.srate = 44100
        self.envelope = {
            "attack": 0.0,
            "decay": 0.0,
            "sustain": (0.0, 0.0),
            "release": 0.0
        }

    def set_srate(self, srate):
        self.srate = srate

    def get_srate(self):
        return srate

    def set_envelope(self, envelope):
        self.envelope = envelope 

    def get_envelope(self):
        return self.envelope
    
    def extract_envelope(self):
        return

    def set_frequencies(self):
        return
    
    def get_frequencies(self):
        return self.frequencies

    def amplitude_track(self):
        return

    def oscillator(self, freq=440.0, dur=1.0, srate=44100.0, amp=1.0, phase=0.0, wave_type='sinusoid'):
        return oscillator(freq=freq, dur=dur, srate=srate, amp=amp, phase=phase, wave_type=wave_type)

    def set_signal(self):
        return

    def get_signal(self):
        return self.signal

    def get_output(self):
        # Create empty signal for output
        # add oscillator for each frequency to output
        # Apply envelope to output
        # Return Output
        return
