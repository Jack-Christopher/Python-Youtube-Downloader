import re
import unicodedata
from pytube import YouTube
from pytube.cli import on_progress

def convert_seconds(seconds):
    units = ["seconds", "minutes", "hours", "days"]
    temp = None

    if seconds < 0:
        return None
    duration = [0, 0, 0, 0]

   # days
    temp = seconds // 86400 # 86400 seconds in a day
    duration[3] = temp
    # hours
    temp = (seconds % 86400) // 3600 # 3600 seconds in an hour
    duration[2] = temp
    # minutes
    temp = (seconds % 3600) // 60 # 60 seconds in a minute
    duration[1] = temp
    # seconds
    temp = (seconds % 60)
    duration[0] = temp

    duration_to_string = ""
    for i in range(len(duration)-1, -1, -1):
        if duration[i] == 1:
            duration_to_string += str(duration[i]) + " " + units[i][:-1] + ", "
        elif duration[i] != 0:
            duration_to_string += str(duration[i]) + " " + units[i] + ", "
    return duration_to_string[:-2]


def download_video(yt, tag, output_path, filename, ext):
    ys = yt.streams.get_by_itag(tag)
    if filename == "":
        filename = yt.title
    filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    filename = re.sub(r'[^\w\s-]', '', filename.lower())
    filename = re.sub(r'[-\s]+', '-', filename).strip('-_')
    filename = filename + "." + ext
    ys.download(output_path=output_path, filename=filename)

