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


#Asking for all the video links
n = int(input("Enter the number of youtube videos to download:   "))
links=[]
print("\nEnter all the links one per line:")

for i in range(0,n):
    temp = input()
    links.append(temp)

#Showing all details for videos and downloading them one by one
for i in range(0,n):
    link = links[i]
    # yt = YouTube(link)
    yt=YouTube(link,on_progress_callback=on_progress)
    print("\nDetails for Video",i+1,"\n")
    print("Title of video:   ",yt.title)
    print("Number of views:  ",yt.views)
    print("Length of video:  ", convert_seconds(yt.length), " (", yt.length, "seconds)")

    temp = yt.streams #.filter(progressive=True)
    # print(temp)
    stream = str(temp)
    stream = stream[1:]
    stream = stream[:-1]
    streamlist = stream.split(", ")

    print("\nAll available options for downloads:\n")
    for i in range(0,len(streamlist)):
        st = streamlist[i].split(" ")
        # print(i+1,") ",st[1]," and ",st[3],sep='')
        for feature in st:
            print(feature, end=" ")
        print()
    
    tag = int(input("\nEnter the itag of your preferred stream to download:   "))
    ys = yt.streams.get_by_itag(tag)
    print("\nDownloading...")
    output_path = input("Enter your preferred output path:   ")
    filename = input("Enter the file name: (type 'default' if you want to use the default name)   ")
    if filename == "default":
        filename = yt.title
    ys.download(output_path=output_path, filename=filename)
    print("\nDownload completed!!")
    print()
