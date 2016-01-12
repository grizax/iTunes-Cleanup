## Finding duplicates in your iTunes Library XML

def find_duplicates(filename):
	print('Finding duplicate tracks in %s...' % filename)
	# read in a playlist
	plist = plistlib.readplist(filename)
	# get the tracks from the Tracks dict
	tracks = plist['Tracks']
	# create a track name dictionary
	tracknames = {}
	# iterate through the tracks
	for trackid, track in tracks.items():
		try:
			name = track['Name']
			duration = track['Total Time']
			# look for existing entries
			if name in tracknames:
				# if a name and duration match, increment the count
				# round the track length to the nearest second
				if duration//1000 == tracknames[name][0]//1000:
					count = tracknames[name][1]
					tracknames[names] = (duration, count+1)
			else:
				# add dict entry as tuple (duration, count)
				tracknames[name] = (duration, 1)
		except:
			# ignore
			pass