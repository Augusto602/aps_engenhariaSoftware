import json
import os

ARQUIVO = "data/historico.json"

def salvar_historico(dado):
    if not os.path.exists("data"):
        os.makedirs("data")

    historico = []

    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r") as f:
                historico = json.load(f)
        except:
            historico = []

    historico.append(dado)

    with open(ARQUIVO, "w") as f:
        json.dump(historico, f, indent=4)

def carregar_historico():
    if not os.path.exists(ARQUIVO):
        return []

    with open(ARQUIVO, "r") as f:
        return json.load(f)