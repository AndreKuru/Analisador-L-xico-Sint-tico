from formals.GM import GM, FrozenGM
from formals.Parser import (
    ParserSLR,
    indexBodies,
    extendGrammar,
    indexProductions,
    MARK_POINTER,
    END_OF_SENTENCE,
    closure,
    lookAhead,
    readCanonicalItemEndOfSentence,
)


def test_read_GM():

    expected = (
        "S▶️",
        {
            "S▶️": {"bB", "aA", "&"},
            "S": {"aA", "bB"},
            "A": {"aS", "bC", "A"},
            "B": {
                "aC",
                "B",
                "bS",
            },
            "C": {"ba", "aB"},
        },
        {"S▶️", "S", "A", "B", "C"},
        {"&", "ba", "b", "a"},
    )

    exitGM = readGM("gr1.txt")
    assert exitGM == expected


def test_indexBodies_with_slides_gramar():

    marked_productions = [
        ("E▶️", ".E"),
        ("E", ".E+T"),
        ("E", ".T"),
        ("T", ".T*F"),
        ("T", ".FF"),
        ("F", ".(E)"),
        ("F", ".id"),
    ]

    noterminals = ["E▶️", "E", "T", "F"]

    terminals = ["id", "+", "*", "(", "=", "[", "]", ")"]

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

    if False:
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

    expected = [
        (0, [".", 1]),
        (1, [".", 1, 5, 2]),
        (1, [".", 2]),
        (2, [".", 2, 6, 3]),
        (2, [".", 3, 3]),
        (3, [".", 7, 1, 11]),
        (3, [".", 4]),
    ]

    assert indexed_productions == expected


"""
def test_extendGrammar_with_grammar_from_slides():

    noterminals = {"E", "T", "F"}
    terminals = {"id", "+", "*", "(", ")"}
    initial = "E"
    productions = {"E": {"E+T", "T"}, "T": {"T*F", "F"}, "F": {"(E)", "id"}}

    gm = GM(noterminals, terminals, initial, productions)
    
    expected_frozen_noterminals = list({'E', 'T', 'F'})
    expected_frozen_noterminals.sort()
    expected_frozen_noterminals = ['E▶️'] + expected_frozen_noterminals
    expected_frozen_terminals = list({'id', '+', '*', '(', ')'})
    expected_frozen_terminals.sort()
    expected_frozen_terminals += [END_OF_SENTENCE]
    expected_frozen_initial = 'E▶️'
    expected_frozen_productions = [(expected_frozen_initial, initial)]
    for head in productions:
        for body in productions[head]:
            expected_frozen_productions.append((head, MARK_POINTER + body + END_OF_SENTENCE))

    expected_frozen_productions = indexProductions(expected_frozen_noterminals, expected_frozen_terminals, expected_frozen_productions)

    expected = FrozenGM(expected_frozen_noterminals, expected_frozen_terminals, expected_frozen_initial, expected_frozen_productions)

    frozen_grammar = extendGrammar(gm)
    frozen_grammar_noterminals = frozen_grammar.noterminals[1:]
    frozen_grammar_noterminals.sort()
    frozen_grammar_noterminals = [frozen_grammar.noterminals[0]] + frozen_grammar_noterminals

    frozen_grammar_terminals = frozen_grammar.terminals[:len(frozen_grammar.terminals) - 1]
    frozen_grammar_terminals.sort()
    frozen_grammar_terminals += [frozen_grammar.terminals[len(frozen_grammar.terminals) - 1]]

    frozen_grammar = FrozenGM(
        frozen_grammar_noterminals,
        frozen_grammar_terminals,
        frozen_grammar.initial,
        frozen_grammar.productions
    )
    assert frozen_grammar == expected

"""


