import enum
from pathlib import Path

# Files path
IMAGE_DIR = Path('.') / 'images'
PARALLEL_PORT = 0x0378
# Time constants
FIXATION_DURATION = 0.1
AUDIO_INTERVAL = 0.1
AUDIO_DURATION = 0.2
# Number of times each audio should be played
LOW_AUDIO_COUNT = 15
HIGH_AUDIO_COUNT = 5
IMAGE_DURATION = 0.4
IMAGE_SIZE = (20, 15)
IMAGE_SUFFIX = '*.jpg'
# Fixation symbol and properties
FIXATION_SYMBOL = '+'
FIXATION_SIZE = 3
FIXATION_POSITION = [0, 0]
SPACE_KEY = "space"
OUTPUT_FILENAME = "exampleOutput.csv"
WRITE_OPEN_MODE = 'w'
DEFAULT_UNIT = "deg"
DEFAULT_MONITOR = "testMonitor"
ERROR_EXIT_CODE = -1  # call exit(-1) upon error
ERROR_MESSAGE = "Program exited with exit code -1 due to an error"


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
