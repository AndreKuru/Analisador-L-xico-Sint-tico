from dataclasses import dataclass, field
from formals.GM import GM, FrozenGM
import sys
import os

MARK_POINTER = "·"
END_OF_SENTENCE = "$"


def indexBodies(symbols: list(), bodies: list(), shift: int):

    # Seleciona um símbolo de uma lista de símbolos
    for symbol_index in range(len(symbols)):
        symbol = symbols[symbol_index]

        # Seleciona um corpo de produção
        for body_index in range(len(bodies)):
            body = bodies[body_index]

            # Itera pelos elementos do corpo
            for element_index in range(len(body)):
                element = body[element_index]

                # Procura o símbolo
                if type(element) == str and symbol in element:
                    # Salva as duas porções do corpo entre o símbolo a ser substituído
                    saved_slice_begin = body[:element_index]
                    saved_slice_end = body[element_index + 1 :]

                    # Quebra o corpo na posição do símbolo
                    splited_element = element.split(symbol)

                    # Substitui o símbolo pelo seu respectivo índice
                    last_position = len(splited_element) - 1
                    for i in range(last_position, 0, -1):
                        splited_element.insert(i, symbol_index + shift)

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


def newInitialProduction(grammar):
    # Acrescenta um novo símbolo inicial
    initial = grammar.initial + "▶️"

    return (initial, grammar.initial)


def indexProductions(noterminals, terminals, marked_productions):

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

    """Junta as cabeças com seus respectivos corpos
    e converte as produções de listas para tuplas"""
    indexed_productions = list()
    for i in range(len(marked_productions)):
        indexed_productions.append((heads[i], bodies[i]))

    return indexed_productions

def extendGrammar(grammar):

    # Cria nova produção com o novo símbolo inicial
    new_initial_production = newInitialProduction(grammar)
    new_initial_noterminal = new_initial_production[0]

    # Acrescenta-o na lista de não terminais
    noterminals = [new_initial_noterminal] + list(grammar.noterminals)
    terminals = list(grammar.terminals) + [END_OF_SENTENCE]

    # Acrescenta a nova produção às produções
    productions = list()
    productions.append(new_initial_production)

    # Converte cada produção de itens de dicionário para tuplas
    for head in grammar.productions:
        for body in grammar.productions[head]:
            # Marca produções com um ponto e com o símbolo de final de sentença
            productions.append((head, MARK_POINTER + body + END_OF_SENTENCE))

    indexed_productions = indexProductions(productions)
    # Cria uma gramática congelada
    return FrozenGM(
        noterminals, terminals, new_initial_noterminal, indexed_productions
    )

def closure(initial_production, total_columns, productions):
    # Inicialização
    canonical_item = [initial_production]
    canonical_item_index = 0
    read_symbols = set()

    while canonical_item_index < canonical_item:

        # Busca o símbolo de marcação
        symbol = 0
        while canonical_item[canonical_item_index][1][symbol] != MARK_POINTER:
            symbol += 1

        # Verifica se o símbolo logo depois do de marcação é um não terminal
        # e está sendo lido pela primeira
        read_symbol = canonical_item[canonical_item_index][1][symbol + 1]
        if read_symbol < len(total_columns) and read_symbol not in read_symbols:
            read_symbols.add(read_symbol)

        # Pega todas as produções do símbolo lido
        for production in productions:
            if read_symbol == production[0]:
                canonical_item.append(production)

        canonical_item_index += 1

def lookAhead(canonical_item: list()):
    new_canonical_item = list()
    for (head, body) in canonical_item:
        pointer_index = body.index(MARK_POINTER)
        new_body = body.copy()
        new_body.remove(MARK_POINTER)
        new_body.insert(pointer_index + 1)
        new_production = (head, new_body)
        new_canonical_item.append(new_production)

    return new_canonical_item

