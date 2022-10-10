import AF
import sys
import os

def lerAF(arquivo):
  arquivo = open(arquivo, 'r')
  arquivo_linhas = arquivo.readlines()
  arquivo_linhas = [linhas.rstrip("\n") for linhas in arquivo_linhas]

  estados        = int(arquivo_linhas[0])
  estado_inicial = int(arquivo_linhas[1])
  estados_finais = set(int(i) for i in arquivo_linhas[2].split(','))
  alfabeto       = set(arquivo_linhas[3].split(','))
  transicoes     = list()
  for linha in range(4, len(arquivo_linhas)):
    transicao = arquivo_linhas[linha].split(',')
    if (len(transicao[2]) > 1) :
        for i in transicao[2].split('-'):
            transicoes.append([int(transicao[0]), transicao[1], int(i)])
    else:
        transicoes.append([int(transicao[0]), transicao[1], int(transicao[2])])
  automato = AF.AF(estados, estado_inicial, estados_finais, alfabeto, transicoes)
  #automato.imprimirAF()
  return automato

def lerER(arquivo):
  arquivo = open(arquivo, 'r')
  arquivo_linhas = arquivo.readlines()
  for linha in arquivo_linhas:
    definicoes = linha.split(':')[0]
    expressoes = linha.split(':')[1]

def uniaoAutomato(automatos) -> AF:
    estados = 1
    alfabeto = set()
    estados_finais = set()
    transicoes = list()
    
    for automato in automatos:
        alfabeto = alfabeto.union(automato.alfabeto)
        aux = [0, '&', automato.estado_inicial + estados]
        transicoes.append((aux))

        for estado_final in automato.estados_finais:
            estados_finais.add(estado_final + estados)

        for transicao in automato.transicoes:
            transicoes.append([transicao[0] + estados, transicao[1], transicao[2] + estados])

    estados += automato.estados
    automato = AF.AF(estados, 0, estados_finais, alfabeto, transicoes)
    
    return automato




a1 = lerAF(sys.argv[1])
a2 = lerAF(sys.argv[2])
a3 = uniaoAutomato([a1, a2])
a3.imprimirAF()
