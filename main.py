# from tkinter import *
from tkinter import Tk, Menu, mainloop, messagebox, ttk, Toplevel, Label, Entry, font, Button, Frame, IntVar, Radiobutton, Scrollbar, Canvas, StringVar, filedialog
from tkinter.ttk import Progressbar
from pytube import YouTube
from threading import Thread
from yt import convert_seconds, download_video

class App(Tk):
    def __init__(self):
        super().__init__()

        self.title('Youtube Downloader')
        window_width, window_height, position_right, position_top = self.get_geometry_data()
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.window_width = window_width
        self.window_height = window_height

        self.menubar = Menu(self, background='#dddddd', foreground='black', activebackground='white', activeforeground='black')  

        file = Menu(self.menubar, tearoff=0, background='#dddddd')  
        file.add_command(label="New", command=self.new)
        file.add_separator()  
        file.add_command(label="Exit", command=self.quit)  
        self.menubar.add_cascade(label="File", menu=file)  
        help = Menu(self.menubar, tearoff=0, background='#dddddd')
        help.add_command(label="About", command=self.about)  
        self.menubar.add_cascade(label="Help", menu=help)  
        self.config(menu=self.menubar)

        self.progressbar = Progressbar(
            self, 
            orient='horizontal',
            length=280
        )
        self.progressbar.pack()
        self.type = StringVar()

        self.main_frame = Frame(
            self, 
            bg='#A8B9BF', 
            width=self.window_width,
            height=self.window_height
        )
        self.main_frame.pack(expand=True, fill="both")


        # self.links = []
        self.current_link = None
        self.option = IntVar()
        self.ext =""
        self.categories = {}
        self.yt_title = ""
        self.duration = ""
        self.current_percentage = 0

    def get_geometry_data(self):
        # get the screen size of your computer
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # calculate a suitable size for your window
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.7)
        # Get the window position from the top dynamically
        position_top = int((screen_height- window_height)/4)
        position_right = int((screen_width - window_width)/2)

        return window_width, window_height, position_right, position_top 


    def about(self):
        self.mssg_box = messagebox.showinfo('Youtube Downloader',
            'Youtube Downloader v1.0.0\n\nCreated by: Jack Christopher\n\nCopyright (c) 2022')

    def new(self):
        self.add_link_window = Toplevel(self)
        self.add_link_window.title("Enter Link")
        self.add_link_window.geometry("500x150")
        Label(self.add_link_window, text ="Enter the Youtube Link: ").pack()
        link = Entry(self.add_link_window, width = 50, font=font.Font(family="Courier", size=10) )
        link.pack()
        Radiobutton(self.add_link_window, text="Solo Audio", variable=self.type, value="audio").pack()
        Radiobutton(self.add_link_window, text="Solo Video", variable=self.type, value="video").pack()
        Radiobutton(self.add_link_window, text="Audio and Video", variable=self.type, value="audio_video").pack()
        Button(self.add_link_window, text = "Add Link", command= lambda: self.add_link(link)).pack()
    
    def add_link(self, link):
        link = link.get()
        if link == "":
            return
        self.add_link_window.destroy()
        self.main_frame.destroy()
        self.main_frame = Frame(
            self, 
            bg='#A8B9BF', 
            width=self.window_width,
            height=self.window_height
        )
        self.main_frame.pack(expand=True, fill="both", side="left")


        self.yt, self.yt_title, self.duration, self.categories = self.get_stream_data(link)
        Label(
            self.main_frame, 
            bg='#A8B9BF',
            text= self.yt_title + self.duration 
        ).pack()
        
        Label(
            self.main_frame, 
            bg='#A8B9BF',
            text=(self.type.get()).replace("_", " and ").capitalize()+":"
        ).pack()

        for stream in self.categories[self.type.get()]:
            text = ""
            if self.type.get() == "audio":
                text = "type: " + stream['mime_type'] + ", abr: " + stream['abr'] + ", audio codec: " + stream['acodec']
            elif self.type.get() == "video":
                text = "type: " + stream['mime_type'] + ", resolution: " + stream['res'] + ", fps: " + stream['fps'] + ", video codec: " + stream['vcodec']
            elif self.type.get() == "audio_video":
                text = "type: " + stream['mime_type'] + ", resolution: " + stream['res'] + ", fps: " + stream['fps'] + ", video codec: " + stream['vcodec'] + ", audio codec: " + stream['acodec']

            Radiobutton(
                self.main_frame, 
                bg='#A8B9BF',
                text=text, 
                variable=self.option, 
                value=stream['itag'], 
                # command= self.download with lambda function and thread
                command= lambda: Thread(target=self.download).start()

            ).pack()
        
    def download(self):
        # ask for directory to save to
        self.output_path = filedialog.askdirectory()
        self.filename = ""
        itag = self.option.get()
        for category in self.categories:
            for stream in self.categories[category]:
                if int(stream['itag']) == itag:
                    self.ext = stream['mime_type'].split('/')[1]

        download_video(self.yt, itag, self.output_path, self.filename, self.ext)



    def progress_function(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        p = round((1- (float(bytes_remaining) / float(size))) * float(100), 1)
        # print (str(p)+'% (', bytes_remaining , ' bytes remaining)')
        self.progressbar.step(p - self.current_percentage)
        self.current_percentage = p
        

    def completed_function(self, stream, filepath):
        self.download_complete_window = Toplevel(self)
        self.download_complete_window.title("Download Complete")
        self.download_complete_window.geometry("200x100")
        Label(self.download_complete_window, text ="Download Complete!").pack()
        Button(self.download_complete_window, text = "OK", command= self.download_complete_window.destroy).pack()
        self.current_percentage = 0
        # print("\nDownload Complete")

    def get_stream_data(self, link):
        # Default progress bar
        # yt=YouTube(link, on_progress_callback=on_progress)
        yt=YouTube(link, on_progress_callback=self.progress_function, on_complete_callback=self.completed_function)
        title = "Title:   " + yt.title + "\n"
        duration = "Length:  " + convert_seconds(yt.length) + " ( " + str(yt.length) + " seconds )\n"


        stream_list = yt.streams
        # remove brackets from the stream_list and split it into a list
        stream_list = str(stream_list)[1:-1].split(", ")

        categories = { "audio": [], "video": [], "audio_video":[] }

        current_category = None
        for i in range(len(stream_list)):
            # remove initial and final brackets from the stream_list
            temp = stream_list[i][1:-1]
            if "acodec" in temp and "vcodec" in temp:
                current_category = "audio_video"
            elif "acodec" in temp:
                current_category = "audio"
            elif "vcodec" in temp:
                current_category = "video"
            temp = temp.replace("\"", "").split(" ")[1:]
            temp = {k: v for k, v in (x.split("=") for x in temp)}
            categories[current_category].append(temp)

        return yt, title, duration, categories


if __name__ == "__main__":
    app = App()
    app.mainloop()
