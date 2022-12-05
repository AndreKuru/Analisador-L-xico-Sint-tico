import FA
import sys
import os


def readFA(arquivo):
    arquivo = open(f"tests/{arquivo}", "r")
    arquivo_linhas = arquivo.readlines()
    arquivo_linhas = [linhas.rstrip("\n") for linhas in arquivo_linhas]

    states = int(arquivo_linhas[0])
    initial = int(arquivo_linhas[1])
    final_states = {"token_generic": set(int(i) for i in arquivo_linhas[2].split(","))}
    alphabet = set(arquivo_linhas[3].split(","))
    transitions = list()
    for linha in range(4, len(arquivo_linhas)):
        transition = arquivo_linhas[linha].split(",")
        if len(transition[2]) > 1:
            for i in transition[2].split("-"):
                transitions.append((int(transition[0]), transition[1], int(i)))
        else:
            transitions.append((int(transition[0]), transition[1], int(transition[2])))
    automata = FA.FA(states, alphabet, initial, final_states, transitions)
    # automato.imprimirAF()
    return automata


def readER(arquivo):
    arquivo = open(arquivo, "r")
    arquivo_linhas = arquivo.readlines()
    definitions = list()
    expressions = list()
    for linha in arquivo_linhas:
        definitions.append(linha.split(": ")[0])
        expressions.append(linha.split(": ")[1])
    print(f"Definições: {definitions}")
    print(f"Expressões: {expressions}")


def automataUnion(automatas) -> FA:
    states = 1
    # Estado inicial é sempre 0
    final_states = set()
    alphabet = set()
    transitions = list()

    for automata in automatas:
        alphabet = alphabet.union(automata.alphabet)
        aux = (0, "&", automata.initial + states)
        transitions.append((aux))

        for token in automata.final_states:
            for final_state in automata.final_states[token]:
                final_states[token].add(final_state + states)

        for transition in automata.transitions:
            transitions.append(
                (transition[0] + states, transition[1], transition[2] + states)
            )

        states += automata.states

    automata = FA.FA(states, alphabet, 0, final_states, transitions)

    return automata


a1 = readFA(sys.argv[1])
# a2 = lerAF(sys.argv[2])
# a3 = uniaoAutomato([a1, a2])
# a3.imprimirAF()
# lerER(sys.argv[1])
a1.printFA()
a1.determinizeFA()
a1.printFA()
