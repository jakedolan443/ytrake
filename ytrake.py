import tkinter as tk
import re
import subprocess
import threading
import time


class Hyperlink(tk.Label):
    def __init__(self, *args, url="", text=""):
        tk.Label.__init__(self, *args)
        
        self.url = url
        self.text = text
        if not text:
            self.text = self.url
            
        self.config(fg="blue", cursor="hand2", font='Verdana, 10', text="{}".format(self.text))
        self.bind("<Button-1>", lambda e: webbrowser.open_new(r"{}".format(url)))
        self.bind("<Enter>", lambda e: e.widget.config(font='System, 10 underline'))
        self.bind("<Leave>", lambda e: e.widget.config(font='System, 10'))


class Entrybox(tk.Frame):
    def __init__(self, *args, title="", default_val=False):
        tk.Frame.__init__(self, *args)
        title_label = tk.Label(self, text=title, font='Verdana, 10 italic'); title_label.pack(anchor='w')
        self.entry_box = tk.Text(self, height=1, font='Verdana, 10', bg='white'); self.entry_box.pack()
        self.entry_box.bind('<Return>', self.dummy_function)
        self.entry_box.bind("<Control-Key-a>", self.select_all)
        if default_val:
            self.entry_box.insert(tk.END, default_val)
    
    def get(self):
        return self.entry_box.get("1.0", tk.END)
        
    def select_all(self, event):
        self.entry_box.tag_add(tk.SEL, "1.0", tk.END)
        self.entry_box.mark_set(tk.INSERT, "1.0")
        self.entry_box.see(tk.INSERT)
        return 'break'
            
    def dummy_function(self, event):  # disable return on text widget
        return 'break'


def stream_process(process, stat_var=None):
    go = process.poll() is None
    old_line = ""
    for line in process.stdout:
        print(line.decode())
        if "Finished" in line.decode():
            old_line = "Finished."
            line = "Finished"
        stat_var.set(old_line)
        old_line = line
    return go

def download(playlist, save_dir, artist, album, stat_var):
    process = subprocess.Popen("".join(['youtube-dl --add-metadata --postprocessor-args "', "-metadata artist='{}' -metadata album='{}' -metadata album_artist='{}'".format(artist, album, artist), '" --extract-audio --audio-format best --yes-playlist "{}" -o "{}/'.format(playlist, save_dir),'%(title)s.%(ext)s"']), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while stream_process(process, stat_var=stat_var):
        time.sleep(0.001)
    

class Mainframe(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.status_var = tk.StringVar(); self.status_var.set("")
        title_label = tk.Label(self, text="Ytrake", font='Verdana, 30 bold'); title_label.pack()
        version_label = tk.Label(self, text="{}".format(self.master.VERSION), font='Verdana, 10 bold'); version_label.pack()
        license_label = tk.Label(self, text="Project distributed under MIT license", font='Verdana, 8 bold'); license_label.pack()
        github_label = Hyperlink(self, url="https://github.com/jakedolan443/ytrake", text="https://github.com/jakedolan443/ytrake"); github_label.pack()
        
        space = tk.Label(self); space.pack(pady=5)
        
        playlist_field = Entrybox(self, title="Playlist URL"); playlist_field.pack(pady=5)
        save_directory = Entrybox(self, title="Save Directory", default_val=str(__file__).split(str(__file__).split("/")[-1])[0]); save_directory.pack(pady=5)
        
        space = tk.Label(self); space.pack(pady=5)
        
        artist_name = Entrybox(self, title="Artist Name"); artist_name.pack(pady=5)
        album_name = Entrybox(self, title="Album Name"); album_name.pack(pady=5)
        
        download_button = tk.Button(self, text="Download", font='Verdana, 15 italic', width=15, command=lambda: self.__init_download(playlist=playlist_field.get(), save_dir=save_directory.get(), artist=artist_name.get(), album=album_name.get(), stat_var=self.status_var)); download_button.pack(anchor='w', pady=10)
        
        status_label = tk.Label(self, textvariable=self.status_var, font='Verdana, 10'); status_label.pack(anchor='w', pady=15)

    def __init_download(self, playlist="", save_dir="", artist="", album="", stat_var=None):
        artist, album = re.sub(r'[^\w]', ' ', artist), re.sub(r'[^\w]', ' ', album)
        playlist = playlist.replace("\n", ""); save_dir = save_dir.replace("\n", ""); artist = artist.replace("\n", ""); album = album.replace("\n", "")
        stat_var.set("downloading ...")
        threading.Thread(target=download, args=(playlist, save_dir, artist, album, stat_var, )).start()


        










class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self); self.geometry("640x640"); self.tk_setPalette(background="#DDDDDD")
        self.VERSION = "v1.0"
        Mainframe(self).pack(fill='both', expand=True, padx=25, pady=25)
        self.mainloop()



if __name__ == "__main__":
    App()
