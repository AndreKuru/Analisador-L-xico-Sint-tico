from dataclasses import dataclass, field
from formals.GM import GM, FrozenGM
import sys
import os

MARK_POINTER = "·"
END_OF_SENTENCE = "$"


def readGM(file):
    file = open(f"tests/{file}", "r")
    file_rows = file.readlines()
    file_rows = [rows.rstrip("\n") for rows in file_rows]

    initial = str(file_rows[0][0])  # Producao inicial
    productions = dict()  # dicionario contendo todas as producoes
    # codigo responsável por ler a Gramatica e encontrar as producoes
    nopipe = []
    for i in range(len(file_rows)):
        file_one_row = file_rows[i].split(" -> ")
        nopipe = file_one_row[1].split(" | ")
        for body in nopipe:
            if file_one_row[0] not in productions:
                productions[file_one_row[0]] = {body}
            else:
                productions[file_one_row[0]].add(body)

    noterminals = set(
        file_rows[row][0] for row in range(0, len(file_rows))
    )  # conjunto de nao terminais da gramática

    # parte responsável por encontrar os não terminais da gramática
    new_fragments = []
    fragments = []
    # vare todas os values do dicionario e separa as producoes por "|"
    for k in productions.keys():
        fragments += productions[k]
    for production in fragments:
        new_fragments += production.split(" | ")
    fragments = new_fragments
    new_fragments = []
    # vare novamente a lista criada anteriormente e separa por todos os terminais para manter
    # somente os que são não terminais
    for noterminal in noterminals:
        for fragment in fragments:
            new_fragments += fragment.split(noterminal)
        fragments = new_fragments
        new_fragments = []

    while "" in fragments:
        fragments.remove("")
    terminals = set(fragments)

    return initial, productions, noterminals, terminals


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

    return (initial, MARK_POINTER + grammar.initial)


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

    indexed_productions = indexProductions(noterminals, terminals, productions)
    # Cria uma gramática congelada
    return FrozenGM(noterminals, terminals, new_initial_noterminal, indexed_productions)


def closure(
    canonical_item: list[tuple[int, list[int]]], noterminals, reference_productions
):
    # Inicialização
    canonical_item_index = 0
    read_symbols = set()

    while canonical_item_index < len(canonical_item):
        if canonical_item_index == 30:
            raise Exception("30")

        # Busca o símbolo de marcação
        symbol = 0
        body = canonical_item[canonical_item_index][1]
        while symbol < len(body) and body[symbol] != MARK_POINTER:
            symbol += 1

        if symbol >= len(body):
            raise Exception("Não encontra o " + MARK_POINTER)

        # Verifica se o símbolo logo depois do de marcação é um não terminal
        # e está sendo lido pela primeira
        read_symbol = body[symbol + 1]
        if read_symbol < len(noterminals) and read_symbol not in read_symbols:
            read_symbols.add(read_symbol)

            # Pega todas as produções do símbolo lido
            for production in reference_productions:
                if read_symbol == production[0]:
                    canonical_item.append(production)

        canonical_item_index += 1

    return canonical_item


# Move o ponteiro de todos as produções passadas no item canonico um para frente
# Caso algum ponteiro já esteja lendo o final da sentença retorna nulo
def lookAhead(canonical_item: list()):
    new_canonical_item = list()
    for (head, body) in canonical_item:
        pointer_index = body.index(MARK_POINTER)
        if pointer_index + 1 >= len(body):
            return None
        new_body = body.copy()
        new_body.remove(MARK_POINTER)
        new_body.insert(pointer_index + 1, MARK_POINTER)
        new_production = (head, new_body)
        new_canonical_item.append(new_production)

    return new_canonical_item


# Encontra a produção que lê o final de sentença
# retorna o índice dela relativo as produções de referência
def readCanonicalItemEndOfSentence(
    canonical_item: list(), reference_productions, end_of_sequence_index
) -> int:
    for production in canonical_item:
        body = production[1]
        pointer_index = body.index(MARK_POINTER)
        if body[pointer_index + 1] == end_of_sequence_index:
            production_hit = production
            production_hit[1].remove(MARK_POINTER)
            production_hit[1].insert(0, MARK_POINTER)
            return reference_productions.index(production_hit)
    return -1


def separate_canonical_items_by_symbol(canonical_items):
    # Vasculha todos os itens
    new_canonical_items = dict()
    canonical_item_index = 0
    while canonical_item_index < len(canonical_items):
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


def initializeSLRTable(total_canonical_items, total_columns, row_content):
    table = list()
    for _ in range(total_canonical_items):
        row = list()
        for _ in range(total_columns):
            row.append(row_content)
        table.append(row)

    return table


def mergeCanonicalItems(
    new_canonical_items: dict[str, set[tuple[str, list[int | str]]]],
    old_canonical_items: list[list[tuple[str, list[int | str]]]],
):
    # Pega um item novo
    for symbol in new_canonical_items:
        count = 0
        already_exists = False
        item_transitions = list()

        # Pega um item velho
        for canonical_item in old_canonical_items:

            # Pega uma produção das velhas nesse item velho específico
            for production in canonical_item:

                # Checa pra ver se está no item novo específico
                if production in new_canonical_items[symbol]:
                    # Conta
                    count += 1
                    break

            # Se der hit em todas as produções é porque é o mesmo item canônico
            if count == len(canonical_item):
                already_exists = True

        # Se comparar com todos os itens velhos e ainda não existir adiciona o novo item a lista
        if not already_exists:
            # Lista de transições index = origem, symbol = transição, destination = último item canonico mesclado
            item_transitions.append((symbol, len(old_canonical_items)))
            old_canonical_items.append(list(new_canonical_items[symbol]))

    return (old_canonical_items, item_transitions)


