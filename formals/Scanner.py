import sys
import os
from dataclasses import dataclass, field
from RE import RE
from RE import RE
from FA import FA


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
    automata = FA(states, alphabet, initial, final_states, transitions)
    # automato.imprimirAF()
    return automata


def readER(arquivo) -> RE:
    arquivo = open(arquivo, "r")
    arquivo_linhas = arquivo.readlines()
    arquivo_linhas = [linhas.rstrip("\n") for linhas in arquivo_linhas]
    definitions = list()
    for linha in arquivo_linhas:
        definition = linha.split(": ")[0]
        expression = linha.split(": ")[1]
        definitions.append((definition, expression))
    return RE(definition)


def automataUnion(automatas: list[FA]) -> FA:
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

    automata = FA(states, alphabet, 0, final_states, transitions)

    return automata


@dataclass
class Scanner:
    token_recognizer: FA = field(init=False)
    token_table: list[tuple[str, int]] = field(default_factory=list)
    lexemas_table: list[str] = field(default_factory=list)

    def __post__init__(self, patterns):

        # Gera os regex de patterns
        read_patterns = list()
        for pattern in patterns:
            read_patterns.append(readER(pattern))

        # Gera os automatos das regex
        automatas = list()
        for read_pattern in read_patterns:
            automatas += read_pattern.generateFAs()

        # for automata in automatas:
        #   automata.minimizeFA()

        # Gera o reconhecedor de tokens a partir dos automatos
        automata = automataUnion(automatas)
        self.token_recognizer = automata.determinizeFA()

        # le o source text com os automatos

    def run(self, source_text):
        entry = source_text

        while len(source_text) >= 0:
            result = self.token_recognizer.run(entry)

            token = result[0]
            self.token_table.append((token, len(self.lexemas_table)))

            lexema = result[1]
            self.lexemas_table.append(lexema)

            entry = result[2]

    def clearTables(self):
        self.token_table = list()
        self.lexemas_table = list()

    # TODO def writeTablesToFiles():


# a1 = readFA(sys.argv[1])
# a2 = lerAF(sys.argv[2])
# a3 = uniaoAutomato([a1, a2])
# a3.imprimirAF()
# lerER(sys.argv[1])
# a1.printFA()
# a1.determinizeFA()
# a1.minimizeFA()
# a1.printFA()
