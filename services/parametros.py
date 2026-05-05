import json
import os

ARQUIVO = "data/parametros.json"

def salvar_parametros(fator):
    if not os.path.exists("data"):
        os.makedirs("data")

    with open(ARQUIVO, "w") as f:
        json.dump({"fator": fator}, f)

def carregar_parametros():
    if not os.path.exists(ARQUIVO):
        return {"fator": 1}

    with open(ARQUIVO, "r") as f:
        return json.load(f)