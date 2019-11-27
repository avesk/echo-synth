import numpy as np


def envelope_amplitude(envelope={}, srate=44100):
    if envelope == {}:
        return None

    attack = np.linspace(0.0, 1.0, int(envelope["attack"] * srate))
    decay = np.linspace(1.0, envelope["sustain"][1], int(envelope["decay"] * srate))
    sustain = np.linspace(
        envelope["sustain"][1],
        envelope["sustain"][1],
        int(envelope["sustain"][0] * srate),
    )
    release = (
        np.reciprocal(np.linspace(1, 15, envelope["release"] * srate))
        * envelope["sustain"][1]
    )

    amp_track = np.concatenate((attack, decay, sustain, release), axis=None)

    return amp_track, amp_track.shape[0]
