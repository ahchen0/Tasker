import tkinter as tk

class TaskerStatusBar(tk.Frame):
    
    def __init__(self, master, width = 500):
        tk.Frame.__init__(self, master)
        self.statusbar = tk.Text(self, width = width, height = 1);
        self.statusbar.insert(tk.END, "Time Plotted: " + str(master.time))
        self.subscribers = []
        self.size = 32
        self.statusbar.pack(side="bottom", fill=tk.X, expand=False)
        self.statusbar.config(state=tk.DISABLED)

    def update(self, newTime):
        self.statusbar.config(state=tk.NORMAL)
        self.master.time = newTime
        self.statusbar.delete("1.0", tk.END)
        self.statusbar.insert(tk.END, "Time Plotted: " + str(newTime))
        self.statusbar.config(state=tk.DISABLED)

    def event_subscribe(self, obj_ref):
        self.subscribers.append(obj_ref)

    def event_publish(self, cmd):
        for sub in self.subscribers:
            self.event_receive(cmd)

    def event_receive(self, cmd):
        pass

    def on_resize_parent(self, event):
        self.statusbar.config(width = event.width, height = 2)

    def on_resize_parentx(self, event):
        self.statusbar.config(width = event.width, height = 2)

