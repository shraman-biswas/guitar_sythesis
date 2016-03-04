import pyaudio
import random
import time
import wave

from RTTTL import RTTTL


class KarplusStrongAlgorithm(RTTTL):

	# source: https://en.wikipedia.org/wiki/Scientific_pitch_notation
	# octaves:	0	1	2	3	4	5	6	7	8	9	10
	_pitch_table = {
		"c" : [ 16.352, 32.703, 65.406, 130.81, 261.63, 523.25, 1046.5, 2093.0, 4186.0, 8372.0, 16744.0, ],
		"c#" : [ 17.324, 34.648, 69.296, 138.59, 277.18, 554.37, 1108.7, 2217.5, 4434.9, 8869.8, 17739.7, ],
		"d" : [ 18.354, 36.708, 73.416, 146.83, 293.66, 587.33, 1174.7, 2349.3, 4698.6, 9397.3, 18794.5, ],
		"d#" : [ 19.445, 38.891, 77.782, 155.56, 311.13, 622.25, 1244.5, 2489.0, 4978.0, 9956.1, 19912.1, ],
		"e" : [ 20.602, 41.203, 82.407, 164.81, 329.63, 659.26, 1318.5, 2637.0, 5274.0, 10548.1, 21096.2, ],
		"f" : [ 21.827, 43.654, 87.307, 174.61, 349.23, 698.46, 1396.9, 2793.8, 5587.7, 11175.3, 22350.6, ],
		"f#" : [ 23.125, 46.249, 92.499, 185.00, 369.99, 739.99, 1480.0, 2960.0, 5919.9, 11839.8, 23679.6, ],
		"g" : [ 24.500, 48.999, 97.999, 196.00, 392.00, 783.99, 1568.0, 3136.0, 6271.9, 12543.9, 25087.7, ],
		"g#" : [ 25.957, 51.913, 103.83, 207.65, 415.30, 830.61, 1661.2, 3322.4, 6644.9, 13289.8, 26579.5, ],
		"a" : [ 27.500, 55.000, 110.00, 220.00, 440.00, 880.00, 1760.0, 3520.0, 7040.0, 14080.0, 28160.0, ],
		"a#" : [ 29.135, 58.270, 116.54, 233.08, 466.16, 932.33, 1864.7, 3729.3, 7458.6, 14917.2, 29834.5, ],
		"b" : [ 30.868, 61.735, 123.47, 246.94, 493.88, 987.77, 1975.5, 3951.1, 7902.1, 15804.3, 31608.5, ],
	}

	def __init__(self, alpha=0.997, offset=3):
		self._offset = offset
		# parameters
		self._alpha = alpha	# attenuation factor
		self._nchannels = 1	# number of audio output channels
		self._swidth = 2	# sample width (bytes)
		self._srate = 44100	# sampling rate (Hz)
		# initialize audio output device
		self._audio_device = pyaudio.PyAudio()
		self._audio_stream = self._audio_device.open(
					format=self._audio_device. \
					get_format_from_width(self._swidth),
					channels=self._nchannels,
					rate=self._srate,
					output=True)

	# play note of specified frequency (Hz) and duration (seconds)
	def play_note(self, note_freq, duration):
		# compute parameters
		N = int(self._srate / note_freq)
		nsamples = int(self._srate * duration)
		buf = [random.uniform(-1,1) for _ in range(N)]
		# online processing
		for i in range(nsamples):
			n = i % N
			if n == 0:
				tmp_buf = [int(x * 32767) for x in buf]
				data = wave.struct.pack("%ih"%(len(tmp_buf)), 
								*list(tmp_buf))
				self._audio_stream.write(data)
			average = (0.5 * (buf[n] + buf[n-1]) 
					if n != 0 else buf[N-1])
			buf[n] = self._alpha * average

	def play_music(self, music_str):
		# parse music string and play music
		music = self.parse_rtttl(music_str)
		self._timestep = 240.0 / self._def_beat
		for x in music:
			print x
			# parse note parameters
			note = x[1]
			octave = x[2]
			dot = x[3]
			# calculate duration
			duration = self._timestep * (1.5 if dot else 1) / x[0]
			if note == "p" or note == "-":
				time.sleep(duration)
			else:
				note_freq = self._pitch_table[note][octave - self._offset]
				self.play_note(note_freq, duration)
