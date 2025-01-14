import numpy as np
from scipy.signal import sawtooth
from scipy.io import wavfile

def create_orbit_beep(duration=0.2, frequency=880, sample_rate=44100):
    """
    Create a William Orbit style beep with frequency modulation and filtering
    """
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create base sawtooth wave
    base = sawtooth(2 * np.pi * frequency * t)
    
    # Add subtle frequency modulation
    mod_freq = 8  # 8 Hz modulation
    mod_depth = 10  # 10 Hz depth
    fm = frequency + mod_depth * np.sin(2 * np.pi * mod_freq * t)
    modulated = sawtooth(2 * np.pi * fm * t)
    
    # Apply envelope
    attack = int(0.01 * sample_rate)
    release = int(0.1 * sample_rate)
    envelope = np.ones_like(t)
    envelope[:attack] = np.linspace(0, 1, attack)
    envelope[-release:] = np.linspace(1, 0, release)
    
    # Apply envelope to modulated signal
    signal = modulated * envelope
    
    # Normalize
    signal = signal / np.max(np.abs(signal))
    
    return signal

def create_orbit_sequence(frequencies=[880, 1760, 1175, 987], tempo=120):
    """
    Create a sequence of beeps in William Orbit style
    """
    sample_rate = 44100
    beat_duration = 60 / tempo  # duration of one beat in seconds
    sequence = np.array([])
    
    for freq in frequencies:
        beep = create_orbit_beep(duration=beat_duration/2, frequency=freq)
        silence = np.zeros(int(sample_rate * beat_duration/2))
        sequence = np.concatenate([sequence, beep, silence])
    
    # Convert to 16-bit integer format
    sequence = np.int16(sequence * 32767)
    return sequence, sample_rate

# Create and save a sequence
sequence, sample_rate = create_orbit_sequence()
wavfile.write('orbit_beeps.wav', sample_rate, sequence)