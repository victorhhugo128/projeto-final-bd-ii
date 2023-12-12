from random import randint

def gerar_numero_cartao() -> int:
    conjuntos_numeros = []
    for conjunto in range(4):
        conjuntos_numeros.append([])
        for numero in range(4):
            conjuntos_numeros[conjunto].append(str(randint(0, 9)))
    numero_cartao = ""
    for conjunto in conjuntos_numeros:
        for numero in conjunto:
            numero_cartao += numero
    return int(numero_cartao)