def separate_canonical_items_by_symbol(canonical_items):
    # Vasculha todos os itens
    new_canonical_items = dict(canonical_items)
    canonical_item_index = 0
    while canonical_item_index < canonical_items:
        production = canonical_items[canonical_item_index]

        # Busca o símbolo de marcação
        symbol = 0
        while production[1][symbol] != MARK_POINTER:
            symbol += 1

        # Separa a produção por símbolo lido
        read_symbol = production[1][symbol + 1]
        if read_symbol not in new_canonical_items:
            new_canonical_items[read_symbol] = [production]
        else:
            new_canonical_items[read_symbol].append(production)

        canonical_item_index += 1

    return new_canonical_items

def goto(canonical_item: list()) -> list():
    # Move o pointeiro
    canonical_item_looked_ahead = lookAhead(canonical_item)

    # Adquiri o closure
    canonical_item_looked_ahead_closure = closure(canonical_item_looked_ahead)

    return canonical_item_looked_ahead_closure

def initializeSLRTable(total_canonical_items, total_columns, row_content):
    table = list()
    for _ in range(total_canonical_items):
        row = list()
        for _ in range(total_columns):
            row.append(row_content)
        table.append(row)

    return table



@dataclass
class ParserSLR:

    grammar_reference: FrozenGM(
        list[str], list[str], str, list[tuple[int, list[int | str]]]
    ) = field(init=False)

    canonical_items: list[list[tuple[int, list[str | int]]]] = field(init=False)
    go_to_table: list[tuple[int, int, int]] = field(init=False)

    firsts: list[set[int]] = field(init=False)
    firsts_untouched: set[int] = field(init=False)
    firsts_in_use: set[int] = field(init=False)

    follows: list[set[int]] = field(init=False)
    follows_shared_from: set[int] = field(init=False)

    slr_table_terminals: list[list[tuple[str, int]]] = field(init=False)
    slr_table_noterminals: list[list[int]] = field(init=False)

    def __post__init__(self, grammar):
        self.generateSLRParser(grammar)

    def getIndexEndOfSentence(self):
        return (
            len(self.grammar_reference.noterminals)
            + len(self.grammar_reference.terminals)
            - 1
        )


    def buildCanonicalItems(self):

        canonical_item_initial = self.grammar_reference.productions[0]
        closure(
            canonical_item_initial,
            self.grammar_reference.noterminals,
            self.grammar_reference.productions,
        )
        new_canonical_item = goto(canonical_item_initial)
        new_canonical_items = separate_canonical_items_by_symbol(new_canonical_item)


    def markShifts(go_to_table, buildSLRTableTerminals):

        for go_to in go_to_table:
            canonical_item_origin_index = go_to[0]
            terminal_index = go_to[1]
            canonical_item_destination_index = go_to[2]
            shift = ("s", canonical_item_destination_index)
            buildSLRTableTerminals[canonical_item_origin_index][
                terminal_index
            ] = shift
        return buildSLRTableTerminals

    def calculateFirst(self, noterminal, productions, epslon):
        if noterminal in self.firsts_untouched:
            self.firsts_untouched.remove(noterminal)

        if noterminal in self.firsts_in_use:
            print("Error")
        self.firsts_in_use.add(noterminal)

        # Vasculha todas as produções do não terminal selecionado
        for production in productions[noterminal]:

            # Vasculha cada símbolo até um terminal ou não terminal não anulável
            # ignorando o ponto de marcação
            index = 1
            while True:
                symbol = production[index]

                # Se símbolo for não terminal
                if symbol < len(self.grammar_reference.noterminal) or symbol == epslon:
                    self.calculateFirst(symbol, productions, epslon)
                    self.first[noterminal] = self.firsts[noterminal].union(
                        self.firsts[symbol]
                    )

                    # Dispensa a produção atual caso tenha chego ao fim ou se nem todos os símbolos até o atual são anuláveis
                    index += 1
                    if index >= len(productions) or epslon not in self.firsts[symbol]:
                        break

                # Se símbolo for terminal
                else:
                    self.firsts[noterminal].add(symbol)

        self.firsts_in_use.remove(noterminal)

    def calculateFirsts(self):
        # Inicializa os firsts
        self.firsts = list()
        self.firsts_untouched = set()
        self.firsts_in_use = set()
        productions = list()
        for index in range(len(self.grammar_reference.noterminals)):
            self.firsts.append(set())
            productions.append(list())
            self.firsts_untouched.add(index)

        for (head, body) in self.grammar_reference.productions:
            productions[head].append(body)

        epslon = self.grammar_reference.terminals.index("&")

        # Preenche os firsts dos terminais
        for index in range(len(self.grammar_reference.terminals)):
            self.firsts.append(set(index))

        # Preenche os firsts dos não terminais que ainda não foram preenchidos
        for index in range(len(self.grammar_reference.noterminals)):
            if index not in self.firsts_untouched:
                self.calculateFirst(index, productions, epslon)

    def updateFollow(
        self, follows_index: int, follows_content: set, follows_opened: list()
    ):
        if follows_index in follows_opened:
            print("Error")
        follows_opened.append(follows_opened)

        self.follows[follows_index] = self.follows[follows_index].union(follows_content)

        for shared in self.follows_shared_from[follows_index]:
            self.updateFollow(shared, follows_content)

    def calculateFollow(self, noterminal, productions, epslon):
        # Vasculha todas as produções do não terminal selecionado
        for production in productions[noterminal]:

            # Vasculha cada símbolo até um terminal ou não terminal não anulável
            # ignorando o ponto de marcação
            # começando do último símbolo antes do símbolo de final de sentença
            index = len(production) - 2
            # Repete até chegar no segundo símbolo, pois o primeiro é o ponto de marcação
            while index > 0:
                symbol = production[index]
                previous_symbol = productions[index - 1]

                # Checa se o elemento atual tem firsts não anulável
                firsts_from_symbol_not_nullable = self.firsts[symbol] - {epslon}
                if firsts_from_symbol_not_nullable > 0:
                    self.updateFollow(previous_symbol, self.firsts[symbol], list())

                # Checa se o elemento atual é noterminals
                if symbol < len(self.grammar_reference.noterminals):
                    self.follows_shared_from[noterminal].add(symbol)
                    self.updateFollow(symbol, self.follows[noterminal], list())

                # Símbolo consegue ser anulável
                if epslon in self.firsts[symbol]:
                    index -= 1

    def calculateFollows(self):

        # Inicializa os follows
        self.follows = list()
        productions = list()
        for index in range(len(self.grammar_reference.noterminals)):
            self.follows.append(set())
            productions.append(list())

        for (head, body) in self.grammar_reference.productions:
            productions[head].append(body)

        epslon = self.grammar_reference.terminals.index("&")

        # Adiciona o símbolo de final de sentença ao follow do símbolo inicial
        self.follows[0].add(self.getIndexEndOfSentence())

        # Preenche os follows dos não terminais que ainda não foram preenchidos
        for index in range(len(self.grammar_reference.noterminals)):
            if index not in self.follows_untouched:
                self.calculateFollow(index, productions, epslon)

    def buildSLRTableTerminals(self):
        # Initialize a tabela de terminais com o formato e tamanho certo
        slr_table_terminals = initializeSLRTable(len(self.canonical_items), len(self.grammar_reference.terminals), ("", None))

        # Marcar os shifts
        self.markShifts(slr_table_terminals)

        self.calculateFirsts()
        self.calculateFollows()

        # # Marcar os reduces
        # markReduces(SLRTableTerminals)

        # # Marcar o accept
        # markAccept(SLRTableTerminals)

    def buildSLRTableNonTerminals(self):
        # Initialize a tabela de não terminais com o formato e tamanho certo
        slr_table_noterminals = initializeSLRTable(len(self.canonical_items), len(self.grammar_reference.noterminals), None)

        # # Marcar os desvios
        # markGoTos(SLRTableNonTerminals)

    def generateSLRParser(self, grammar):

        # Estende a gramática e a congela
        self.grammar_reference = extendGrammar(grammar)

        # Construir itens canônicos (automato)
        self.buildCanonicalItems()

        # Contruir tabela SLR
        self.buildSLRTableTerminals()
        self.buildSLRTableNonTerminals()

        # Demais entradas na tabela são erros

        # Estado inicial é o que contém a produção pelo símbolo inicial da gramática estendida
