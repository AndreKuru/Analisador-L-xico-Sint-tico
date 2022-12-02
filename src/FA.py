class FA:

  def __init__(self, states, initial, final_states, alphabet, transitions) -> None:
    self.states        = states
    self.initial = initial
    self.final_states = final_states
    self.alphabet       = alphabet
    self.transitions     = transitions

  def printFA(self):
    print(f"Número de estados: {self.states}")
    print(f"Estado inicial: {self.initial}") 
    print(f"Estados finais: {self.final_states}") 
    print(f"Alfabeto: {self.alphabet}") 
    print("Transições: ")
    for transition in self.transitions:
      print(transition)
