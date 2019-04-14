#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import subprocess
import sys

# spacestream.py
# Scrapes a list of youtube channels for any that have a live stream currently
# running.
# Launches the first live stream on each channel in mpv.
#
# The general idea of this script is to not miss live rocket launches...

spacestreams = [
        "https://www.youtube.com/user/spacexchannel",
        "https://www.youtube.com/user/RocketLabNZ",
        "https://www.youtube.com/user/virgingalactic",
        "https://www.youtube.com/channel/UCRn9F2D9j-t4A-HgudM7aLQ",

        # NasaTV is commented out because they seem to have 24/7 live tv but
        # uncomment the following two channels if you just want to test.
        # The other one is the crappy "Space & Universe (Official)" channel that just
        # rebroadcasts old launches "LIVE" 24/7. Good for testing I guess.

        #"https://www.youtube.com/user/NASAtelevision",
        #"https://www.youtube.com/user/NewerDocumentaries",
]

def livestream_url(stream):
    r = requests.get(stream)
    if r.status_code != 200:
        print('NOOOOooooo')
        return None

    soup = BeautifulSoup(r.text, features="html.parser")
    spans = soup.findAll('span', class_="yt-badge-live")
    if spans:
        # At least one stream is live
        h3 = soup.find('h3', class_="yt-lockup-title")
        videourl = h3.findChild('a').attrs['href']
        return "https://youtube.com" + videourl

    return None


def main():
    procs = []
    for stream in spacestreams:
        livestream = livestream_url(stream)
        if livestream:
            print('Launching ', 'mpv', livestream)
            proc = subprocess.Popen(['mpv', '--really-quiet', livestream],
                                    stdin=None, stdout=None, stderr=None,
                                    close_fds=True)
            procs.append(proc)
    if procs:
        sys.exit(0)
    else:
        print('No streams currently live')

if __name__ == "__main__":
    main()
