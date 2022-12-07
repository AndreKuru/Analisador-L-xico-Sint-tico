from formals.GM import readGM
from formals.Scanner import readFA, readER
from formals.FA import FA
from formals.RE import RE


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


def test_read_FA():

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
    exit = readFA("afdb.txt")
    assert exit == expected


def test_read_RE():

    expected = RE(
        [("digit", "[0-9]"), ("letter", "[a-zA-Z]"), ("id", "letter(letter | digit)*")]
    )

    exitRE = readER("./tests/er2.txt")
    assert exitRE == expected
