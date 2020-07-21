import os
from random import shuffle, choice
from audioCreator import generateSound
from psychopy import visual, core, event

IMAGE_DIR = './images/'


class StimuliSequence:
    """
    Stimuli presentations are as accurate as core.Clock() is.
    """
    # Time constants
    FIXATION_DURATION = 0.1
    AUDIO_TIME = 0.1
    AUDIO_DURATION = 0.2
    # Audio frequencies
    LOW_AUDIO_FREQUENCY = 440.0
    LOW_AUDIO = "low"
    HIGH_AUDIO_FREQUENCY = 500.0
    HIGH_AUDIO = "high"
    # Number of times each audio should be played
    LOW_AUDIO_COUNT = 15
    HIGH_AUDIO_COUNT = 5
    IMAGE_DURATION = 0.4
    # Fixation symbol and properties
    FIXATION_SYMBOL = '+'
    FIXATION_SIZE = 3
    FIXATION_POSITION = [0, 0]
    SPACE_KEY = "space"

    def __init__(self):
        """

        """
        self._mainWindow = visual.Window(
            fullscr=True,
            monitor="testMonitor",
            units="deg"
        )

        self._initImages()
        # Fixation '+' stimuli
        self._fixation = visual.TextStim(
            win=self._mainWindow, text=self.FIXATION_SYMBOL,
            pos=self.FIXATION_POSITION,
            bold=True,
            height=self.FIXATION_SIZE
        )

        self._globalClock = core.Clock()
        self._lowFrequencySound = generateSound(self.LOW_AUDIO_FREQUENCY,
                                                self.AUDIO_DURATION)

        self._highFrequencySound = generateSound(self.HIGH_AUDIO_FREQUENCY,
                                                 self.AUDIO_DURATION)

        self._audioCounter = {self.LOW_AUDIO: 0, self.HIGH_AUDIO: 0}
        event.globalKeys.clear()
        event.globalKeys.add(key=self.SPACE_KEY, func=self._spacePress)

    def _initImages(self):
        """

        :return:
        """
        # Load files
        images = [IMAGE_DIR + imageName for imageName in os.listdir(IMAGE_DIR)]
        shuffle(images)

        # Generate stim object from each image
        self._imageStimuli = [visual.ImageStim(
            win=self._mainWindow,
            image=image
        )
            for image in images]

    def _spacePress(self):
        print("space")

    def _drawFixation(self):
        """

        :return:
        """
        clock = core.Clock()
        while clock.getTime() < self.FIXATION_DURATION:
            self._fixation.draw()
            self._mainWindow.flip()

    def _playHighSound(self):
        self._highFrequencySound.play()
        self._audioCounter[self.HIGH_AUDIO] += 1

    def _playLowSound(self):
        self._lowFrequencySound.play()
        self._audioCounter[self.LOW_AUDIO] += 1

    def _playSound(self):
        """

        :return:
        """
        # If low sounds were played 15 times play the other one
        if self._audioCounter[self.LOW_AUDIO] == self.LOW_AUDIO_COUNT:
            self._playHighSound()
        # If high frequencies were played 5 times play low one
        elif self._audioCounter[self.HIGH_AUDIO] == self.HIGH_AUDIO_COUNT:
            self._playLowSound()
        # Else choose random sound
        else:
            key = choice(list(self._audioCounter.keys()))
            if key == self.LOW_AUDIO:
                self._playLowSound()
            else:
                self._playHighSound()

    def _drawImage(self, image):
        """
        Draw the image stimulus and play random sound
        :param image: image stimulus to show
        :return:
        """
        clock = core.Clock()
        playedSound = False
        while clock.getTime() < self.IMAGE_DURATION:
            image.draw()
            self._mainWindow.flip()
            if clock.getTime() >= self.AUDIO_TIME and not playedSound:
                self._playSound()
                playedSound = True

    def _runSequence(self, image):
        """

        :param image:
        :return:
        """
        self._drawFixation()
        self._drawImage(image)

    def run(self):
        """

        :return:
        """
        self._globalClock.reset()
        for image in self._imageStimuli:
            self._runSequence(image)
        event.globalKeys.remove(key=self.SPACE_KEY)


labProgram = StimuliSequence()
labProgram.run()
core.quit()
