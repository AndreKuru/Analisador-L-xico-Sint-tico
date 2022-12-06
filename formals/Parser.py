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
    pass

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

    canonical_items = []
    first_item = []
    first_body = marked_productions[marked_productions.index(grammar.initial)][1]
    first_production = (grammar.initial, first_body)
    first_item.append(first_production)
    symbol_being_read = first_body[first_body.index('.') + 1]
    if symbol_being_read in grammar.noterminals:
        closure(first_item, symbol_being_read, marked_productions, grammar.noterminals)
    elif symbol_being_read in grammar.terminals:
        goTo(first_item, symbol_being_read)

def extendGrammar(grammar):

    initial = grammar.initial + "'"
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