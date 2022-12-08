from formals.Scanner import readFA, readER, automataUnion
from formals.FA import FA
from formals.RE import RE


"""
def test_readRE():

    expected = RE(
        [("digit", "[0-9]"), ("letter", "[a-zA-Z]"), ("id", "letter(letter | digit)*")]
    )

    exitRE = readER("./tests/er2.txt")
    assert exitRE == expected


def test_readFA_with_afdb():

    expected = FA(
        5,
        {"a", "b"},
        0,
        {"token_generic": {3}},
        [
            (0, "a", 1),
            (0, "b", 2),
            (1, "a", 1),
            (1, "b", 3),
            (2, "a", 1),
            (2, "b", 2),
            (3, "a", 1),
            (3, "b", 4),
            (4, "a", 1),
            (4, "b", 2),
        ],
    )
    exit = readFA("tests/afdb.txt")
    assert exit == expected


def test_readFA_with_afnde():

    expected = FA(
        4,
        {"a", "b", "&"},
        0,
        {"token_generic": {3}},
        [
            (0, "&", 1),
            (0, "&", 2),
            (1, "a", 1),
            (1, "b", 2),
            (2, "a", 1),
            (2, "&", 3),
            (3, "b", 3),
        ],
    )
    exit = readFA("tests/afnde.txt")
    assert exit == expected

"""

def test_automataUnion():
    automatas = []
    automatas.append(
        FA(
            4,
            {"a", "b"},
            0,
            {"token_generic": {2}},
            [
                (0, "a", 1),
                (0, "b", 3),
                (1, "a", 1),
                (1, "b", 2),
                (2, "a", 1),
                (2, "b", 2),
                (3, "a", 3),
                (3, "b", 3),
            ],
        )
    )
    automatas.append(
        FA(
            4,
            {"a", "b"},
            0,
            {"token_generic": {2}},
            [
                (0, "b", 1),
                (0, "a", 3),
                (1, "b", 1),
                (1, "a", 2),
                (2, "b", 1),
                (2, "a", 2),
                (3, "b", 3),
                (3, "a", 3),
            ],
        )
    )

    expect = FA(
        9,
        {"a", "b", "&"},
        0,
        {"token_generic": {3, 7}},
        [
            (0, "&", 1),
            (1, "a", 2),
            (1, "b", 4),
            (2, "a", 2),
            (2, "b", 3),
            (3, "a", 2),
            (3, "b", 3),
            (4, "a", 4),
            (4, "b", 4),
            (0, "&", 5),
            (5, "b", 6),
            (5, "a", 8),
            (6, "b", 6),
            (6, "a", 7),
            (7, "b", 6),
            (7, "a", 7),
            (8, "b", 8),
            (8, "a", 8),
        ],
    )

    result = automataUnion(automatas)

    assert result == expect
