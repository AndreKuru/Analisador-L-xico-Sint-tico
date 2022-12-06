from dataclasses import dataclass
from formals.GM import GM
import sys
import os

@dataclass
class Parser:

    terminals: list[str]
    noterminals: list[str]
    canonical_items: list[list[tuple[str, str]]]
    slr_table_terminals: list[list[tuple[str, int]]]
    slr_table_noterminals: list[list[int]]

def goTo(item, symbol):

    new_productions = list()
    for production in item:
        new_production = tuple()
        body = list(production[1])
        dot_index = body.index('.')
        
        symbol_being_read = body[dot_index + 1]
        if symbol_being_read == symbol:
            body.remove('.')
            body.insert(dot_index + 1, '.')
            new_body = ''.join(body)
            new_production = (production[0], new_body)
            new_productions.append(new_production)
    
    return new_productions

def closure(item, symbol, productions, noterminals):

    heads_to_be_inserted = list()
    heads_to_be_inserted.append(symbol)

    i = 0
    while i < len(heads_to_be_inserted):
        for production in productions:
            if production[0] == heads_to_be_inserted[i]:
                item.append(production)
                symbol_being_read = production[1][production[1].index('.') + 1]

                if (symbol_being_read not in heads_to_be_inserted and 
                    symbol_being_read in noterminals):
                    heads_to_be_inserted.append(symbol_being_read)

        i += 1
    
    return item

def indexBodies(symbols: list(), bodies, shift):

    for symbol_index in range(len(symbols)):
        symbol = symbols[symbol_index]

        for body in bodies:
                body_index = bodies.index(body)

                for element in body:

                    if symbol in element:
                        element_index = body.index(element)
                        saved_slice_begin = body[:element_index]
                        saved_slice_end = body[element_index + 1:]
                        splited_element = element.split(symbol)

                        last_position = len(splited_element) - 1
                        for i in range(last_position, 0, -1):
                            splited_element.insert(i, str(symbol_index + shift))
                        splited_element = saved_slice_begin + splited_element + saved_slice_end
                        
                        while '' in splited_element:
                            splited_element.remove('')
                        bodies[body_index] = splited_element
        
    return bodies

def indexProductions(noterminals: list(), terminals: list(), marked_productions):
    
    heads = list()
    bodies = list()
    for (_, body) in marked_productions:
        bodies.append([body])

    for noterminal_index in range(len(noterminals)):
        noterminal = noterminals[noterminal_index]

        for (head, _) in marked_productions:
            if head == noterminal:
                heads.append(noterminal_index)

    bodies = indexBodies(noterminals, bodies, 0)

    bodies = indexBodies(terminals, bodies, len(noterminals))

    for body in bodies:
        body_index = bodies.index(body)

        for element in body:
            element_index = body.index(str(element))

            if element.isnumeric():
                element = int(element)
                body[element_index] = element

        bodies[body_index] = body
    
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
            if '.' not in production:
                marked_production = '.' + production
                marked_productions.append(tuple(head, marked_production))
    
    return marked_productions

def buildCanonicalItems(grammar):

    # Marca produções com um ponto
    marked_productions = markProductions(grammar)
    indexed_productions = indexProductions(terminals, noterminals, marked_productions)

    canonical_items = []
    first_item = []
    first_body = marked_productions[marked_productions.index(grammar.initial)][1]
    first_production = (grammar.initial, first_body)
    first_item.append(first_production)
    symbol_being_read = first_body[first_body.index('.') + 1]
    if symbol_being_read in grammar.noterminals:
        new_item = closure(first_item, symbol_being_read, marked_productions, grammar.noterminals)
        canonical_items.append(new_item)
    go_tos = {}
    for index in range(len(canonical_items)):
        go_to = []
        for production in canonical_items[index]:
            symbol_being_read = production[1][production[1].index('.') + 1]
            go_to = goTo(canonical_items[index], symbol_being_read)
            go_tos[(index, symbol_being_read)] = go_to

def extendGrammar(grammar):

    initial = grammar.initial + "▶️"
    noterminals = grammar.noterminals
    terminals = grammar.terminals
    productions = grammar.productions
    productions[initial] = grammar.initial

    extended_gm = GM(noterminals, terminals, initial, productions)

    return extended_gm

def generateSLRParser(grammar):

    # Estender gramática
    extended_gm = extendGrammar(grammar)

    # Construir itens canônicos (automato)
    canonical_items = buildCanonicalItems(extended_gm)

    # Contruir tabela SLR
    SLRTableTerminals = buildSLRTableTerminals(canonical_items, extended_gm)
    SLRTableNonTerminals = buildSLRTableNonTerminals(canonical_items, extended_gm)
    
    # Marcar os shifts
    markShifts(SLRTableTerminals)

    # Marcar os reduces
    markReduces(SLRTableTerminals)

    # Marcar o accept
    markAccept(SLRTableTerminals)

    # Calcular os follows
    follows = calculateFollows(extended_gm)

    # Marcar os desvios
    markGoTos(SLRTableNonTerminals)

    # Demais entradas na tabela são erros

    # Estado inicial é o que contém a produção pelo símbolo inicial da gramática estendida

closure(
    item = [("E'", '.E')],
    symbol = 'E',
    productions = [
        ("E'", '.E'),
        ('E', '.E+T'),
        ('E', '.T'),
        ('T', '.T*F'),
        ('T', '.F'),
        ('F', '.(E)'),
        ('F', '.id')
    ],
    noterminals = ['E', 'T', 'F']
)