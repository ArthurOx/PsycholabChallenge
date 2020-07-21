from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound

# Audio frequencies
LOW_AUDIO = 440.0
HIGH_AUDIO = 500.0


def generate_sound(frequency, duration):
    """
    Generate a pure tone sound
    :param frequency: frequency of the sound
    :param duration: duration (in secs) of sound
    :return: a PTB sound object to call .play() on
    """
    generatedSound = sound.Sound(value=frequency, secs=duration)
    return generatedSound
