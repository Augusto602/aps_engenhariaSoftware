import tkinter as tk
from services.storage import carregar_historico

class HistoricoView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Histórico", font=("Arial", 14)).pack(pady=10)

        historico = carregar_historico()

        for item in historico:
            tk.Label(self, text=f"Emergia: {round(item['resultado'],2)}").pack()

        tk.Button(self, text="Voltar", command=self.voltar).pack(pady=10)

    def voltar(self):
        from views.home import Home
        self.master.show_frame(Home)