class RTTTL:

	# parse Ring Tone Text Language protocol
	def parse_rtttl(self, music_str):
		self._music_str = music_str
		# split name, defaults, and data sections
		self._name, defaults, data = self._music_str.split(":")
		# split defaults into duration, octave, and beat sections
		d, o, b = defaults.split(",")
		self._def_duration = int(d.split("=")[1])
		self._def_octave = int(o.split("=")[1])
		self._def_beat = int(b.split("=")[1])
		# split data section into notes
		data = data.split(",")
		# parse each note
		self._music = [self._parse_note(x) for x in data]
		return self._music

	# parse each note
	def _parse_note(self, x):
		# skips 1st blank space
		i = 0 if x[0] != " " else 1 
		j = i
		# searches for 1st alphabet - beginning of note
		while not x[j].isalpha():
			j += 1
		duration = int(x[i:j]) if j > i else self._def_duration
		k = j
		# searches for 1st number - beginning of octave
		while k < len(x) and not x[k].isdigit(): 
			k += 1
		# checks presence of dot
		dot = (x[k-1] == ".")
		# removes dot if found
		note = (x[j:k-1] if dot else x[j:k]).lower()
		octave = int(x[k:]) if k != len(x) else self._def_octave
		return duration, note, octave, dot
