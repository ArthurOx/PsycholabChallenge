import enum


class Events(enum.Enum):
    """
    Enums of stimuli events
    """
    fixationStart = 1
    fixationEnd = 2
    imageStart = 3
    imageEnd = 4
    audioStart = 5
    audioEnd = 6
    keyPress = 7
