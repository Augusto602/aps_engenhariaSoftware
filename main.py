import tkinter as tk
from views.home import Home

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Emergético")
        self.geometry("700x500")
        self.frame = None
        self.show_frame(Home)

    def show_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()