import tkinter as tk
from views.calcular import CalcularView
from views.historico import HistoricoView

class Home(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Sistema Emergético", font=("Arial", 18)).pack(pady=30)

        tk.Button(self, text="Calcular",
                  command=lambda: master.show_frame(CalcularView)).pack(pady=10)

        tk.Button(self, text="Histórico",
                  command=lambda: master.show_frame(HistoricoView)).pack(pady=10)