def test_indexProductions():

    noterminals = ["E▶️", "E", "T", "F"]

    terminals = ["id", "+", "*", "(", ")"]

    marked_productions = [
        ("E▶️", ".E"),
        ("E", ".E+T"),
        ("E", ".T"),
        ("T", ".T*F"),
        ("T", ".F"),
        ("F", ".(E)"),
        ("F", ".id"),
    ]

    expected = [
        (0, [".", 1]),
        (1, [".", 1, 5, 2]),
        (1, [".", 2]),
        (2, [".", 2, 6, 3]),
        (2, [".", 3]),
        (3, [".", 7, 1, 8]),
        (3, [".", 4]),
    ]

    indexed_productions = indexProductions(noterminals, terminals, marked_productions)
    assert indexed_productions == expected


def test_closure_with_canonical_items_0_from_slides_gramar():

    noterminals = ["E▶️", "E", "T", "F"]
    terminals = ["+", "*", "(", ")", "id", "$"]

    productions = [
        ("E▶️", MARK_POINTER + "E"),
        ("E", MARK_POINTER + "E+T"),
        ("E", MARK_POINTER + "T"),
        ("T", MARK_POINTER + "T*F"),
        ("T", MARK_POINTER + "F"),
        ("F", MARK_POINTER + "(E)"),
        ("F", MARK_POINTER + "id"),
    ]
    indexed_reference_productions = indexProductions(
        noterminals, terminals, productions
    )
    initial_production = [indexed_reference_productions[0]]

    expected = [
        ("E▶️", MARK_POINTER + "E"),
        ("E", MARK_POINTER + "E+T"),
        ("E", MARK_POINTER + "T"),
        ("T", MARK_POINTER + "T*F"),
        ("T", MARK_POINTER + "F"),
        ("F", MARK_POINTER + "(E)"),
        ("F", MARK_POINTER + "id"),
    ]

    expected = indexProductions(noterminals, terminals, expected)

    item6 = [
        ("E", "E+" + MARK_POINTER + "T"),
    ]
    indexed_item6 = indexProductions(noterminals, terminals, item6)

    expected_item6 = [
        ("E", "E+" + MARK_POINTER + "T"),
        ("T", MARK_POINTER + "T*F"),
        ("T", MARK_POINTER + "F"),
        ("F", MARK_POINTER + "(E)"),
        ("F", MARK_POINTER + "id"),
    ]

    indexed_expected_item6 = indexProductions(noterminals, terminals, expected_item6)

    canonical_item = closure(
        initial_production, noterminals, indexed_reference_productions
    )
    canonical_item6 = closure(indexed_item6, noterminals, indexed_reference_productions)

    assert canonical_item == expected
    assert canonical_item6 == indexed_expected_item6


def test_lookAhead_with_slides_item6_to_item9():
    # Pro indexed ***BEGIN
    noterminals = ["E▶️", "E", "T", "F"]
    terminals = ["+", "*", "(", ")", "id", "$"]
    # Pro indexed ***END
    canonical_item6 = [("E", "E+" + MARK_POINTER + "T$"), ("T", MARK_POINTER + "T*F$")]

    indexed_canonical_item6 = indexProductions(noterminals, terminals, canonical_item6)

    expected_canonical_item6 = [
        ("E", "E+T" + MARK_POINTER + "$"),
        ("T", "T" + MARK_POINTER + "*F$"),
    ]

    indexed_expected_canonical_item6 = indexProductions(
        noterminals, terminals, expected_canonical_item6
    )

    indexed_canonical_item6 = lookAhead(indexed_canonical_item6)

    assert indexed_canonical_item6 == indexed_expected_canonical_item6


def test_readCanonicalItemEndOfSentence_with_slides_item6() -> bool:
    # Pro indexed ***BEGIN
    noterminals = ["E▶️", "E", "T", "F"]
    terminals = ["+", "*", "(", ")", "id", "$"]

    reference_productions = [
        ("E▶️", MARK_POINTER + "E$"),
        ("E", MARK_POINTER + "E+T$"),
        ("E", MARK_POINTER + "T$"),
        ("T", MARK_POINTER + "T*F$"),
        ("T", MARK_POINTER + "F$"),
        ("F", MARK_POINTER + "(E)$"),
        ("F", MARK_POINTER + "id$"),
    ]
    reference_productions = indexProductions(
        noterminals, terminals, reference_productions
    )

    end_of_sequence_index = len(noterminals) + len(terminals) - 1
    # Pro indexed ***END
    canonical_item6 = [("E", "E+" + MARK_POINTER + "T$"), ("T", MARK_POINTER + "T*F$")]

    indexed_canonical_item6 = indexProductions(noterminals, terminals, canonical_item6)

    expected = -1

    result = readCanonicalItemEndOfSentence(
        indexed_canonical_item6, reference_productions, end_of_sequence_index
    )

    assert expected == result


