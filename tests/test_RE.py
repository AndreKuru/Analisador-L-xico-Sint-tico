from formals.FA import FA
from formals.RE import RE


def test_generateFAs():

    re = RE(
        [("digit", "[0-9]"), ("letter", "[a-zA-Z]"), ("id", "letter(letter | digit)*")]
    )

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

    expected = FA(
        3,
        {"a", "b"},
        0,
        {"token_generic": {0}},
        [
            (0, "a", 1),
            (0, "b", 2),
            (1, "b", 0),
            (2, "a", 0),
        ],
    )
    re.generateFAs()
    assert re == expected
