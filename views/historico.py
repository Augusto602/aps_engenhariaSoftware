import tkinter as tk
from styles.styles import CORES, FONTES, construir_cabecalho
from services.storage import carregar_historico


class HistoricoView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=CORES["fundo"])
        self._construir_ui()

    def _construir_ui(self):
        construir_cabecalho(self, "📋 Histórico", ao_voltar=self.voltar)

        corpo = tk.Frame(self, bg=CORES["fundo"])
        corpo.pack(fill="both", expand=True, padx=40, pady=24)

        historico = carregar_historico()

        if not historico:
            self._estado_vazio(corpo)
        else:
            self._construir_lista(corpo, historico)

    def _construir_lista(self, pai, historico):
        canvas = tk.Canvas(pai, bg=CORES["fundo"], highlightthickness=0)
        barra = tk.Scrollbar(pai, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=barra.set)

        barra.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        interno = tk.Frame(canvas, bg=CORES["fundo"])
        janela = canvas.create_window((0, 0), window=interno, anchor="nw")

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(janela, width=e.width))
        interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        def _scroll(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        def _bind_scroll(widget):
            """Propaga o scroll para o widget e todos os seus filhos."""
            widget.bind("<MouseWheel>", _scroll)
            for filho in widget.winfo_children():
                _bind_scroll(filho)

        for i, item in enumerate(reversed(historico), 1):
            card = self._card_historico(interno, i, item)
            card.pack(fill="x", pady=(0, 10))
            _bind_scroll(card)

        canvas.bind("<MouseWheel>", _scroll)
        interno.bind("<MouseWheel>", _scroll)

    def _card_historico(self, pai, indice, item):
        sombra = tk.Frame(pai, bg=CORES["sombra"])
        sombra.pack(fill="x")

        card = tk.Frame(
            sombra, bg=CORES["superficie"],
            highlightbackground=CORES["borda"],
            highlightthickness=1,
        )
        card.pack(fill="x", padx=3, pady=3)

        interno = tk.Frame(card, bg=CORES["superficie"])
        interno.pack(fill="x", padx=16, pady=12)

        topo = tk.Frame(interno, bg=CORES["superficie"])
        topo.pack(fill="x")

        tk.Label(
            topo, text=f"#{indice}",
            bg=CORES["superficie"], fg=CORES["texto_suave"],
            font=FONTES["pequena"],
        ).pack(side="left")

        tk.Label(
            topo, text=f"Emergia: {round(item['resultado'], 4)}",
            bg=CORES["superficie"], fg=CORES["destaque"],
            font=("Segoe UI", 11, "bold"),
        ).pack(side="right")

        tk.Frame(interno, bg=CORES["borda"], height=1).pack(fill="x", pady=(8, 8))

        rodape = tk.Frame(interno, bg=CORES["superficie"])
        rodape.pack(fill="x")

        entrada_txt = ", ".join(map(str, item.get("entrada", [])))
        transf_txt  = ", ".join(map(str, item.get("transformidade", [])))

        tk.Label(
            rodape, text=f"Entrada: {entrada_txt}",
            bg=CORES["superficie"], fg=CORES["texto_suave"],
            font=FONTES["pequena"], anchor="w",
        ).pack(fill="x")

        tk.Label(
            rodape, text=f"Transformidade: {transf_txt}",
            bg=CORES["superficie"], fg=CORES["texto_suave"],
            font=FONTES["pequena"], anchor="w",
        ).pack(fill="x")

        return sombra

    def _estado_vazio(self, pai):
        centro = tk.Frame(pai, bg=CORES["fundo"])
        centro.pack(expand=True)

        tk.Label(
            centro, text="📭",
            bg=CORES["fundo"], fg=CORES["texto_suave"],
            font=("Segoe UI", 40),
        ).pack(pady=(0, 12))

        tk.Label(
            centro, text="Nenhum cálculo encontrado",
            bg=CORES["fundo"], fg=CORES["texto"],
            font=("Segoe UI", 13, "bold"),
        ).pack()

        tk.Label(
            centro, text="Realize um cálculo para vê-lo aqui.",
            bg=CORES["fundo"], fg=CORES["texto_suave"],
            font=FONTES["pequena"],
        ).pack(pady=(4, 0))

    def voltar(self):
        from views.home import Home
        self.master.show_frame(Home)