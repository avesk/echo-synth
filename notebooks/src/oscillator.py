def sinusoid(freq=440.0, dur=1.0, srate=44100.0, amp=1.0, phase = 0.0): 
    t = np.linspace(0,dur,int(srate*dur))
    data = amp * np.sin(2*np.pi*freq *t+phase)
    return data

def oscillator(freq=440.0, dur=1.0, srate=44100.0, amp=1.0, phase=0.0, wave_type='sinusoid'):
    
    if wave_type not in ['sinusoid', 'triangle', 'square']:
        return None
    
    if wave_type == 'sinusoid':
        return sinusoid(freq=freq, dur=dur, srate=srate, amp=amp, phase=phase)
    
    wave = sinusoid(freq=freq, dur=dur, amp=amp)
    
    for i in range(1,20):
        harmonic = 2*i+1
        sin = sinusoid(freq=freq*harmonic, dur=dur, amp=amp)
        if wave_type == 'triangle':
            sin = sin*(np.power(-1,i))*(harmonic**-2)
        else:
            sin = sin / harmonic
        wave = np.add(wave, sin)
        
    if wave_type == 'square':
        return wave * 4 / np.pi 
    if wave_type == 'triangle':
        return wave * np.pi / 4
