from formals.GM import GM
from formals.FA import FA


def test_eliminateLR():
    gr = GM(
        "E",
        {
            "E": {"T", "E-T", "E+T"},
            "T": {"T", "T*F", "T/F"},
            "F": {"P", "F**P"},
            "P": {"(E)", "cte", "id"},
        },
        {"F", "P", "T", "E"},
        {"/", "-", "cte", "(", "id", "**", "+", "*"},
    )
    expected = GM(
        "E",
        {
            "E": {"TE'"},
            "E'": {"-TE'", "+TE'", "&"},
            "T": {"FT'"},
            "T'": {"*FT'", "/TF'", "&"},
            "F": {"PF'"},
            "F'": {"**PF'", "&"},
            "P": {"F**P"},
            "P": {"(E)", "cte", "id"},
        },
        {"F", "P", "T", "E", "E'", "T'", "F'"},
        {"/", "-", "cte", "(", "id", "**", "+", "*"},
    )

    assert gr == expected
