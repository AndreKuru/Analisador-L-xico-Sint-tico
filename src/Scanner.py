import FA
import sys
import os

def readFA(arquivo):
  arquivo = open(f'tests/{arquivo}', 'r')
  arquivo_linhas = arquivo.readlines()
  arquivo_linhas = [linhas.rstrip("\n") for linhas in arquivo_linhas]

  states       = int(arquivo_linhas[0])
  initial      = int(arquivo_linhas[1])
  final_states = set(int(i) for i in arquivo_linhas[2].split(','))
  alphabet     = set(arquivo_linhas[3].split(','))
  transitions  = list()
  for linha in range(4, len(arquivo_linhas)):
    transition = arquivo_linhas[linha].split(',')
    if (len(transition[2]) > 1) :
        for i in transition[2].split('-'):
            transitions.append([int(transition[0]), transition[1], int(i)])
    else:
        transitions.append([int(transition[0]), transition[1], int(transition[2])])
  automata = FA.FA(states, initial, final_states, alphabet, transitions)
  #automato.imprimirAF()
  return automata

def readER(arquivo):
  arquivo = open(arquivo, 'r')
  arquivo_linhas = arquivo.readlines()
  definitions = list()
  expressions = list()
  for linha in arquivo_linhas:
    definitions.append(linha.split(': ')[0])
    expressions.append(linha.split(': ')[1])
  print(f"Definições: {definitions}")
  print(f"Expressões: {expressions}")

def determinizeFA(automata) -> FA:

  # 1 - Varrer transicoes em busca de transicoes pelo simbolo de palavra vazia

  # 1.1 - Calcula os e-fechos do automato original
  e_closures = dict()
  # 1.1.1 - Adiciona o proprio estado ao seu e-fecho 
  for i in range(automata.states):
    e_closure = set()
    e_closure.add(i)
    e_closure_aux = e_closure.copy()
    e_closures[i] = e_closure_aux
    e_closure.clear()

  # 1.1.2 - Adiciona demais estados alcançados por e-transicoes
  for transition in automata.transitions:
    if '&' in transition:
      e_closure = set()
      e_closure_aux = e_closure.union(e_closures[transition[0]])
      e_closure_aux = e_closure_aux.union(e_closures[transition[2]])
      e_closure_aux = e_closures[transition[0]].union(e_closure_aux)
      e_closures[transition[0]] = e_closure_aux
      e_closure.clear()

  key_states = list(e_closures)

  new_states = dict()
  for i in range(automata.states):
    if {key_states[i]} == e_closures[i]:
      new_states[i] = e_closures[i]
    else:  
      new_states[i + automata.states - 1] = e_closures[i]

  print('ESTADOS NOVOS MAPEADOS')
  print(new_states)

  '''1.3 - Define o e-fecho do estado inicial do automato original
        como estado inicial do automato resultante'''

  initial = key_states[0]

  '''1.4 - Define os conjuntos de estados que contem algum estado final do automato
        original como estados finais do automato resultante'''
  
  final_states = dict()

  for (index, state) in new_states.items():
    for final_state in automata.final_states:
      if final_state in state:
        final_states[index] = state

  # 1.5 - As novas transicoes passam a ser a união dos e-fecho de cada transicao do estado novo

  alphabet_aux = automata.alphabet.copy()
  transitions = list()
  for state in new_states.values():
    for sign in alphabet_aux:
      transitions.append([state, sign, set()])

  for transition in automata.transitions:
    for i in range(len(transitions)):
      
      if transition[0] in transitions[i][0] and transition[1] == transitions[i][1]:
        transitions[i][2] = transitions[i][2].union(e_closures[transition[2]])

  for (index, state) in new_states.items():
    for transition in transitions:
      if state == transition[0]:
        transition[0] = index
      if state == transition[2]:
        transition[2] = index

  DFA = FA.FA(len(new_states), initial, list(final_states), automata.alphabet, transitions)
  
  return DFA

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

def automataUnion(automatas) -> FA:
    states = 1
    # Estado inicial é sempre 0
    final_states = set()
    alphabet = set()
    transitions = list()
    
    for automata in automatas:
      alphabet = alphabet.union(automata.alphabet)
      aux = [0, '&', automata.initial + states]
      transitions.append((aux))

      for final_state in automata.final_states:
          final_states.add(final_state + states)

      for transition in automata.transitions:
          transitions.append([transition[0] + states, transition[1], transition[2] + states])

      states += automata.states

    automata = FA.FA(states, 0, final_states, alphabet, transitions)
    
    return automata




a1 = readFA(sys.argv[1])
#a2 = lerAF(sys.argv[2])
#a3 = uniaoAutomato([a1, a2])
#a3.imprimirAF()
#lerER(sys.argv[1])
a4 = determinizeFA(a1)
a4.printFA()