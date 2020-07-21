from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound


def generateSound(frequency, duration):
    """

    :param frequency:
    :param duration:
    :return:
    """
    generatedSound = sound.Sound(value=frequency, secs=duration)
    return generatedSound
