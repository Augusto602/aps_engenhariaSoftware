import tkinter as tk
from styles.styles import CORES, FONTES, construir_cabecalho, construir_botao
from views.calcular import CalcularView
from views.historico import HistoricoView


class Home(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=CORES["fundo"])
        self._construir_ui(master)

    def _construir_ui(self, master):
        construir_cabecalho(self, "⚡ Sistema Emergético")

          # Boas-vindas
        tk.Label(
            self, text="⚡",
            bg=CORES["fundo"], fg=CORES["destaque"],
            font=("Segoe UI", 48),
        ).pack(pady=(32, 4))

        tk.Label(
            self, text="Bem-vindo ao Sistema Emergético",
            bg=CORES["fundo"], fg=CORES["texto"],
            font=("Segoe UI", 16, "bold"),
        ).pack()

        tk.Label(
            self, text="Selecione uma opção para continuar",
            bg=CORES["fundo"], fg=CORES["texto_suave"],
            font=FONTES["pequena"],
        ).pack(pady=(4, 8))

        # Linha divisória
        tk.Frame(self, bg=CORES["borda"], height=1).pack(fill="x", padx=60, pady=(0, 24))

        area_botoes = tk.Frame(self, bg=CORES["fundo"])
        area_botoes.pack()

        self._card_nav(
            area_botoes,
            icone="⚙",
            rotulo="Calcular",
            descricao="Realize um novo cálculo emergético",
            destaque=True,
            ao_clicar=lambda: master.show_frame(CalcularView),
        ).pack(pady=(0, 14))

        self._card_nav(
            area_botoes,
            icone="📋",
            rotulo="Histórico",
            descricao="Veja os cálculos anteriores",
            destaque=False,
            ao_clicar=lambda: master.show_frame(HistoricoView),
        ).pack()

    def _card_nav(self, pai, icone, rotulo, descricao, ao_clicar, destaque=False):
        fundo        = CORES["destaque"] if destaque else CORES["primaria"]
        fundo_hover  = "#00796B"         if destaque else "#455A64"
        fundo_sombra = "#00695C"         if destaque else "#37474F"
        texto_desc   = "#B2DFDB"         if destaque else "#CFD8DC"

        moldura = tk.Frame(pai, bg=fundo_sombra)
        moldura.pack_propagate(False)
        moldura.config(width=340, height=72)

        btn = tk.Frame(moldura, bg=fundo, cursor="hand2")
        btn.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(
            btn, text=icone,
            bg=fundo, fg="#FFFFFF",
            font=("Segoe UI", 22), width=3,
        ).pack(side="left", padx=(12, 0))

        area_texto = tk.Frame(btn, bg=fundo)
        area_texto.pack(side="left", padx=10, fill="y", expand=True)

        lbl_titulo = tk.Label(
            area_texto, text=rotulo,
            bg=fundo, fg="#FFFFFF",
            font=("Segoe UI", 12, "bold"), anchor="w",
        )
        lbl_titulo.pack(anchor="w", pady=(14, 0))

        lbl_desc = tk.Label(
            area_texto, text=descricao,
            bg=fundo, fg=texto_desc,
            font=FONTES["pequena"], anchor="w",
        )
        lbl_desc.pack(anchor="w")

        lbl_seta = tk.Label(
            btn, text="›",
            bg=fundo, fg="#FFFFFF",
            font=("Segoe UI", 22), padx=16,
        )
        lbl_seta.pack(side="right")

        todos = [btn, area_texto, lbl_titulo, lbl_desc, lbl_seta]

        def _entrar(e):
            for w in todos:
                try: w.config(bg=fundo_hover)
                except: pass

        def _sair(e):
            for w in todos:
                try: w.config(bg=fundo)
                except: pass

        for w in todos:
            w.bind("<Enter>",    _entrar)
            w.bind("<Leave>",    _sair)
            w.bind("<Button-1>", lambda e: ao_clicar())

        return moldura