from pathlib import Path

import numpy as np
import simpleaudio as sa
import wavio
from PIL import Image

# credit to Levi Borodenko: 
__author__ = "Levi Borodenko"
__copyright__ = "Levi Borodenko"
__license__ = "mit"


class SpectroGraphic(object):
    """
    Takes an image file and creates a sound that
    draws that image on a spectrogram.

    [description]
    Arguments:
        path {Path} -- Path to file (e.g.: {"./data/python.png"})

    Keyword Arguments:
        height {int} -- y-resolution in spectrogram (default: {100})
        duration {int} -- duration of sound in seconds (default: {20})
        min_freq {int} -- minimal freq. for image (default: {1000})
        max_freq {int} -- maximal freq. for image (default: {8000})
        sample_rate {int} -- Sample rate (default: {44100})
        num_tones {int} -- Number of tones to used to fill in each pixel
        (default: {3})
        contrast {float} -- Contrast between loud and quiet pixels
        (default: {5})
    """

    def __init__(
        self,
        path: Path,
        height: int = 100,
        duration: int = 20,
        min_freq: int = 1000,
        max_freq: int = 8000,
        sample_rate: int = 44100,
        num_tones: int = 3,
        contrast: float = 5,
        use_black_and_white: bool = False,
    ):

        super(SpectroGraphic, self).__init__()
        self.PATH = Path(path)
        self.image = Image.open(self.PATH)
        self.HEIGHT = height
        self.DURATION = duration
        self.SAMPLE_RATE = sample_rate

        # Width after setting height to self.HEIGHT
        # Preserving aspect-ratio
        self.WIDTH = int(self.image.width * (self.HEIGHT / self.image.height))

        # duration per column
        self.DURATION_COL = self.DURATION / self.WIDTH

        # instance of ColumnToSound that will generate
        # the sounds for each column of the image
        self.col_to_sound = ColumnToSound(
            duration=self.DURATION_COL,
            sample_rate=sample_rate,
            min_freq=min_freq,
            max_freq=max_freq,
            y_resolution=height,
            num_tones=num_tones,
            contrast=contrast,
        )

        # Flag whether we have processed the image yet
        self.is_processed = False

        # if true, then we do not use grey-scale with only 0 and 1
        self.USE_BLACK_AND_WHITE = use_black_and_white

    def _resize(self):
        """[summary]
        We resize the image to be at most self.HEIGHT pixels tall.

        [description]
        The reason is to put a limit on the frequency resolution that
        we would need to draw it in on the spectrograph.
        """

        # resizing image
        self.image = self.image.resize(
            size=(self.WIDTH, self.HEIGHT), resample=Image.LANCZOS
        )

    def _preprocess(self):
        """Resizes the image, converts it to grey-scale
        and returns the columns as a np.ndarray.
        """

        # resize image
        self._resize()

        # convert to gray scale
        self.image = self.image.convert(mode="L")

        # get pixels as array and normalise them to be
        # between 0 and 1
        self.image_array = np.array(self.image) / 255.0

        # transpose image to get list of columns
        self.columns = np.transpose(self.image_array)

        if self.USE_BLACK_AND_WHITE:
            self.columns[self.columns >= 0.5] = 1
            self.columns[self.columns < 0.5] = 0
            self.columns = 1 - self.columns

    def _process(self):
        """Preprocesses the image then turns the
        columns into sounds and stacks them up to produce
        the resulting sound.
        """
        self._preprocess()

        audio_array = np.hstack(
            [self.col_to_sound.gen_soundwall(col) for col in self.columns]
        )

        # convert to 16-bit data
        audio_array *= 32767 / np.max(np.abs(audio_array))
        audio_array = audio_array.astype(np.int16)

        return audio_array

    @property
    def sound_array(self):
        if self.is_processed:
            return self._sound_array
        else:
            self.is_processed = True
            self._sound_array = self._process()
            return self._sound_array

    def play(self):
        """Plays the SpectroGraphic sound.
        """

        # get sound array
        audio = self.sound_array

        # play it using simpleaudio
        wave_object = sa.WaveObject(audio, 1, 2, self.SAMPLE_RATE)
        play_object = wave_object.play()
        play_object.wait_done()

    def save(self, wav_file: Path = "SpectroGraphic.wav"):
        """saves the spectrographic to a .wav file

        We use the wavio module
        """

        wavio.write(wav_file, self.sound_array, self.SAMPLE_RATE)


