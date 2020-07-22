import csv
from random import shuffle
from audio import generate_sound, LOW_AUDIO, HIGH_AUDIO
from psychopy import visual, core, event, constants
# from psychopy import parallel
from itertools import zip_longest
from config import *


class StimuliSequence:
    """
    Stimuli presentations are as accurate as core.Clock() is.
    """

    def __init__(self):
        """
        Initialize window, clock and all stimuli objects
        """
        self._main_window = visual.Window(
            fullscr=True,
            monitor=DEFAULT_MONITOR,
            units=DEFAULT_UNIT
        )

        self._init_images()
        # Fixation '+' stimuli
        self._fixation = visual.TextStim(
            win=self._main_window, text=FIXATION_SYMBOL,
            pos=FIXATION_POSITION,
            bold=True,
            height=FIXATION_SIZE
        )

        self._global_clock = core.Clock()
        self._timings = {Events.fixationStart: [], Events.fixationEnd: [],
                         Events.imageStart: [], Events.imageEnd: [],
                         Events.audioStart: [], Events.audioEnd: [],
                         Events.keyPress: []}
        # self._port = parallel.ParallelPort(address=self.PARALLEL_PORT)
        # Create list with audio objects and shuffle it
        audio_list = [
                         generate_sound(LOW_AUDIO, AUDIO_DURATION)
                     ] * LOW_AUDIO_COUNT
        audio_list += [generate_sound(HIGH_AUDIO, AUDIO_DURATION)
                       ] * HIGH_AUDIO_COUNT
        shuffle(audio_list)
        self._audio_iter = iter(audio_list)

        event.globalKeys.clear()
        event.globalKeys.add(key=SPACE_KEY, func=self._space_press)

    def _init_images(self):
        """
        Initialize all image stimuli objects
        """
        # Load files
        files = IMAGE_DIR.rglob(IMAGE_SUFFIX)
        images = [str(image_name) for image_name in files]
        shuffle(images)

        # Generate stim object from each image
        self._image_stimuli = [visual.ImageStim(
            win=self._main_window,
            image=image,
            size=IMAGE_SIZE
        )
            for image in images]

    def _space_press(self):
        """
        Called upon space key press event, records its timestamp
        """
        self._timings[Events.keyPress].append(self._global_clock.getTime())

    def _draw_fixation(self):
        """
        Draw the fixation point
        """
        clock = core.Clock()
        self._timings[Events.fixationStart].append(
            self._global_clock.getTime())

        while clock.getTime() < FIXATION_DURATION:
            self._fixation.draw()
            self._main_window.flip()

        self._timings[Events.fixationEnd].append(self._global_clock.getTime())

    def _draw_image(self, image):
        """
        Draw the image stimulus and play random sound
        :param image: image stimulus to show
        """
        clock = core.Clock()
        played_sound = False
        recorded_sound = False
        self._timings[Events.imageStart].append(self._global_clock.getTime())
        audio = None
        while clock.getTime() < IMAGE_DURATION:
            image.draw()
            self._main_window.flip()
            if clock.getTime() >= AUDIO_INTERVAL and not played_sound:
                self._timings[Events.audioStart].append(
                    self._global_clock.getTime())
                audio = next(self._audio_iter)
                audio.play()
                played_sound = True

            # Append audio end timestamp
            if played_sound and not recorded_sound and audio.status == \
                    constants.FINISHED:
                self._timings[Events.audioEnd].append(self._global_clock.getTime())
                recorded_sound = True

        self._timings[Events.imageEnd].append(self._global_clock.getTime())

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
        event.globalKeys.remove(key=SPACE_KEY)

    def save_into_file(self):
        """
        Saves timings into a csv file
        """
        try:
            with open(OUTPUT_FILENAME, WRITE_OPEN_MODE,
                      newline='') as outfile:
                writer = csv.writer(outfile)
                # keys without the enum name
                keys = [key.name for key in self._timings.keys()]
                writer.writerow(keys)

                for values in zip_longest(*self._timings.values()):
                    writer.writerow(values)
        except IOError:
            print(ERROR_EXIT_CODE)
            exit(ERROR_EXIT_CODE)


if __name__ == "__main__":
    lab_program = StimuliSequence()
    lab_program.run()
    lab_program.save_into_file()
    core.quit()
