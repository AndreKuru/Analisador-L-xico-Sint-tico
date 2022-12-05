from dataclasses import dataclass

@dataclass
class FA:

  total_states: int
  alphabet: set[str]
  initial: int
  final_states: set[int]
  transitions: list[list[int | str]]
  #transitions: list[tuple[int, str, int]]

  def printFA(self):
    print(f"Número de estados: {self.total_states}")
    print(f"Estado inicial: {self.initial}") 
    print(f"Estados finais: {self.final_states}") 
    print(f"Alfabeto: {self.alphabet}") 
    print("Transições: ")
    for transition in self.transitions:
      print(transition)

  def determinizeFA(self):
    # Calcular e fecho
    e_closures = list()
    # Adiciona o proprio estado ao seu e-fecho 
    for state in range(self.total_states):
      e_closure = {state}
      e_closures.append(e_closure)

    # Adiciona demais estados alcançados por e-transicoes
    for transition in self.transitions:
      if '&' in transition:

        # Adiciona recursivamente em todos os closures que contem aquele estado origem
        origin_state = transition[0]
        for index in range(len(e_closures)):
          if (origin_state in e_closures[index]):
            destination_state_closure = e_closures[transition[2]]
            e_closures[index] = e_closures[index].union(destination_state_closure)

    new_states = list()
    new_states.append(e_closures[self.initial])

    # Inicialização para o while
    new_transitions = list()
    new_state_index = 0

    alphabet = list(self.alphabet)
    alphabet.remove('&')
    alphabet.sort()

    # While para completar todos estados e transições
    while (new_state_index < len(new_states)):

      # Inicializa todas as transições para o estado selecionado
      for symbol_index in alphabet:
        new_transitions.append([
          new_state_index,
          symbol_index, 
          set()
        ])


      #Busca por cada transição de cada estado nos novos estados (que são conjuntos dos estados antigos)
      # e mescla nas transições do estado novo
      for old_state in new_states[new_state_index]:
        for symbol_index in range(len(alphabet)):
          for transition in self.transitions:
            if (transition[0] == old_state and
                transition[1] == alphabet[symbol_index]):
                destination_state_closure = e_closures[transition[2]]
                index = new_state_index*len(alphabet) + symbol_index
                new_transitions[index][2] = new_transitions[index][2].union(destination_state_closure)

      # Adiciona os estados destinos que não foram apontados ainda
      for symbol_index in range(len(alphabet)):
        index = new_state_index*len(alphabet) + symbol_index
        destination_state = new_transitions[index][2]
        if (destination_state not in new_states and
            destination_state != set()):
          new_states.append(destination_state)

      new_state_index += 1
    # fim do while

    # Substitui os estados destinos por seu correspondente na lista de estados novos (e.g. {0, 1, 2} -> 0)
    # E remove as transições que transitam para um conjunto vazio de estados
    index = 0
    while (index < len(new_transitions)):
      destination_state = new_transitions[index][2]
      if destination_state == set():
        new_transitions.pop(index)
      else:
        new_transitions[index][2] = new_states.index(destination_state)
        index += 1

    # Atualiza os estados finais
    new_final_states = set()

    for i in range(len(new_states)):
      for old_final_state in self.final_states:
        if old_final_state in new_states[i]:
          new_final_states.add(i)

    self.final_states = new_final_states

    # Propriedades restantes atualizadas
    self.total_states = len(new_states)
    self.alphabet = set(alphabet)
    self.initial = 0
    self.transitions = new_transitions