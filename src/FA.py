class FA:

  def __init__(self, total_states, alphabet, initial, final_states, transitions) -> None:
    self.total_states  = total_states
    self.alphabet      = alphabet
    self.initial       = initial
    self.final_states  = final_states
    self.transitions   = transitions

  def printFA(self):
    print(f"Número de estados: {self.total_states}")
    print(f"Estado inicial: {self.initial}") 
    print(f"Estados finais: {self.final_states}") 
    print(f"Alfabeto: {self.alphabet}") 
    print("Transições: ")
    for transition in self.transitions:
      print(transition)

  def checkNewStates(self, new_transitions, total_states):

    # while(len(total_states) < self.total_states * len(self.alphabet)):
    
      # 1 - Varre as transições verificando novos estados
      for transition in new_transitions:
        if transition[0] not in total_states.values():
          total_states[len(total_states)] = transition[0]
        if transition[2] not in total_states.values():
          total_states[len(total_states)] = transition[2]

        # 1.1 - Para cada novo estado, verifica as transições de seus subconjuntos
        current_state = total_states[len(total_states)-1]
        print('CURRENT STATE ' + str(current_state))
        for transition in new_transitions:
          # 1.2 - Ignora as transições do símbolo inicial
          if transition[0] == {0}:
            continue
          # 1.3 - Se encontra um subconjunto, une com o novo estado
          if transition[0].issubset(current_state):
            transition[0] = transition[0].union(current_state)
          if transition[2].issubset(current_state):
            transition[2] = transition[2].union(current_state)

        # 1.4 - Varre novamente as transições
        for transition1 in new_transitions:
          source_state = transition1[0]
          symbol = transition1[1]
          for transition2 in new_transitions:
            # 1.5 - Comparando os estados fonte e o símbolo de transição
            if (source_state.issubset(transition2[0]) and
                transition2[1] == symbol):
              transition2[2] = transition2[2].union(transition1[2])

        '''for symbol in self.alphabet:
          if [current_state, symbol] not in new_transitions:
            new_transitions.append([current_state, symbol, set()])'''

      print('--------------------------------')
      print(new_transitions)
      print('--------------------------')
      print(total_states)

  def determinizeFA(self):

    # 1 - Varrer transicoes em busca de transicoes pelo simbolo de palavra vazia
    if '&' in self.transitions:

      # 1.1 - Calcula os e-fechos do automato original
      e_closures = dict()
      # 1.1.1 - Adiciona o proprio estado ao seu e-fecho 
      for i in range(self.total_states):
        e_closure = set()
        e_closure.add(i)
        e_closure_aux = e_closure.copy()
        e_closures[i] = e_closure_aux
        e_closure.clear()

      # 1.1.2 - Adiciona demais estados alcançados por e-transicoes
      for transition in self.transitions:
        if '&' in transition:
          e_closure = set()
          e_closure_aux = e_closure.union(e_closures[transition[0]])
          e_closure_aux = e_closure_aux.union(e_closures[transition[2]])
          e_closure_aux = e_closures[transition[0]].union(e_closure_aux)
          e_closures[transition[0]] = e_closure_aux
          e_closure.clear()

      key_states = list(e_closures)

      new_states = dict()
      for i in range(self.total_states):
        if {key_states[i]} == e_closures[i]:
          new_states[i] = e_closures[i]
        else:  
          new_states[i + self.total_states - 1] = e_closures[i]

      print('ESTADOS NOVOS MAPEADOS')
      print(new_states)

      '''1.3 - Define o e-fecho do estado inicial do automato original
            como estado inicial do automato resultante'''

      initial = key_states[0]

      '''1.4 - Define os conjuntos de estados que contem algum estado final do automato
            original como estados finais do automato resultante'''
      
      final_states = dict()

      for (index, state) in new_states.items():
        for final_state in self.final_states:
          if final_state in state:
            final_states[index] = state

      # 1.5 - As novas transicoes passam a ser a união dos e-fecho de cada transicao do estado novo

      alphabet_aux = self.alphabet.copy()
      transitions = list()
      for state in new_states.values():
        for sign in alphabet_aux:
          transitions.append([state, sign, set()])

      for transition in self.transitions:
        for i in range(len(transitions)):
          
          if transition[0] in transitions[i][0] and transition[1] == transitions[i][1]:
            transitions[i][2] = transitions[i][2].union(e_closures[transition[2]])

      for (index, state) in new_states.items():
        for transition in transitions:
          if state == transition[0]:
            transition[0] = index
          if state == transition[2]:
            transition[2] = index

      DFA = FA.FA(len(new_states), self.alphabet, initial, list(final_states), transitions)
      
      return DFA

    # 2 - Se nao
    else:
      # 2.1 - Criar conjunto de estados
      total_states = {}
      for i in range(self.total_states):
        total_states[i] = {i}

      # 2.2 - Percorrer as transições e criar novos estado atingidos
      new_transitions = []
      for read_transition in self.transitions:
        read_transition_is_new = True
        for new_transition in new_transitions:
          if (read_transition[0] in new_transition[0] and
            read_transition[1] == new_transition[1]):
            read_transition_is_new = False
            new_transition[2].add(read_transition[2])
            pass
        if read_transition_is_new:
          new_transitions.append([{read_transition[0]}, read_transition[1], {read_transition[2]}])

      print(new_transitions)

      #while len(new_transitions) < (self.total_states * len(self.alphabet)):
      self.checkNewStates(new_transitions, total_states)


      '''NAO ESTA FUNCIONANDO AINDA'''

      # 2.3 - Gerar conjunto de estados finais

      # 2.4 - Gerar producoes

        # 2.4.1 - Para cada estado novo do conjunto potencia

        # 2.4.2 - Para cada simbolo do alfabeto

      '''2.4.3 - Adicionar producao ao conjunto de producoes,
              se nas transicoes originais existia uma transicao
              de um estado contido no estado novo pelo simbolo'''

    pass