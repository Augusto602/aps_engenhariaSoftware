from services.calculo import calcular_emergia

matriz = [
    [0.1, 0.2],
    [0.3, 0.1]
]

entrada = [100, 50]
transformidade = [2, 3]

emergia, fluxo = calcular_emergia(matriz, entrada, transformidade)

print("Fluxo:", fluxo)
print("Emergia:", emergia)