def buildCanonicalItems(grammar_reference):

    canonical_item = [grammar_reference.productions[0]]
    canonical_items = list()
    item_index = 0
    items_transitions = list()  # Goto-table list[tuple[Symbol, item_destination]]
    while True:

        # Se o item canonico for válido
        if canonical_item != None:
            # Adquire o closure
            new_canonical_item = closure(
                canonical_item,
                grammar_reference.noterminals,
                grammar_reference.productions,
            )
            # Agrupa todos possíveis novos itens canônicos por símbolo de transição
            new_canonical_items = separate_canonical_items_by_symbol(new_canonical_item)

            # Atualiza os itens canonicos com os novos
            canonical_items, item_transitions = mergeCanonicalItems(
                new_canonical_items, canonical_items
            )

            # Adiciona as transições do último item canonico
            items_transitions.append(item_transitions)

        # Passa para o próximo item canônico não processado
        item_index += 1

        # Move o pointeiro
        canonical_item = lookAhead(canonical_items[item_index])

        if not item_index < len(new_canonical_items):
            return (canonical_items, items_transitions)


def markShifts(items_transitions, buildSLRTableTerminals):

    for canonical_item_origin_index in range(len(items_transitions)):
        symbol_index = items_transitions[canonical_item_origin_index][0]
        canonical_item_destination_index = items_transitions[
            canonical_item_origin_index
        ][1]
        shift = ("s", canonical_item_destination_index)
        buildSLRTableTerminals[canonical_item_origin_index][symbol_index] = shift
    return buildSLRTableTerminals


def markReduces(
    slr_table_terminals,
    canonical_items,
    follows,
    reference_productions,
    end_of_sequence_index,
):

    # Seleciona um item canônico
    for canonical_item_index in range(len(canonical_items)):
        canonical_item = canonical_items[canonical_item_index]

        # Obtem e salva o número da produção, caso o símbolo a ser lido é o símbolo de final de sentença
        production_index = readCanonicalItemEndOfSentence(
            canonical_item, reference_productions, end_of_sequence_index
        )
        if production_index != -1:

            # Para cada follow da cabeça da produção
            for follow in follows[reference_productions[production_index][0]]:
                reduce = ("r", production_index)

                # Adiciona reduce número da produção
                slr_table_terminals[canonical_item_index][follow] = reduce

    return slr_table_terminals


def markAccept(slr_table_terminals, canonical_items, productions):
    # Seleciona a primeira produção
    initial_production = productions[0]

    # A procura nos itens canônicos
    for canonical_item in canonical_items:
        if initial_production in canonical_item:

            # Marca a ação aceitar no item pelo símbolo de final de sentença
            accept = ("acc", 0)
            slr_table_terminals[canonical_item][-1] = accept

    return slr_table_terminals


def markGoTos(slr_table_noterminals, items_transitions):
    # Para cada item, verifica na tabela de GOTO
    for item_index in range(len(items_transitions)):

        # Para cada não terminal
        for noterminal in range(len(slr_table_noterminals)):

            # Marca a ação desviar no item  pelo não terminal
            deviation = items_transitions[item_index][1]
            slr_table_noterminals[item_index][noterminal] = deviation

    return slr_table_noterminals


@dataclass
class ParserSLR:

    grammar_reference: FrozenGM(
        list[str], list[str], str, list[tuple[int, list[int | str]]]
    ) = field(init=False)

    #    canonical_items: list[list[tuple[int, list[str | int]]]] = field(init=False)
    #    go_to_table: list[tuple[int, int, int]] = field(init=False)

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

    def calculateFirst(self, noterminal, productions, epslon):
        if noterminal in self.firsts_untouched:
            self.firsts_untouched.remove(noterminal)

        if noterminal in self.firsts_in_use:
            raise Exception("Erro")
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
            raise Exception("Erro")
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

    def buildSLRTableTerminals(
        self, grammar_reference, canonical_items, items_transitions
    ):
        # Initialize a tabela de terminais com o formato e tamanho certo
        slr_table_terminals = initializeSLRTable(
            len(canonical_items), len(grammar_reference.terminals), ("", None)
        )

        # Marcar os shifts
        slr_table_terminals = markShifts(slr_table_terminals, items_transitions)

        self.calculateFirsts()
        self.calculateFollows()

        end_of_sequence_index = (
            len(grammar_reference.noterminals) + len(grammar_reference.terminals) - 1
        )

        # Marcar os reduces
        slr_table_terminals = markReduces(
            slr_table_terminals,
            canonical_items,
            self.follows,
            grammar_reference.productions,
            end_of_sequence_index,
        )

        # Marcar o accept
        slr_table_terminals = markAccept(
            slr_table_terminals, canonical_items, grammar_reference.productions
        )

    def buildSLRTableNoTerminals(
        self, grammar_reference, canonical_items, items_transitions
    ):
        # Initialize a tabela de não terminais com o formato e tamanho certo
        slr_table_noterminals = initializeSLRTable(
            len(canonical_items), len(grammar_reference.noterminals), None
        )

        # Marcar os desvios
        slr_table_noterminals = markGoTos(slr_table_noterminals, items_transitions)

    def generateSLRParser(self, grammar):

        # Estende a gramática e a congela
        grammar_reference = extendGrammar(grammar)

        # Construir itens canônicos (automato)
        canonical_items, items_transitions = buildCanonicalItems(grammar_reference)

        # Contruir tabela SLR
        self.buildSLRTableTerminals(
            grammar_reference, canonical_items, items_transitions
        )
        self.buildSLRTableNoTerminals(
            grammar_reference, canonical_items, items_transitions
        )

        # Demais entradas na tabela são erros

        # Estado inicial é o que contém a produção pelo símbolo inicial da gramática estendida
