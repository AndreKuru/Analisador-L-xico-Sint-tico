from formals.FA import FA


def test_determinizeFA_with_epslon_transitions():
    fa = FA(
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
        4,
        {"a", "b"},
        0,
        {"token_generic": {0, 2, 3}},
        [
            (0, "a", 1),
            (0, "b", 2),
            (1, "a", 1),
            (1, "b", 2),
            (2, "a", 1),
            (2, "b", 3),
            (3, "b", 3),
        ],
    )

    fa.determinizeFA()
    assert fa == expected


def test_discardDead():
    fa = FA(
        4,
        {"a", "b"},
        0,
        {"token": {1, 2}},
        [(0, "a", 1), (0, "b", 0), (1, "a", 2), (1, "b", 1), (2, "a", 1), (2, "b", 2), (3, "a", 1), (3, "b", 2)],
    )

    expected = FA(
        3,
        {"a", "b"},
        0,
        {"token": {1, 2}},
        [(0, "a", 1), (0, "b", 0), (1, "a", 2), (1, "b", 1), (2, "a", 1), (2, "b", 2)],
    )

    fa.discardDead()
    assert fa == expected

def test_discardUnreach():

    fa = FA(
        3,
        {"a", "b"},
        0,
        {"token": {1, 2}},
        [(0, "a", 1), (0, "b", 0), (1, "a", 2), (1, "b", 1), (2, "a", 1), (2, "b", 2)],
    )
    
    expected = FA(
        3,
        {"a", "b"},
        0,
        {"token": {1, 2}},
        [(0, "a", 1), (0, "b", 0), (1, "a", 2), (1, "b", 1), (2, "a", 1), (2, "b", 2)],
    )
    
    fa.discardUnreach()
    assert fa == expected

def test_mergeClasses():
    
    fa = FA(
        3,
        {"a", "b"},
        0,
        {"token": {1, 2}},
        [(0, "a", 1), (0, "b", 0), (1, "a", 2), (1, "b", 1), (2, "a", 1), (2, "b", 2)],
    )
    expected = FA(
        2,
        {"a", "b"},
        0,
        {"token": {1}},
        [(0, "a", 1), (0, "b", 0), (1, "b", 1), (1, "a", 1)],
    )
    
    fa.mergeClasses()
    assert fa == expected
