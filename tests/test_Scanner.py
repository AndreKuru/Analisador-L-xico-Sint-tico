from formals.FA import FA
from formals.Scanner import *

def test_readFA():
    fa = readFA("afda.txt")

    expected = FA(
        4,
        {"a", "b"},
        0,
        {"token_generic": {0, 1, 2, 3}},
        [
            (0, "a", 1),
            (0, "b", 0),
            (1, "a", 0),
            (1, "b", 1),
            (2, "a", 3),
            (2, "b", 2),
            (3, "a", 2),
            (3, "b", 3),
        ],
    )

    assert fa == expected

def test_automataUnion():
    automatas = []
    automatas.append(FA(4, {"a", "b"}, 0, {"token_generic": {2}}, [(0, "a", 1), (0, "b", 3), (1, "a", 1), (1, "b", 2), (2, "a", 1), (2, "b", 2), (3, "a", 3), (3, "b", 3)]))
    automatas.append(FA(4, {"a","b"}, 0, {"token_generic": {2}}, [(0, "b", 1), (0, "a", 3), (1, "b", 1), (1, "a", 2), (2, "b", 1), (2, "a", 2), (3, "b", 3), (3, "a", 3)]))

     
    expect = FA(5, {"a", "b"}, 0, {"token_generic": {2, 4}}, [(0, "b", 1), (0, "a", 3), (1, "b", 1), (1, "a", 2), (2, "b", 1), (2, "a", 2), (3, "4", 3), (3, "a", 3), (4, "a", 3), (4, "b", 4)])
