import AF
import sys
import os

def lerAF(arquivo):
  arquivo = open(arquivo, 'r')
  arquivo_linhas = arquivo.readlines()
  estados        = int(arquivo_linhas[0])
  estado_inicial = int(arquivo_linhas[1])
  estados_finais = set(arquivo_linhas[2].split(','))
  alfabeto       = set(arquivo_linhas[3].split(','))
  transicoes     = list()
  for linha in range(4, len(arquivo_linhas)):
    transicoes.append(arquivo_linhas[linha].split(','))
  automato = AF.AF(estados, estado_inicial, estados_finais, alfabeto, transicoes)
  automato.imprimirAF()

def lerER(arquivo):
  arquivo = open(arquivo, 'r')
  arquivo_linhas = arquivo.readlines()
  for linha in arquivo_linhas:
    definicoes = linha.split(':')[0]
    expressoes = linha.split(':')[1]


lerAF(sys.argv[1])