class ColumnToSound(object):
    """Class to turn grey-scale image columns into
    a sound.

    It takes a numpy array of grey intensities (in the range 0 to 1)
    of length Y_RESOLUTION and turns them into a DURATION seconds long
    sound in the frequency range between MIN_FREQ and MAX_FREQ.


    Arguments:
        duration {int} -- Duration of sound in seconds

    Keyword Arguments:
        sample_rate {int} -- Sample rate of sound (default: {44100})
        min_freq {int} -- Minimal frequency in the spectrograph
        (default: {10000})
        max_freq {int} -- Maximal frequency in the spectrograph
        (default: {17000})
        y_resolution {int} -- Number of pixels to plot (default: {1000})
        num_tones {int} -- Number of tones to use to fill out each pixel
        (default: {3})
        contrast {float} -- Contrast between loud and quiet pixels
        (default: {5})
    """

    def __init__(
        self,
        duration: int,
        sample_rate: int = 44100,
        min_freq: int = 10000,
        max_freq: int = 17000,
        y_resolution: int = 1000,
        num_tones: int = 3,
        contrast: float = 5,
    ):
        super(ColumnToSound, self).__init__()

        # saving imporant parameters
        self.Y_RESOLUTION = y_resolution
        self.CONTRAST = contrast

        # sample rate; 44100 is a good default
        self.SAMPLE_RATE = sample_rate

        # region in which to draw the pixel sound
        self.MIN_FREQ = min_freq
        self.MAX_FREQ = max_freq

        # Number of tones used to fill the pixel sound
        self.NUM_TONES = num_tones

        # frequency window for each pixel sound
        self.HEIGHT = (max_freq - min_freq) / (y_resolution)

        # frequency delta between each tone that fills the pixel sound
        self.tone_delta = self.HEIGHT / num_tones

        # duration in seconds
        self.DURATION = duration

    def _get_wave(self, freq: int, intensity: float = 1, duration: int = 1):
        """Core method that takes a frequency, intensity and duration
        and returns an array representing the corresponding sound.


        Arguments:
            freq {int} -- frequency

        Keyword Arguments:
            intensity {float} -- between 0 and 1 (default: {1})
            duration {float} -- in seconds (default: {1})

        Returns:
            np.ndarray -- sound wave array
        """

        # get timesteps
        t = np.linspace(
            start=0, stop=duration, num=int(duration * self.SAMPLE_RATE), endpoint=False
        )

        # generate corresponding sine wave.
        # this is the only place that CONTRAST acts in
        sound_wave = (intensity ** self.CONTRAST) * np.cos(freq * t * 2 * np.pi)

        return sound_wave

    def pixel_to_sound(self, y: int, intensity: float = 1):
        """Takes a pixel in a imagae column at the y'th position
        from the top and turns it into a sound at a corresponding
        position in the spectrum.

        [description]

        Arguments:
            y {int} -- position of pixel in column from the top.

        Keyword Arguments:
            intensity {float} -- [description] (default: {1})

        Returns:
            np.ndarray -- sound array

        Raises:
            ValueError
        """

        # pixel position (count) from the top must be
        # positive and not larger than the number of pixels
        # in the column.
        if y < 0 or y > self.Y_RESOLUTION:
            raise ValueError("y must be between 0 and 1.")

        # Loudness should be between 0 and 1
        if not (0 <= intensity <= 1):
            raise ValueError("Intensity must be between 0 and 1.")

        # Duration should be positive
        if self.DURATION < 0:
            raise ValueError("Duration must be positive.")

        # calculating base frequency for pixel sound
        base_freq = (self.MAX_FREQ - self.MIN_FREQ) / (self.Y_RESOLUTION) * (
            self.Y_RESOLUTION - y
        ) + self.MIN_FREQ

        # get base wave
        wave = self._get_wave(base_freq, intensity, self.DURATION)

        # add tones to fill up pixel sound
        # first tone:
        tone_freq = base_freq

        # iterating over tones, adding up the sounds.
        for _ in range(self.NUM_TONES):

            tone_freq += self.tone_delta
            wave += self._get_wave(tone_freq, intensity, self.DURATION)

        return wave

    def gen_soundwall(self, column: np.ndarray):
        """Takes a column of pixels and generates
        the sound wall.

        [description]

        Arguments:
            column {np.ndarray} -- Y_RESOLUTION long column of
            pixels (values between 0 and 1)

        Returns:
            np.ndarray -- soundwall
        """

        # empty wave that we will add individual
        # pixel sounds onto
        wave = self.pixel_to_sound(0, 0)

        # iterating over column, adding the pixel sounds
        # of all pixels together to get the final wave.
        for idx, intensity in enumerate(column):
            wave += self.pixel_to_sound(idx, intensity)

        return wave