from formals.GM import GM
from formals.Parser import Parser, buildCanonicalItems, generateSLRParser, closure, goTo


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
    symbol = '('

    expected = [
        ('F', '(.E)')
        ]
    
    goto = goTo(item, symbol)
    assert goto == expected

def test_closure_with_canonical_items_0_from_slides_gramar():

    item = [("E'", '.E')]
    symbol = 'E'
    productions = [
        ("E'", '.E'),
        ('E', '.E+T'),
        ('E', '.T'),
        ('T', '.T*F'),
        ('T', '.F'),
        ('F', '.(E)'),
        ('F', '.id')
    ]
    noterminals = ['E', 'T', 'F']

    expected = [
        ("E'", '.E'),
        ('E', '.E+T'),
        ('E', '.T'),
        ('T', '.T*F'),
        ('T', '.F'),
        ('F', '.(E)'),
        ('F', '.id')
    ]

    canonical_item = closure(item, symbol, productions, noterminals)
    assert canonical_item == expected

'''def test_buildCanonicalItems_with_slides_gramar():
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