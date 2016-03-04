class RTTTL:

	def parse_rtttl(self, music_str):
		self._music_str = music_str
		self._name, defaults, data = self._music_str.split(":")
		d, o, b = defaults.split(",")
		self._def_duration = int(d.split("=")[1])
		self._def_octave = int(o.split("=")[1])
		self._def_beat = int(b.split("=")[1])
		data = data.split(",")
		self._music = [self._parse_note(x) for x in data]
		return self._music

	def _parse_note(self, x):
		i = 0 if x[0] != " " else 1 # skips 1st blank space 
		j = i
		while not x[j].isalpha(): # searches for 1st alphabet - beginning of note
			j += 1
		duration = int(x[i:j]) if j > i else self._def_duration
		k = j
		while k < len(x) and not x[k].isdigit(): # searches for 1st number - beginning of octave 
			k += 1
		dot = (x[k-1] == ".") # checks presence of dot
		note = (x[j:k-1] if dot else x[j:k]).lower() # removes dot if found
		octave = int(x[k:]) if k != len(x) else self._def_octave
		return duration, note, octave, dot
