import tkinter as tk
from tkinter import filedialog
from styles.styles import CORES, FONTES, construir_cabecalho, construir_card, construir_campo, construir_botao, construir_resultado, divisor
from services.calculo import calcular_emergia
from services.storage import salvar_historico
import matplotlib.pyplot as plt


class CalcularView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=CORES["fundo"])
        self.fluxo = None
        self._construir_ui()

    def _construir_ui(self):
        construir_cabecalho(self, "⚡ Cálculo Emergético", ao_voltar=self.voltar)

        corpo = tk.Frame(self, bg=CORES["fundo"])
        corpo.pack(fill="both", expand=True, padx=40, pady=24)

        interno = construir_card(corpo)
        self.matriz          = construir_campo(interno, "Matriz",         "ex: 0.1,0.2;0.3,0.1", largura=52)
        self.entrada         = construir_campo(interno, "Entrada",        "ex: 100,50")
        self.transformidade  = construir_campo(interno, "Transformidade", "ex: 2,3")

        divisor(corpo)

        linha_botoes = tk.Frame(corpo, bg=CORES["fundo"])
        linha_botoes.pack(fill="x", pady=16)

        acoes = [
            ("⚙  Calcular",          self.calcular,          True),
            ("📊  Mostrar Fluxo",     self.plotar,            False),
            ("📂  Importar Completo", self.importar_completo, False),
        ]

        for texto, cmd, destaque in acoes:
            construir_botao(linha_botoes, texto, cmd, destaque=destaque).pack(side="left", padx=(0, 10))

        self.resultado = construir_resultado(corpo)

    def _definir_resultado(self, texto, erro=False):
        self.resultado.config(
            text=texto,
            fg=CORES["perigo"] if erro else CORES["destaque"],
        )

    def voltar(self):
        from views.home import Home
        self.master.show_frame(Home)

    def _parse_matriz(self, texto):
        return [list(map(float, l.split(","))) for l in texto.split(";")]

    def calcular(self):
        try:
            matriz         = self._parse_matriz(self.matriz.get())
            entrada        = list(map(float, self.entrada.get().split(",")))
            transformidade = list(map(float, self.transformidade.get().split(",")))

            emergia, fluxo = calcular_emergia(matriz, entrada, transformidade)
            self.fluxo = fluxo

            salvar_historico({
                "matriz": matriz, "entrada": entrada,
                "transformidade": transformidade,
                "resultado": float(emergia),
            })

            self._definir_resultado(
                f"Emergia: {round(emergia, 2)}     Fluxo: {[round(v, 2) for v in fluxo]}"
            )
        except Exception as e:
            self._definir_resultado(f"Erro: {e}", erro=True)

    def plotar(self):
        if self.fluxo is None:
            self._definir_resultado("Faça um cálculo primeiro.", erro=True)
            return
        try:
            plt.figure(facecolor=CORES["fundo"])
            plt.bar(range(len(self.fluxo)), self.fluxo, color=CORES["destaque"])
            plt.title("Fluxo Emergético", color=CORES["primaria"])
            plt.xlabel("Processos"); plt.ylabel("Fluxo")
            plt.tight_layout(); plt.show()
        except Exception as e:
            self._definir_resultado(f"Erro ao gerar gráfico: {e}", erro=True)

    def importar_completo(self):
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=[("Texto", "*.txt"), ("CSV", "*.csv")]
        )
        if not arquivo:
            return
        try:
            with open(arquivo) as f:
                linhas = f.readlines()

            secao, matriz, entrada, transformidade = None, [], [], []

            for linha in linhas:
                linha = linha.strip()
                if not linha: continue
                if   linha.upper() == "[A]": secao = "A"; continue
                elif linha.upper() == "[F]": secao = "F"; continue
                elif linha.upper() == "[T]": secao = "T"; continue

                valores = [float(v) for v in linha.replace(";", ",").split(",") if v.strip()]
                if   secao == "A": matriz.append(valores)
                elif secao == "F": entrada.extend(valores)
                elif secao == "T": transformidade.extend(valores)

            if not matriz:         raise Exception("Matriz [A] não encontrada")
            if not entrada:        raise Exception("Entrada [F] não encontrada")
            if not transformidade: raise Exception("Transformidade [T] não encontrada")

            tamanho = len(matriz[0])
            if any(len(l) != tamanho for l in matriz): raise Exception("Matriz inválida")
            if len(entrada) != tamanho:                raise Exception("Entrada incompatível")
            if len(transformidade) != tamanho:         raise Exception("Transformidade incompatível")

            self.matriz.delete(0, tk.END)
            self.matriz.insert(0, ";".join([",".join(map(str, l)) for l in matriz]))
            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, ",".join(map(str, entrada)))
            self.transformidade.delete(0, tk.END)
            self.transformidade.insert(0, ",".join(map(str, transformidade)))

            self._definir_resultado("Arquivo importado com sucesso ✔")
        except Exception as e:
            self._definir_resultado(f"Erro: {e}", erro=True)