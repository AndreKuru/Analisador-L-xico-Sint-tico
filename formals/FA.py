from dataclasses import dataclass
from itertools import combinations
import copy

def xsearch(old_class,transition):
    i = 0

    while i < len(old_class):
        for x in old_class[i]:
            if x == transition:
                    return i
        i += 1
    
    return len(old_class)

@dataclass
class FA:

    total_states: int
    alphabet: set[str]
    initial: int
    final_states: dict[str, set[int]]
    # transitions: list[list[int | str]]
    transitions: list[tuple[int, str, int]]

    def transition(self, state, symbol):
        for t in self.transitions:
            if t[0] == state and t[1] == symbol:
                return int(t[2])
    
    def runFA(self, entry) -> tuple[str, str, str]:
        self.runState(self.initial, entry, "")

    def runState(self, current_state, lexeme, entry) -> tuple[str, str, str]:
        # Lê o primeiro símbolo da entrada
        symbol = entry[0]

        # Procura o próximo estado
        next_state = None
        for transition in self.transitions:
            if transition[0] == current_state and transition[1] == symbol:
                next_state = transition[2]
# Se próximo estado é morto retorna o token do estado atual (que deve ser final)
        if next_state == None:
            for token in self.final_states:
                if current_state in self.final_states[token]:
                    return (token, lexeme, entry)
            print("Error")

        # Se ainda resta entrada continua rodando
        if len(
            entry[
                1,
            ]
        ):
            return self.runState(
                next_state,
                lexeme + symbol,
                entry[
                    1,
                ],
            )

        # Se não soubrar entrada retorna o token do estado atual (que deve ser final)
        for token in self.final_states:
            if current_state in self.final_states[token]:
                return (
                    token,
                    lexeme + symbol,
                    entry[
                        1,
                    ],
                )

        print("Error")

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
            if "&" in transition:

                # Adiciona recursivamente em todos os closures que contem aquele estado origem
                origin_state = transition[0]
                for index in range(len(e_closures)):
                    if origin_state in e_closures[index]:
                        destination_state_closure = e_closures[transition[2]]
                        e_closures[index] = e_closures[index].union(
                            destination_state_closure
                        )

        new_states = list()
        new_states.append(e_closures[self.initial])

        # Inicialização para o while
        new_transitions = list()
        new_state_index = 0

        alphabet = list(self.alphabet)
        alphabet.remove("&")
        alphabet.sort()

        # While para completar todos estados e transições
        while new_state_index < len(new_states):

            # Inicializa todas as transições para o estado selecionado
            for symbol_index in alphabet:
                new_transitions.append([new_state_index, symbol_index, set()])

            # Busca por cada transição de cada estado nos novos estados (que são conjuntos dos estados antigos)
            # e mescla nas transições do estado novo
            for old_state in new_states[new_state_index]:
                for symbol_index in range(len(alphabet)):
                    for transition in self.transitions:
                        if (
                            transition[0] == old_state
                            and transition[1] == alphabet[symbol_index]
                        ):
                            destination_state_closure = e_closures[transition[2]]
                            index = new_state_index * len(alphabet) + symbol_index
                            new_transitions[index][2] = new_transitions[index][2].union(
                                destination_state_closure
                            )

            # Adiciona os estados destinos que não foram apontados ainda
            for symbol_index in range(len(alphabet)):
                index = new_state_index * len(alphabet) + symbol_index
                destination_state = new_transitions[index][2]
                if destination_state not in new_states and destination_state != set():
                    new_states.append(destination_state)

            new_state_index += 1
        # fim do while

        # Substitui os estados destinos por seu correspondente na lista de estados novos (e.g. {0, 1, 2} -> 0)
        # E remove as transições que transitam para um conjunto vazio de estados
        index = 0
        while index < len(new_transitions):
            destination_state = new_transitions[index][2]
            if destination_state == set():
                new_transitions.pop(index)
            else:
                new_transitions[index][2] = new_states.index(destination_state)
                index += 1

        # Gera novos estados finais
        new_final_states = dict()
        for token in self.final_states:
            new_final_states[token] = set()

        for i in range(len(new_states)):
            for token in self.final_states:
                for old_final_state in self.final_states[token]:
                    if old_final_state in new_states[i]:
                        new_final_states[token].add(i)

        # Atualiza todas propriedades
        self.total_states = len(new_states)
        self.alphabet = set(alphabet)
        self.initial = 0
        self.final_states = new_final_states

        self.transitions = list()
        for new_transition in new_transitions:
            self.transitions.append(tuple(new_transition))

    def minimizeFA(self):
        minimized = copy.deepcopy(self)

        #remover estados inalcançaveis
        reach = set([minimized.initial])
        new = set([minimized.initial])
        
        while len(new):
            aux = set()

            for state in new:
                for symbol in minimized.alphabet:
                    if (minimized.transition(state, symbol)) not in reach:
                        aux.add(minimized.transition(state, symbol))
                    

            reach = reach.union(aux)
            new = aux

        unreach = set([minimized.transitions[i][0] for i in range(len(minimized.transitions))]) - reach
        for i in range(len(minimized.transitions)):
            if i >= len(minimized.transitions):
                break
            elif not minimized.transitions[i][0] in reach:
                minimized.transitions.remove(minimized.transitions[i])
        minimized.final_states = {i for i in reach if i in minimized.final_states['token_generic']}

        #remover estados morto
        alive = minimized.final_states
        new = minimized.final_states


        while len(new):
            aux = set()
            
            for i in minimized.transitions:
                if minimized.transition(i[0], i[1]) in alive:
                    if i[0] not in alive:
                        aux.add(i[0])
            alive = alive.union(aux)
            new = aux

        dead = set([minimized.transitions[i][0] for i in range(len(minimized.transitions))]) - alive
        
        for i in range(len(minimized.transitions) - 1):
            if i >= len(minimized.transitions):
                break
            else:
                if minimized.transitions[i][0] not in alive:
                    minimized.transitions.remove(minimized.transitions[i])
        
        #classes de equivalencia
        old_class = [minimized.final_states, set([minimized.transitions[i] for i in range(len(minimized.transitions))]).difference(minimized.final_states)]
    
        for i in old_class:
            new_class = []
    
            if len(i) < 2:
                new_class.append(i)
                continue

            pair = list(combinations(i, 2))
            for x in pair:
                same = True
                for z in self.alphabet:
                    a, b = x
                    if (xsearch(old_class, self.transition(a, z))) != (xsearch(old_class, self.transition(b, z))):
                        new_class.append(set(a))
                        new_class.append(set(b))
                        same = False
               
                insert = False
                if same:
                    for classx in new_class:
                        if a in classx:
                            classx = classx.union(set(b))
                            insert = True
                        elif b in classx:
                            classx = classx.union(set(a))
                            insert = True

                if not insert:
                    new_class.append({a, b})
        
        print(new_class)
        print(new_class)
        print('self')
        for i in self.transitions:
            print(i)
        print("minimized")
        for i in minimized.transitions:
           print(i)
