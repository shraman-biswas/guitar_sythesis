import sys

from KarplusStrongAlgorithm import KarplusStrongAlgorithm


def main():
	print "[ Karplus-Strong algorithm - play music ]"

	# load rtttl music strings from music.txt
	with open("music.txt") as f:
		music = f.read().splitlines()

	# get music track selection number
	track_num = int(sys.argv[1])-1 if len(sys.argv) > 1 else 7

	# parameters
	alpha = 0.997	# attenuation factor
	offset = 3	# frequecny offset (Hz)

	# initialize Karplus-Strong algorithm and play music
	ksa = KarplusStrongAlgorithm(alpha, offset)
	ksa.play_music(music[track_num])


if __name__ == "__main__":
	main()
