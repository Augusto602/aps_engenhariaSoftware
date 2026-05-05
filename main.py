import tkinter as tk
from styles.styles import CORES
from views.home import Home


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Emergético")
        self.geometry("700x500")
        self.minsize(600, 400)
        self.configure(bg=CORES["fundo"])
        self._centralizar(700, 500)
        self.frame = None
        self.show_frame(Home)

    def _centralizar(self, largura, altura):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - largura) // 2
        y = (sh - altura) // 2
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def show_frame(self, classe_frame):
        novo_frame = classe_frame(self)
        if self.frame:
            self.frame.destroy()
        self.frame = novo_frame
        self.frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()