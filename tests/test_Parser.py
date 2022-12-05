from formals.GM import GM

def test_generateSLRParser_with_slides_gramar():

  noterminals = {'E', 'T', 'F'}
  terminals = {'id', '+', '*', '(', ')'}
  initial = 'E'
  productions = {'E': {'E+T', 'T'},
                'T': {'T*F', 'F'},
                'F': {'(E)', 'id'}}

  gramar = GM(noterminals, terminals, initial, productions)

  #generateSLRTable(gramar)

  canonicalItems = (
    ( # Item 0
      ("E'", "·E"),
      ("E", "·E+T"),
      ("E", "·T"),
      ("T", "·T*F"),
      ("T", "·F"),
      ("F", "·(E)"),
      ("F", "·id"),
    ),
    ( # Item 1
      ("E'", "E·"),
      ("E", "E·+T"),
    ),
    ( # Item 2
      ("E", "T·"),
      ("T", "T·*F"),
    ),
    ( # Item 3
      ("T", "F·"),
    ),
    ( # Item 4
      ("F", "(·E)"),
      ("E", "·E+T"),
      ("E", "·T"),
      ("T", "·T*F"),
      ("T", "·F"),
      ("F", "·(E)"),
      ("F", "·id"),
    ),
    ( # Item 5
      ("F", "id·"),
    ),
    ( # Item 6
      ("E", "E+·T"),
      ("T", "·T*F"),
      ("T", "·F"),
      ("F", "·(E)"),
      ("F", "·id"),
    ),
    ( # Item 7
      ("T", "T*·F"),
      ("F", "·(E)"),
      ("F", "·id"),
    ),
    ( # Item 8
      ("E", "E·+T"),
      ("F", "(E·)"),
    ),
    ( # Item 9
      ("E", "E+T·"),
      ("T", "T·*F"),
    ),
    ( # Item 10
      ("T", "T*F·"),
    ),
    ( # Item 11
      ("F", "(E)·"),
    ),
  )

  slr_table_terminals = (
  ''' 0''' (("s", 5), ("", None), ("", None), ("s", 4), ("", None), ("", None)),
  ''' 1''' (("", None), ("s", 6), ("", None), ("", None), ("", None), ("acc", None)),
  ''' 2''' (("", None), ("r", 2), ("s", 7), ("", None), ("r", 2), ("r", 2)),
  ''' 3''' (("", None), ("r", 4), ("r", 4), ("", None), ("r", 4), ("r", 4)),
  ''' 4''' (("s", 5), ("", None), ("", None), ("s", 4), ("", None), ("", None)),
  ''' 5''' (("", None), ("r", 6), ("r", 6), ("", None), ("r", 6), ("r", 6)),
  ''' 6''' (("s", 5), ("", None), ("", None), ("s", 4), ("", None), ("", None)),
  ''' 7''' (("s", 5), ("", None), ("", None), ("s", 4), ("", None), ("", None)),
  ''' 8''' (("", None), ("r", 6), ("", None), ("", None), ("s", 11), ("", None)),
  ''' 9''' (("", None), ("r", 1), ("s", 7), ("", None), ("r", 1), ("r", 1)),
  '''10''' (("", None), ("r", 3), ("r", 3), ("", None), ("r", 3), ("r", 3)),
  '''11''' (("", None), ("r", 5), ("r", 5), ("", None), ("r", 5), ("r", 5)),
  )

  slr_table_noterminals = (
  ''' 0''' (1, 2, 3),
  ''' 1''' (None, None, None),
  ''' 2''' (None, None, None),
  ''' 3''' (None, None, None),
  ''' 4''' (8, 2, 3),
  ''' 5''' (None, None, None),
  ''' 6''' (None, 9, 3),
  ''' 7''' (None, None, 10),
  ''' 8''' (None, None, None),
  ''' 9''' (None, None, None),
  '''10''' (None, None, None),
  '''11''' (None, None, None),
  )