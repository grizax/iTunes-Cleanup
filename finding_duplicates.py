## Finding duplicates in your iTunes Library XML
import re
import argparse
import plistlib
import numpy as np
from matplotlib import pyplot

def find_common_tracks(filenames):
    """
    Find common tracks in given playlist files and save them to common.txt
    """
    trackname_sets = []
    for filename in filenames:
        
        # create a new set
        tracknames = set()
        
        # read in playlist
        plist = plistlib.readPlist(filename)
        
        # get the tracks
        tracks = plist['Tracks']
        
        # iterate through the tracks using items() method
        for trackid, track in tracks.items():
            try:
                # add the track name to a set
                tracknames.add(track['Name'])
            except:
                pass
        
        # add to list
        trackname_sets.append(tracknames)
        
        # get the set of common tracks
        common_tracks = set.intersection(*trackname_sets)
        
        # write to file
        if len(common_tracks) > 0:
            f = open("common.txt", 'wb')
            for val in common_tracks:
                s = "%s\n" % val
                f.write(s.encode("UTF-8"))
                f.close()
                print("%d common tracks found. "
                      "Track names written to common.txt." % len(common_tracks))
        else:
            print("No common tracks!")


def find_duplicates(filename):
	print('Finding duplicate tracks in %s...' % filename)
	
    # read in a playlist
	plist = plistlib.readplist(filename)
	
    # get the tracks from the Tracks dict
	tracks = plist['Tracks']
	
    # create a track name dictionary
	tracknames = {}
	
    # iterate through the tracks using items() method
    # checking to see if name is 'in' keyword
	for trackid, track in tracks.items():
		try:
			name = track['Name']
			duration = track['Total Time']
			# look for existing entries 'in' tracknames
			if name in tracknames:
				# if a name and duration match, increment the count
				# and round the track length to the nearest second.
				if duration//1000 == tracknames[name][0]//1000:
				    count = tracknames[name][1]
                    tracknames[name] = (duration, count + 1)
            else:
				# add dict entry as tuple (duration, count)
                # if this is the first time the program has across
                # the track name, it creates a new entry for it, with
                # a count of 1.
			    tracknames[name] = (duration, 1)

		except:
			# ignore in case tracks don't have name
			pass
    
    # store duplicates as (name, count) tuples
    dups = []
    for k, v in tracknames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    # save duplicates to a file
    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
    else:
        print("No duplicate tracks found.")
    f = open("dups.txt", 'wb')
    for val in dups:
        f.write("[%d] %s\n" % (val[0], val[1]))
    f.close()


def plotStats(filename):
    """
    Plot some statistics by reading track information from playlist.
    """
    # read in a playlist
    plist = plistlib.readPlist(filename)
    
    # get the tracks from the playlist
    tracks = plist['Tracks']
    
    # create lists of song ratings and track durations
    ratings = []
    durations = []
    
    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            # ignore
            pass
    
    # ensure that valid data was collected
    if ratings == [] or durations == []:
        print("No valid Album Rating/Total Time data in %s." % filename)
        return
    
    # scatter plot
    x = np.array(durations, np.int32)
    
    # convert to minutes
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')
    
    # plot histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    # show plot
    pyplot.show()

# gather our code in a main() function
def main():
    """
    This program analyzes playlist files (.xml) exported from iTunes.
    """
    parser = argparse.ArgumentParser
    
    # add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()
    
    # add expected arguments
    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)
    
    # parse args
    args = parser.parse_args()
    
    if args.plFiles:
        # find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")


if __name__ == '__main__':
    main()

