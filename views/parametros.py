import tkinter as tk

class ParametrosView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Parâmetros", font=("Arial", 14)).pack(pady=10)

        tk.Label(self, text="(Pode expandir futuramente)").pack()

        tk.Button(self, text="Voltar", command=self.voltar).pack(pady=10)

    def voltar(self):
        from views.home import Home
        self.master.show_frame(Home)