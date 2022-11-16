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
  definicoes = list()
  expressoes = list()
  for linha in arquivo_linhas:
    definicoes.append(linha.split(': ')[0])
    expressoes.append(linha.split(': ')[1])
  print(f"Definições: {definicoes}")
  print(f"Expressões: {expressoes}")

def determinizarAutomato(automato) -> AF:

  # 1 - Varrer transicoes em busca de transicoes pelo simbolo de palavra vazia

  # 1.1 - Calcula os e-fechos do automato original
  e_fechos = dict()
  # 1.1.1 - Adiciona o proprio estado ao seu e-fecho 
  for i in range(automato.estados):
    e_fecho = set()
    e_fecho.add(i)
    e_fecho_aux = e_fecho.copy()
    e_fechos[i] = e_fecho_aux
    e_fecho.clear()

  # 1.1.2 - Adiciona demais estados alcançados por e-transicoes
  for transicao in automato.transicoes:
    if '&' in transicao:
      e_fecho = set()
      e_fecho_aux = e_fecho.union(e_fechos[transicao[0]])
      e_fecho_aux = e_fecho_aux.union(e_fechos[transicao[2]])
      e_fecho_aux = e_fechos[transicao[0]].union(e_fecho_aux)
      e_fechos[transicao[0]] = e_fecho_aux
      e_fecho.clear()

  estados_chaves = list(e_fechos)

  estados_novos = dict()
  for i in range(automato.estados):
    if {estados_chaves[i]} == e_fechos[i]:
      estados_novos[i] = e_fechos[i]
    else:  
      estados_novos[i + automato.estados - 1] = e_fechos[i]

  print('ESTADOS NOVOS MAPEADOS')
  print(estados_novos)

  '''1.3 - Define o e-fecho do estado inicial do automato original
        como estado inicial do automato resultante'''

  estado_inicial = estados_chaves[0]

  '''1.4 - Define os conjuntos de estados que contem algum estado final do automato
        original como estados finais do automato resultante'''
  
  estados_finais = dict()

  for (index, estado) in estados_novos.items():
    for estado_final in automato.estados_finais:
      if estado_final in estado:
        estados_finais[index] = estado

  # 1.5 - As novas transicoes passam a ser a união dos e-fecho de cada transicao do estado novo

  alfabeto_aux = automato.alfabeto.copy()
  transicoes = list()
  for estado in estados_novos.values():
    for simbolo in alfabeto_aux:
      transicoes.append([estado, simbolo, set()])

  for transicao in automato.transicoes:
    for i in range(len(transicoes)):
      if transicao[0] in transicoes[i][0] and transicao[1] == transicoes[i][1]:
        transicoes[i][2] = transicoes[i][2].union(e_fechos[transicao[2]])

  for (index, estado) in estados_novos.items():
    for transicao in transicoes:
      if estado == transicao[0]:
        transicao[0] = index
      if estado == transicao[2]:
        transicao[2] = index

  automato_determinizado = AF.AF(len(estados_novos), estado_inicial, list(estados_finais), automato.alfabeto, transicoes)
  
  return automato_determinizado

  '''
  2 - Se nao
  
    2.1 - Gerar conjunto potencia do conjunto de estados do automato

    2.2 - Definir estado inicial

   2.3 - Gerar conjunto de estados finais

    2.4 - Gerar producoes

      2.4.1 - Para cada estado novo do conjunto potencia

      2.4.2 - Para cada simbolo do alfabeto

      2.4.3 - Adicionar producao ao conjunto de producoes,
            se nas transicoes originais existia uma transicao
            de um estado contido no estado novo pelo simbolo
  '''

  pass

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
#a2 = lerAF(sys.argv[2])
#a3 = uniaoAutomato([a1, a2])
#a3.imprimirAF()
#lerER(sys.argv[1])
a4 = determinizarAutomato(a1)
a4.imprimirAF()