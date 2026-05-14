import tkinter as tk
import matplotlib.pyplot as plt

from styles.styles import CORES, FONTES, construir_cabecalho
from services.storage import carregar_historico
from services.calculo import calcular_emergia


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
        canvas = tk.Canvas(
            pai,
            bg=CORES["fundo"],
            highlightthickness=0
        )

        barra = tk.Scrollbar(
            pai,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(yscrollcommand=barra.set)

        barra.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        interno = tk.Frame(canvas, bg=CORES["fundo"])
        janela = canvas.create_window((0, 0), window=interno, anchor="nw")

        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(janela, width=e.width)
        )

        interno.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

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
            sombra,
            bg=CORES["superficie"],
            highlightbackground=CORES["borda"],
            highlightthickness=1,
        )
        card.pack(fill="x", padx=3, pady=3)

        interno = tk.Frame(card, bg=CORES["superficie"])
        interno.pack(fill="x", padx=16, pady=12)

        topo = tk.Frame(interno, bg=CORES["superficie"])
        topo.pack(fill="x")

        tk.Label(
            topo,
            text=f"#{indice}",
            bg=CORES["superficie"],
            fg=CORES["texto_suave"],
            font=FONTES["pequena"],
        ).pack(side="left")

        area_direita = tk.Frame(topo, bg=CORES["superficie"])
        area_direita.pack(side="right")

        botao_grafico = tk.Button(
            area_direita,
            text="📊",
            command=lambda historico_item=item: self.plotar_historico(historico_item),
            bg=CORES["fundo"],
            fg=CORES["destaque"],
            activebackground=CORES["borda"],
            activeforeground=CORES["destaque"],
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 12, "bold"),
            padx=8,
            pady=2,
        )
        botao_grafico.pack(side="left", padx=(0, 10))

        tk.Label(
            area_direita,
            text=f"Emergia: {round(item['resultado'], 4)}",
            bg=CORES["superficie"],
            fg=CORES["destaque"],
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")

        tk.Frame(
            interno,
            bg=CORES["borda"],
            height=1
        ).pack(fill="x", pady=(8, 8))

        rodape = tk.Frame(interno, bg=CORES["superficie"])
        rodape.pack(fill="x")

        entrada_txt = ", ".join(map(str, item.get("entrada", [])))
        transf_txt = ", ".join(map(str, item.get("transformidade", [])))

        tk.Label(
            rodape,
            text=f"Entrada: {entrada_txt}",
            bg=CORES["superficie"],
            fg=CORES["texto_suave"],
            font=FONTES["pequena"],
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            rodape,
            text=f"Transformidade: {transf_txt}",
            bg=CORES["superficie"],
            fg=CORES["texto_suave"],
            font=FONTES["pequena"],
            anchor="w",
        ).pack(fill="x")

        return sombra

    def plotar_historico(self, item):
        try:
            matriz = item.get("matriz")
            entrada = item.get("entrada")
            transformidade = item.get("transformidade")

            if not matriz or not entrada or not transformidade:
                raise Exception("Dados insuficientes para gerar o gráfico deste histórico.")

            emergia, fluxo = calcular_emergia(
                matriz,
                entrada,
                transformidade
            )

            plt.figure(facecolor=CORES["fundo"])
            plt.bar(
                range(len(fluxo)),
                fluxo,
                color=CORES["destaque"]
            )

            plt.title(
                f"Fluxo Emergético - Histórico #{round(item.get('resultado', emergia), 4)}",
                color=CORES["primaria"]
            )

            plt.xlabel("Processos")
            plt.ylabel("Fluxo")
            plt.tight_layout()
            plt.show()

        except Exception as e:
            self._mostrar_erro_grafico(str(e))

    def _mostrar_erro_grafico(self, mensagem):
        janela = tk.Toplevel(self)
        janela.title("Erro ao gerar gráfico")
        janela.configure(bg=CORES["fundo"])
        janela.resizable(False, False)

        conteudo = tk.Frame(janela, bg=CORES["fundo"])
        conteudo.pack(padx=28, pady=22)

        tk.Label(
            conteudo,
            text="⚠️",
            bg=CORES["fundo"],
            fg=CORES["perigo"],
            font=("Segoe UI", 28),
        ).pack(pady=(0, 8))

        tk.Label(
            conteudo,
            text="Não foi possível gerar o gráfico",
            bg=CORES["fundo"],
            fg=CORES["texto"],
            font=("Segoe UI", 12, "bold"),
        ).pack()

        tk.Label(
            conteudo,
            text=mensagem,
            bg=CORES["fundo"],
            fg=CORES["texto_suave"],
            font=FONTES["pequena"],
            wraplength=360,
        ).pack(pady=(8, 16))

        tk.Button(
            conteudo,
            text="Fechar",
            command=janela.destroy,
            bg=CORES["destaque"],
            fg="white",
            activebackground=CORES["destaque"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=6,
        ).pack()

    def _estado_vazio(self, pai):
        centro = tk.Frame(pai, bg=CORES["fundo"])
        centro.pack(expand=True)

        tk.Label(
            centro,
            text="📭",
            bg=CORES["fundo"],
            fg=CORES["texto_suave"],
            font=("Segoe UI", 40),
        ).pack(pady=(0, 12))

        tk.Label(
            centro,
            text="Nenhum cálculo encontrado",
            bg=CORES["fundo"],
            fg=CORES["texto"],
            font=("Segoe UI", 13, "bold"),
        ).pack()

        tk.Label(
            centro,
            text="Realize um cálculo para vê-lo aqui.",
            bg=CORES["fundo"],
            fg=CORES["texto_suave"],
            font=FONTES["pequena"],
        ).pack(pady=(4, 0))

    def voltar(self):
        from views.home import Home
        self.master.show_frame(Home)