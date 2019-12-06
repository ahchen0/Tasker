import tkinter as tk

class TaskerStatusBar(tk.Frame):
    """
    Status bar for Tasker GUI. Displays the time for which the orbits on the map is currently displayed

    :param Application master: Parent class (should be an Application)
    :param int width: Width of status bar
    """
    
    def __init__(self, master, width = 500):
        tk.Frame.__init__(self, master)
        self.statusbar = tk.Text(self, width = width, height = 1);
        self.statusbar.insert(tk.END, "Time Plotted: " + str(master.time))
        self.subscribers = []
        self.size = 32
        self.statusbar.pack(side="bottom", fill=tk.X, expand=False)
        self.statusbar.config(state=tk.DISABLED)

    def update(self, newTime):
        """
        Changes the map to a new time and displays the new time in the status bar

        :param datetime newTime: New time to change to
        """
        self.statusbar.config(state=tk.NORMAL)
        self.master.time = newTime
        self.statusbar.delete("1.0", tk.END)
        self.statusbar.insert(tk.END, "Time Plotted: " + str(newTime))
        self.statusbar.config(state=tk.DISABLED)

    def event_subscribe(self, obj_ref):
        """
        Subscribes obj_ref to the TaskerGui.

        :param obj_ref: object to be subscribed to TaskerGui
        """

        self.subscribers.append(obj_ref)

    def event_publish(self, cmd):
        """
        Publishes an event to all subscribers

        :param str cmd: Command to be published
        """

        for sub in self.subscribers:
            self.event_receive(cmd)

    def event_receive(self, cmd):
        """
        Receives an event from a subscription

        :param event: The event received from a subscription
        """

        pass

    def on_resize_parent(self, event):
        """
        Called when app is resized.
        """

        self.statusbar.config(width = event.width, height = 2)

    def on_resize_parentx(self, event):
        """
        Called only by Panedwindow to resize in x-dir only.
        """
        self.statusbar.config(width = event.width, height = 2)