def test_readCanonicalItemEndOfSentence_with_slides_item5() -> bool:
    # Pro indexed ***BEGIN
    noterminals = ["E▶️", "E", "T", "F"]
    terminals = ["+", "*", "(", ")", "id", "$"]

    reference_productions = [
        ("E▶️", MARK_POINTER + "E$"),
        ("E", MARK_POINTER + "E+T$"),
        ("E", MARK_POINTER + "T$"),
        ("T", MARK_POINTER + "T*F$"),
        ("T", MARK_POINTER + "F$"),
        ("F", MARK_POINTER + "(E)$"),
        ("F", MARK_POINTER + "id$"),
    ]
    reference_productions = indexProductions(
        noterminals, terminals, reference_productions
    )

    end_of_sequence_index = len(noterminals) + len(terminals) - 1
    # Pro indexed ***END
    canonical_item5 = [("F", "id" + MARK_POINTER + "$")]

    indexed_canonical_item5 = indexProductions(noterminals, terminals, canonical_item5)

    expected = 6

    result = readCanonicalItemEndOfSentence(
        indexed_canonical_item5, reference_productions, end_of_sequence_index
    )

    assert expected == result


'''

def test_goTo_with_canonical_item_0_from_slides_gramar():

    item = [
        ("E'", '.E'),
        ('E', '.E+T'),
        ('E', '.T'),
        ('T', '.T*F'),
        ('T', '.F'),
        ('F', '.(E)'),
        ('F', '.id')
    ]
    symbol = 'id'

    expected = [
        ('F', 'id.')
        ]
    
    goto = goTo(item, symbol)
    assert goto == expected


def test_buildCanonicalItems_with_slides_gramar():
    noterminals = {"E", "T", "F"}
    terminals = {"id", "+", "*", "(", ")"}
    initial = "E"
    productions = {"E": {"E+T", "T"}, "T": {"T*F", "F"}, "F": {"(E)", "id"}}

    gramar = GM(noterminals, terminals, initial, productions)

    expected = [
        [  # item 0
            ("e'", "·e"),
            ("e", "·e+t"),
            ("e", "·t"),
            ("t", "·t*f"),
            ("t", "·f"),
            ("f", "·(e)"),
            ("f", "·id"),
        ],
        [  # item 1
            ("e'", "e·"),
            ("e", "e·+t"),
        ],
        [  # item 2
            ("e", "t·"),
            ("t", "t·*f"),
        ],
        [
            ("t", "f·"),
        ],  # item 3
        [  # item 4
            ("f", "(·e)"),
            ("e", "·e+t"),
            ("e", "·t"),
            ("t", "·t*f"),
            ("t", "·f"),
            ("f", "·(e)"),
            ("f", "·id"),
        ],
        [
            ("f", "id·"),
        ],  # item 5
        [  # item 6
            ("e", "e+·t"),
            ("t", "·t*f"),
            ("t", "·f"),
            ("f", "·(e)"),
            ("f", "·id"),
        ],
        [  # item 7
            ("t", "t*·f"),
            ("f", "·(e)"),
            ("f", "·id"),
        ],
        [  # item 8
            ("e", "e·+t"),
            ("f", "(e·)"),
        ],
        [  # item 9
            ("e", "e+t·"),
            ("t", "t·*f"),
        ],
        [
            ("t", "t*f·"),
        ],  # item 10
        [
            ("f", "(e)·"),
        ],  # item 11
    ]

    canonical_items = buildCanonicalItems(gramar)

    assert canonical_items == expected


def test_generateSLRParser_with_slides_gramar():

    noterminals = {"E", "T", "F"}
    terminals = {"id", "+", "*", "(", ")"}
    initial = "E"
    productions = {"E": {"E+T", "T"}, "T": {"T*F", "F"}, "F": {"(E)", "id"}}

    gramar = GM(noterminals, terminals, initial, productions)

    parser = generateSLRParser(gramar)

    canonical_items = [
        [  # item 0
            ("e'", "·e"),
            ("e", "·e+t"),
            ("e", "·t"),
            ("t", "·t*f"),
            ("t", "·f"),
            ("f", "·(e)"),
            ("f", "·id"),
        ],
        [  # item 1
            ("e'", "e·"),
            ("e", "e·+t"),
        ],
        [  # item 2
            ("e", "t·"),
            ("t", "t·*f"),
        ],
        [
            ("t", "f·"),
        ],  # item 3
        [  # item 4
            ("f", "(·e)"),
            ("e", "·e+t"),
            ("e", "·t"),
            ("t", "·t*f"),
            ("t", "·f"),
            ("f", "·(e)"),
            ("f", "·id"),
        ],
        [
            ("f", "id·"),
        ],  # item 5
        [  # item 6
            ("e", "e+·t"),
            ("t", "·t*f"),
            ("t", "·f"),
            ("f", "·(e)"),
            ("f", "·id"),
        ],
        [  # item 7
            ("t", "t*·f"),
            ("f", "·(e)"),
            ("f", "·id"),
        ],
        [  # item 8
            ("e", "e·+t"),
            ("f", "(e·)"),
        ],
        [  # item 9
            ("e", "e+t·"),
            ("t", "t·*f"),
        ],
        [
            ("t", "t*f·"),
        ],  # item 10
        [
            ("f", "(e)·"),
        ],  # item 11
    ]

    slr_table_terminals = [
        """ 0"""[("s", 5), ("", None), ("", None), ("s", 4), ("", None), ("", None)],
        """ 1"""[
            ("", None), ("s", 6), ("", None), ("", None), ("", None), ("acc", None)
        ],
        """ 2"""[("", None), ("r", 2), ("s", 7), ("", None), ("r", 2), ("r", 2)],
        """ 3"""[("", None), ("r", 4), ("r", 4), ("", None), ("r", 4), ("r", 4)],
        """ 4"""[("s", 5), ("", None), ("", None), ("s", 4), ("", None), ("", None)],
        """ 5"""[("", None), ("r", 6), ("r", 6), ("", None), ("r", 6), ("r", 6)],
        """ 6"""[("s", 5), ("", None), ("", None), ("s", 4), ("", None), ("", None)],
        """ 7"""[("s", 5), ("", None), ("", None), ("s", 4), ("", None), ("", None)],
        """ 8"""[("", None), ("r", 6), ("", None), ("", None), ("s", 11), ("", None)],
        """ 9"""[("", None), ("r", 1), ("s", 7), ("", None), ("r", 1), ("r", 1)],
        """10"""[("", None), ("r", 3), ("r", 3), ("", None), ("r", 3), ("r", 3)],
        """11"""[("", None), ("r", 5), ("r", 5), ("", None), ("r", 5), ("r", 5)],
    ]

    slr_table_noterminals = [
        """ 0"""[1, 2, 3],
        """ 1"""[None, None, None],
        """ 2"""[None, None, None],
        """ 3"""[None, None, None],
        """ 4"""[8, 2, 3],
        """ 5"""[None, None, None],
        """ 6"""[None, 9, 3],
        """ 7"""[None, None, 10],
        """ 8"""[None, None, None],
        """ 9"""[None, None, None],
        """10"""[None, None, None],
        """11"""[None, None, None],
    ]

    expected = Parser(
        list(terminals),
        list(noterminals),
        canonical_items,
        slr_table_terminals,
        slr_table_noterminals,
    )

    assert parser == expected
'''
