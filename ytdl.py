import sys
import json
import string
import urllib.request
import urllib.parse
import json
import subprocess

import pdb

def get_searchable_string(s):
    """Returns a new string with all the punctuations and offensive words
    removed, so that the new string is friendly for a search operation."""
    offensive_chars = string.punctuation
    offensive_words = ['song']
    for ch in offensive_chars:
        s = s.replace(ch, ' ')
    for word in offensive_words:
        s = s.replace(word, ' ')
    s = ' '.join(s.split())
    return s

def test_get_searchable_string():
    s = "song: Calvin Harris - My Way (Official Video)"
    expected = "Calvin Harris My Way Official Video"
    actual = get_searchable_string(s)
    assert actual == expected

def get_songs_list(filename):
    """Return as a list the songs listed in a text file; each song should be on
    a single line and different songs should be separated by at least one
    newline. Given, filename which has the list of songs."""
    file = open(filename, 'r')
    songs_list = []
    for line in file:
        if line == '\n':
            continue
        songs_list.append(get_searchable_string(line))
    file.close()
    return songs_list

if __name__ == '__main__':
    config_filename = 'config.json'
    songs_filename = ''
    HTTP_PROXY = ''
    API_KEY = ''

    if len(sys.argv) != 2:
        print('Usage: ytdl.py <songs.txt>')
        sys.exit(0)

    songs_filename = sys.argv[1]

    config_data = {}
    with open(config_filename, 'r') as f:
        config_data = json.load(f)
    if 'HTTP_PROXY' in config_data:
        HTTP_PROXY = config_data['HTTP_PROXY']
    API_KEY = config_data['API_KEY']

    # TODO
    # check_network()geturl
    
    for song in get_songs_list(songs_filename):
        queries = {
            "key": API_KEY,
            "part": "snippet",
            "maxResults": "1",
            "q": song,
            "type": "video"
        }
        query_string = urllib.parse.urlencode(queries)
        url = "https://www.googleapis.com/youtube/v3/search?" + query_string
        # response = urllib.request.urlopen("https://www.google.com/")
        response = urllib.request.urlopen(url)
        # pdb.set_trace()
        # sys.exit(0)
        if response.getcode() != 200:
            print('GET ', response.geturl(), 'returned a', response.getcode())
            sys.exit(1)
        # if response
        response_dict = json.loads(response.read().decode('utf-8'))
        res = response_dict
        # print (res['items'][0]['snippet']['title'])
        # print(res['items'][0]['id']['videoId'])
        # print('')

        url = "https://www.youtube.com/watch?v=" + res['items'][0]['id']['videoId']
        print('Title:', res['items'][0]['snippet']['title'])
        print('Url:', url)

        ffmpeg_path = ""
        if sys.platform == "win32":
            ffmpeg_path = r"libav\win64\usr\bin"
        else:
            ffmpeg_path = "libav/win64/usr/bin"

        subprocess.call([
            "ytdl",
            "--proxy", HTTP_PROXY,
            "--abort-on-error",
            "--socket-timeout", "30",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--max-filesize", "20m",
            "--retries", "3",
            "--ffmpeg-location", ffmpeg_path,
            "--output", "%(title)s.%(ext)s",
            "--restrict-filenames",
            url
            ],
            shell=True)

        print("")
        

# https://www.youtube.com/watch?v=R0Avu3v9a8w

# ytdl --proxy <HTTP_PROXY> --abort-on-error --socket-timeout "30" -x --audio-format "mp3" --max-filesize "20m" --retries "3" --ffmpeg-location "libav\win64\usr\bin" <url>
# --audio-quality

# part=snippet
# maxResults
# q
# type=video

# %load_ext autoreload
# %autoreload 2

# res = response.read().decode('utf-8')

# Video URL part
# ['items'][0]['id']['videoId']

# Video Title
# ['items'][0]['snippet']['title']