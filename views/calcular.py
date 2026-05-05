import tkinter as tk
from tkinter import filedialog
from services.calculo import calcular_emergia
from services.storage import salvar_historico
import matplotlib.pyplot as plt
import numpy as np

class CalcularView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Cálculo Emergético", font=("Arial", 14)).pack(pady=10)

        tk.Label(self, text="Matriz (ex: 0.1,0.2;0.3,0.1)").pack()
        self.matriz = tk.Entry(self, width=50)
        self.matriz.pack()

        tk.Label(self, text="Entrada (ex: 100,50)").pack()
        self.entrada = tk.Entry(self)
        self.entrada.pack()

        tk.Label(self, text="Transformidade (ex: 2,3)").pack()
        self.transformidade = tk.Entry(self)
        self.transformidade.pack()

        tk.Button(self, text="Calcular", command=self.calcular).pack(pady=10)
        tk.Button(self, text="Mostrar Fluxo (Gráfico)", command=self.plotar).pack()
        tk.Button(self, text="Importar Completo", command=self.importar_completo).pack(pady=5)

        tk.Button(self, text="Voltar", command=self.voltar).pack(pady=10)

        self.resultado = tk.Label(self, text="")
        self.resultado.pack()

        self.fluxo = None

    def voltar(self):
        from views.home import Home
        self.master.show_frame(Home)

    def parse_matriz(self, texto):
        return [list(map(float, l.split(","))) for l in texto.split(";")]

    def calcular(self):
        try:
            matriz = self.parse_matriz(self.matriz.get())
            entrada = list(map(float, self.entrada.get().split(",")))
            transformidade = list(map(float, self.transformidade.get().split(",")))

            emergia, fluxo = calcular_emergia(matriz, entrada, transformidade)

            self.fluxo = fluxo

            salvar_historico({
                "matriz": matriz,
                "entrada": entrada,
                "transformidade": transformidade,
                "resultado": float(emergia)
            })

            self.resultado.config(
                text=f"Emergia: {round(emergia,2)}\nFluxo: {[round(v,2) for v in fluxo]}"
            )

        except Exception as e:
            self.resultado.config(text=f"Erro: {str(e)}")

    def plotar(self):
        try:
            if self.fluxo is None:
                self.resultado.config(text="Faça um cálculo primeiro")
                return

            plt.figure()
            plt.bar(range(len(self.fluxo)), self.fluxo)
            plt.title("Fluxo Emergético")
            plt.xlabel("Processos")
            plt.ylabel("Fluxo")
            plt.show()

        except Exception:
            self.resultado.config(text="Erro ao gerar gráfico")

    
    def importar_completo(self):
        from tkinter import filedialog

        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo completo",
            filetypes=[("Arquivos de texto", "*.txt"), ("CSV", "*.csv")]
        )

        if not arquivo:
            return

        try:
            with open(arquivo, "r") as f:
                linhas = f.readlines()

            secao = None
            matriz = []
            entrada = []
            transformidade = []

            for linha in linhas:
                linha = linha.strip()

                if not linha:
                    continue

                if linha.upper() == "[A]":
                    secao = "A"
                    continue
                elif linha.upper() == "[F]":
                    secao = "F"
                    continue
                elif linha.upper() == "[T]":
                    secao = "T"
                    continue

                linha = linha.replace(";", ",")

                valores = [float(v.strip()) for v in linha.split(",") if v.strip()]

                if secao == "A":
                    matriz.append(valores)
                elif secao == "F":
                    entrada.extend(valores)
                elif secao == "T":
                    transformidade.extend(valores)

            # 🔒 validações
            if not matriz:
                raise Exception("Matriz [A] não encontrada")

            if not entrada:
                raise Exception("Entrada [f] não encontrada")

            if not transformidade:
                raise Exception("Transformidade [T] não encontrada")

            tamanho = len(matriz[0])

            for linha in matriz:
                if len(linha) != tamanho:
                    raise Exception("Matriz inválida")

            if len(entrada) != tamanho:
                raise Exception("Entrada incompatível com matriz")

            if len(transformidade) != tamanho:
                raise Exception("Transformidade incompatível")

            # joga na tela
            texto_matriz = ";".join([",".join(map(str, l)) for l in matriz])

            self.matriz.delete(0, tk.END)
            self.matriz.insert(0, texto_matriz)

            self.entrada.delete(0, tk.END)
            self.entrada.insert(0, ",".join(map(str, entrada)))

            self.transformidade.delete(0, tk.END)
            self.transformidade.insert(0, ",".join(map(str, transformidade)))

            self.resultado.config(text="Arquivo completo importado ✔")

        except Exception as e:
            self.resultado.config(text=f"Erro: {str(e)}")