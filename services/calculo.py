import numpy as np

def calcular_emergia(matriz, entrada, transformidade):
    A = np.array(matriz, dtype=float)
    f = np.array(entrada, dtype=float)
    T = np.array(transformidade, dtype=float)

    # validações
    if A.shape[0] != A.shape[1]:
        raise Exception("Matriz deve ser quadrada")

    if len(f) != A.shape[0]:
        raise Exception("Entrada incompatível com matriz")

    if len(T) != A.shape[0]:
        raise Exception("Transformidade incompatível")

    I = np.eye(len(A))
    
    inversa = np.linalg.inv(I - A)


    x = inversa.dot(f)

    emergia = T.dot(x)

    return emergia, x