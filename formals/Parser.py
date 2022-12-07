from dataclasses import dataclass, field
from formals.GM import GM, FrozenGM
import sys
import os


def closure(item, symbol, productions, noterminals):

    heads_to_be_inserted = list()
    heads_to_be_inserted.append(symbol)

    i = 0
    while i < len(heads_to_be_inserted):
        for production in productions:
            if production[0] == heads_to_be_inserted[i]:
                item.append(production)
                symbol_being_read = production[1][production[1].index(".") + 1]

                if (
                    symbol_being_read not in heads_to_be_inserted
                    and symbol_being_read in noterminals
                ):
                    heads_to_be_inserted.append(symbol_being_read)

        i += 1

    return item


def indexBodies(symbols: list(), bodies, shift):

    # Seleciona um símbolo de uma lista de símbolos
    for symbol_index in range(len(symbols)):
        symbol = symbols[symbol_index]

        # Seleciona um corpo de produção
        for body in bodies:
            body_index = bodies.index(body)

            # Itera pelos elementos do corpo
            for element in body:

                # Procura o símbolo
                if symbol in element:
                    element_index = body.index(element)

                    # Salva as duas porções do corpo entre o símbolo a ser substituído
                    saved_slice_begin = body[:element_index]
                    saved_slice_end = body[element_index + 1 :]

                    # Quebra o corpo na posição do símbolo
                    splited_element = element.split(symbol)

                    # Substitui o símbolo pelo seu respectivo índice
                    last_position = len(splited_element) - 1
                    for i in range(last_position, 0, -1):
                        splited_element.insert(i, str(symbol_index + shift))

                    # Une as porções salvas com o índice entre elas
                    splited_element = (
                        saved_slice_begin + splited_element + saved_slice_end
                    )

                    # Remove espaços em branco gerados ao quebrar o corpo
                    while "" in splited_element:
                        splited_element.remove("")

                    # Atualiza o corpo na lista de corpos
                    bodies[body_index] = splited_element

    return bodies


def indexProductions(noterminals: list(), terminals: list(), marked_productions):

    # Separa as produções em cabeça e corpos
    heads = list()
    bodies = list()
    # Converte os corpos de produção de strings para listas de strings
    for (_, body) in marked_productions:
        bodies.append([body])

    # Seleciona um não terminal
    for noterminal_index in range(len(noterminals)):
        noterminal = noterminals[noterminal_index]

        # Substitui as cabeças pelos seus respectivos índices
        for (head, _) in marked_productions:
            if head == noterminal:
                heads.append(noterminal_index)

    # Substitui nos corpos das produções, os não terminais pelos seus respectivos índices
    bodies = indexBodies(noterminals, bodies, 0)

    # Substitui nos corpos das produções, os terminais pelos seus respectivos índices
    bodies = indexBodies(terminals, bodies, len(noterminals))

    # Converte os índices dentro das produções de string para inteiro
    for body in bodies:
        body_index = bodies.index(body)

        for element in body:
            element_index = body.index(str(element))

            if element.isnumeric():
                element = int(element)
                body[element_index] = element

        bodies[body_index] = body

    """Junta as cabeças com seus respectivos corpos
    e converte as produções de listas para tuplas"""
    indexed_productions = list()
    for i in range(len(marked_productions)):
        indexed_productions.append((heads[i], bodies[i]))

    return indexed_productions


def markProductions(grammar):

    # Marca as produções com um ponto
    marked_productions = list()
    for head, body in grammar.productions.items():
        unmarked_productions = list(body)
        for production in unmarked_productions:
            if "." not in production:
                marked_production = "." + production
                marked_productions.append(tuple(head, marked_production))

    return marked_productions


def newInitialProduction(grammar):

    # Acrescenta um novo símbolo inicial
    initial = grammar.initial + "▶️"

    return (initial, grammar.initial)


@dataclass
class ParserSLR:

    grammar_reference: FrozenGM() = field(init=False)

    canonical_items: list[list[tuple[int, list[str | int]]]] = field(init=False)
    go_to_table: list[tuple[int, str, int]] = field(init=False)

    slr_table_terminals: list[list[tuple[str, int]]] = field(init=False)
    slr_table_noterminals: list[list[int]] = field(init=False)

    def __post__init__(self, grammar):
        self.generateSLRParser(grammar)

    def goTo(self, item, symbol):

        new_productions = list()
        for production in item:
            new_production = tuple()
            body = list(production[1])
            dot_index = body.index(".")

            symbol_being_read = body[dot_index + 1]
            if symbol_being_read == symbol:
                body.remove(".")
                body.insert(dot_index + 1, ".")
                new_body = "".join(body)
                new_production = (production[0], new_body)
                new_productions.append(new_production)

        return new_productions

    def extendGrammar(self, grammar):

        # Cria nova produção com o novo símbolo inicial
        new_initial_production = newInitialProduction(grammar)
        new_initial_noterminal = new_initial_production[0]

        # Acrescenta-o na lista de não terminais
        noterminals = [new_initial_noterminal] + list(grammar.noterminals)
        terminals = list(grammar.terminals)

        # Acrescenta a nova produção às produções
        productions = list()
        productions.append(new_initial_production)

        # Converte cada produção de itens de dicionário para tuplas
        for head in grammar.productions:
            for body in grammar.productions[head]:
                productions.append((head, body))

        # Cria uma gramática congelada
        self.grammar_reference = FrozenGM(
            noterminals, terminals, new_initial_noterminal, productions
        )

    def buildCanonicalItems(self):

        grammar = self.grammar_reference

        # Marca produções com um ponto
        marked_productions = markProductions(grammar)
        indexed_productions = indexProductions(
            grammar.terminals, grammar.noterminals, marked_productions
        )

        canonical_items = list()
        first_body = marked_productions[marked_productions.index(grammar.initial)][1]
        first_production = (grammar.initial, first_body)

        first_item = [first_production]
        symbol_being_read = first_body[first_body.index(".") + 1]
        if symbol_being_read in grammar.noterminals:
            new_item = closure(
                first_item, symbol_being_read, marked_productions, grammar.noterminals
            )
            canonical_items.append(new_item)
        go_tos = dict()
        for index in range(len(canonical_items)):
            go_to = []
            for production in canonical_items[index]:
                symbol_being_read = production[1][production[1].index(".") + 1]
                go_to = goTo(canonical_items[index], symbol_being_read)
                go_tos[(index, symbol_being_read)] = go_to

        # final

        # self.canonical_items = return

    def buildSLRTableTerminals(self):
        # Marcar os shifts
        markShifts(SLRTableTerminals)

        # Marcar os reduces
        markReduces(SLRTableTerminals)

        # Marcar o accept
        markAccept(SLRTableTerminals)

        # Calcular os follows
        follows = calculateFollows(extended_gm)

    def buildSLRTableNonTerminals(self):
        # Marcar os desvios
        markGoTos(SLRTableNonTerminals)

    def generateSLRParser(self, grammar):

        # Estende a gramática e a congela
        self.extendGrammar(grammar)

        # Construir itens canônicos (automato)
        self.buildCanonicalItems()

        # Contruir tabela SLR
        self.buildSLRTableTerminals()
        self.buildSLRTableNonTerminals()

        # Demais entradas na tabela são erros

        # Estado inicial é o que contém a produção pelo símbolo inicial da gramática estendida
