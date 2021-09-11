import tkinter as tk



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
        self.entry_box = tk.Text(self, height=1, font='Verdana, 10', bg='#FFFFFF'); self.entry_box.pack()
        self.entry_box.bind('<Return>', self.dummy_function)
        self.entry_box.bind("<Control-Key-a>", self.select_all)
        if default_val:
            self.entry_box.insert(tk.END, default_val)
        
    def select_all(self, event):
        self.entry_box.tag_add(tk.SEL, "1.0", tk.END)
        self.entry_box.mark_set(tk.INSERT, "1.0")
        self.entry_box.see(tk.INSERT)
        return 'break'
            
    def dummy_function(self, event):  # disable return on text widget
        return 'break'


class Mainframe(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        title_label = tk.Label(self, text="Ytrake", font='Verdana, 30 bold'); title_label.pack()
        version_label = tk.Label(self, text="{}".format(self.master.VERSION), font='Verdana, 10 bold'); version_label.pack()
        license_label = tk.Label(self, text="Project distributed under MIT license", font='Verdana, 8 bold'); license_label.pack()
        github_label = Hyperlink(self, url="https://github.com/jakedolan443/ytrake", text="https://github.com/jakedolan443/ytrake"); github_label.pack()
        
        space = tk.Label(self); space.pack(pady=5)
        
        playlist_field = Entrybox(self, title="Playlist URL"); playlist_field.pack(pady=5)
        save_directory = Entrybox(self, title="Save Directory", default_val="/home/retro"); save_directory.pack(pady=5)










class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self); self.geometry("640x640"); self.tk_setPalette(background="#DDDDDD")
        self.VERSION = "v1.0"
        Mainframe(self).pack(fill='both', expand=True, padx=25, pady=25)
        self.mainloop()
