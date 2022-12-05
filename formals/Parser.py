from dataclasses import dataclass
from GM import GM
import sys
import os

@dataclass
class Parser:

    terminals: list[str]
    noterminals: list[str]
    canonical_items: list[list[tuple[str, str]]]
    slr_table_terminals: list[list[tuple[str, int]]]
    slr_table_noterminals: list[list[tuple[str, int]]]

    def markProduction(production):

        marked_production = '.' + production
        
        return set(marked_production)



    def buildCanonicalItems(grammar):
        for hbody in grammar.productions.values():
            unmarked_productions = list(body)
            marked_productions = list()
            for production in unmarked_productions:
                if '.' not in production:
                    marked_production = markProduction(production)
                    marked_productions.append(marked_production)

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

    noterminals = {'E', 'T', 'F'}
    terminals = {'+', '*', '(', ')', 'id'}
    initial = 'E'
    productions = {'E': {'E+T', 'T'},
                  'T': {'T*F', 'F'},
                  'F': {'(E)', 'id'}}

    gm = GM(noterminals, terminals, initial, productions)
    generateSLRParser(gm)