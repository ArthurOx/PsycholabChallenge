import csv
from pathlib import Path
from random import shuffle
from audio import generate_sound, LOW_AUDIO, HIGH_AUDIO
from psychopy import visual, core, event, constants
from itertools import zip_longest

# Files path
IMAGE_DIR = Path('.') / 'images'


class StimuliSequence:
    """
    Stimuli presentations are as accurate as core.Clock() is.
    """
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

    def __init__(self):
        """
        Initialize window, clock and all stimuli objects
        """
        self._main_window = visual.Window(
            fullscr=True,
            monitor="testMonitor",
            units="deg"
        )

        self._init_images()
        # Fixation '+' stimuli
        self._fixation = visual.TextStim(
            win=self._main_window, text=self.FIXATION_SYMBOL,
            pos=self.FIXATION_POSITION,
            bold=True,
            height=self.FIXATION_SIZE
        )

        self._global_clock = core.Clock()
        self._timings = {"fixationStart": [], "fixationEnd": [],
                         "imageStart": [], "imageEnd": [], "audioStart": [],
                         "audioEnd": [], "keyPress": []}

        # Create list with audio objects and shuffle it
        audio_list = [
                         generate_sound(LOW_AUDIO, self.AUDIO_DURATION)
                     ] * self.LOW_AUDIO_COUNT
        audio_list += [generate_sound(HIGH_AUDIO, self.AUDIO_DURATION)
                       ] * self.HIGH_AUDIO_COUNT
        shuffle(audio_list)
        self._audio_iter = iter(audio_list)

        event.globalKeys.clear()
        event.globalKeys.add(key=self.SPACE_KEY, func=self._space_press)

    def _init_images(self):
        """
        Initialize all image stimuli objects
        """
        # Load files
        files = IMAGE_DIR.rglob(self.IMAGE_SUFFIX)
        images = [str(image_name) for image_name in files]
        shuffle(images)

        # Generate stim object from each image
        self._image_stimuli = [visual.ImageStim(
            win=self._main_window,
            image=image,
            size=self.IMAGE_SIZE
        )
            for image in images]

    def _space_press(self):
        """
        Called upon space key press event, records its timestamp
        """
        self._timings["keyPress"].append(self._global_clock.getTime())

    def _draw_fixation(self):
        """
        Draw the fixation point
        """
        clock = core.Clock()
        self._timings["fixationStart"].append(self._global_clock.getTime())

        while clock.getTime() < self.FIXATION_DURATION:
            self._fixation.draw()
            self._main_window.flip()

        self._timings["fixationEnd"].append(self._global_clock.getTime())

    def _draw_image(self, image):
        """
        Draw the image stimulus and play random sound
        :param image: image stimulus to show
        """
        clock = core.Clock()
        played_sound = False
        recorded_sound = False
        self._timings["imageStart"].append(self._global_clock.getTime())
        audio = None
        while clock.getTime() < self.IMAGE_DURATION:
            image.draw()
            self._main_window.flip()
            if clock.getTime() >= self.AUDIO_INTERVAL and not played_sound:
                self._timings["audioStart"].append(
                    self._global_clock.getTime())
                audio = next(self._audio_iter)
                audio.play()
                played_sound = True

            # Append audio end timestamp
            if played_sound and not recorded_sound and audio.status == \
                    constants.FINISHED:
                self._timings["audioEnd"].append(self._global_clock.getTime())
                recorded_sound = True

        self._timings["imageEnd"].append(self._global_clock.getTime())

    def _run_sequence(self, image):
        """
        Run a single cycle
        :param image: image to show in current cycle.
        """
        self._draw_fixation()
        self._draw_image(image)

    def run(self):
        """
        Run all program cycles
        """
        self._global_clock.reset()
        for image in self._image_stimuli:
            self._run_sequence(image)
        event.globalKeys.remove(key=self.SPACE_KEY)

    def save_into_file(self):
        """
        Saves timings into a csv file
        """
        try:
            with open(self.OUTPUT_FILENAME, self.WRITE_OPEN_MODE,
                      newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(self._timings.keys())

                for values in zip_longest(*self._timings.values()):
                    writer.writerow(values)
        except IOError:
            exit()


if __name__ == "__main__":
    lab_program = StimuliSequence()
    lab_program.run()
    lab_program.save_into_file()
    core.quit()
