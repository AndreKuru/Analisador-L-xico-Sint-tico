from dataclasses import dataclass
import copy
import random

<<<<<<< HEAD
=======

def xsearch(old_class, transition):
    i = 0
    while i < len(old_class):
        for x in old_class[i]:
            if x == transition:
                return i
        i += 1
    return len(old_class)
>>>>>>> fa77cb202ea132402aa747848f068697559ce215


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
<<<<<<< HEAD
                return int(t[2])
    
    def runFA(self, entry) -> tuple[str, str, str]:
=======
                return t

    # Roda o automato e retorna (token, lexema, entrada restante)
    def run(self, entry) -> tuple[str, str, str]:
>>>>>>> fa77cb202ea132402aa747848f068697559ce215
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
        self.discardDead()
        self.discardUnreach()
        self.mergeClasses()
        #   # remover estados inalcançaveis
        #   reach = set([self.initial])
        #   new = set([self.initial])
        #   
        #   while len(new):
        #       aux = set()
        #       for state in new:
        #           for symbol in self.alphabet:
        #               if (self.transition(state, symbol)) not in reach:
        #                   aux.add(self.transition(state, symbol))
        #               

        #       reach = reach.union(aux)
        #       new = aux

<<<<<<< HEAD
        #   unreach = set([self.transitions[i][0] for i in range(len(self.transitions))]) - reach
        #   for i in range(len(self.transitions)):
        #       if i >= len(self.transitions):
        #           break
        #       elif not self.transitions[i][0] in reach:
        #           self.transitions.remove(self.transitions[i])
        #   
        #   newfinal = {}
        #   for i in reach:
        #       for token in self.final_states:
        #           if i in self.final_states[token]:
        #               newfinal[token] = i
        #   self.final_states = {i for i in reach if i in self.final_states['token_generic']}
        #   # remover estados morto
        #   alive = self.final_states
        #   new = self.final_states

        #   while len(new):
        #       aux = set()
        #       
        #       for i in self.transitions:
        #           if self.transition(i[0], i[1]) in alive:
        #               if i[0] not in alive:
        #                   aux.add(i[0])
        #       alive = alive.union(aux)
        #       new = aux

        #   dead = set([self.transitions[i][0] for i in range(len(self.transitions))]) - alive
        #   
        #   for i in range(len(self.transitions) - 1):
        #       if i >= len(self.transitions):
        #           break
        #       else:
        #           if self.transitions[i][0] not in alive:
        #               self.transitions.remove(self.transitions[i])

        #   # classes de equivalencia
        #   old_class = [
        #       self.final_states,
        #       set(
        #           [self.transitions[i] for i in range(len(self.transitions))]
        #       ).difference(self.final_states),
        #   ]

        #   for i in old_class:
        #       new_class = []
        #
        #       if len(i) < 2:
        #           new_class.append(i)
        #           continue

        #       pair = list(combinations(i, 2))
        #       for x in pair:
        #           same = True
        #           for z in self.alphabet:
        #               a, b = x
        #               if (xsearch(old_class, self.transition(a, z))) != (xsearch(old_class, self.transition(b, z))):
        #                   new_class.append(set(a))
        #                   new_class.append(set(b))
        #                   same = False
        #          
        #           insert = False
        #           if same:
        #               for classx in new_class:
        #                   if a in classx:
        #                       classx = classx.union(set(b))
        #                       insert = True
        #                   elif b in classx:
        #                       classx = classx.union(set(a))
        #                       insert = True

        #           if not insert:
        #               new_class.append({a, b})
        #   for i in self.transitions:
        #       print(i)


    def discardDead(self):
        
        last = set()
        alives = set()
        for token in self.final_states:
            for i in self.final_states[token]:
                alives.add(i)
        while last != alives:
            last = alives.copy()
            for token in self.transitions:
                transition = set([token[1], token[2]])
                if token[0] not in alives:  
                    for _ in self.transitions:
                        if _[2] == token[0]:
                                alives.add(token[0])   
        
        if self.initial not in alives:
            print("ERRO")
            return False
        
        dead = []
        dead_state = []
        
        for i in self.transitions:
            if i[0] not in alives:
                if i[0] not in dead:
                    dead.append(i[0])
                dead_state.append(i) 
        
        for i in dead_state: 
            self.transitions.remove(i)
        self.total_states -= len(dead)
        

=======
        # remover estados inalcançaveis
        reach = set([minimized.initial])
        new = set([minimized.initial])

        while len(new):
            aux = set()

            for state in new:
                for symbol in minimized.alphabet:
                    if (minimized.transition(state, symbol)) not in reach:
                        aux.add(minimized.transition(state, symbol))
>>>>>>> fa77cb202ea132402aa747848f068697559ce215

    def discardUnreach(self):

<<<<<<< HEAD
        reachable = {self.initial}
        last_reach = set()
=======
        unreach = (
            set(
                [minimized.transitions[i][0] for i in range(len(minimized.transitions))]
            )
            - reach
        )
        for i in range(len(minimized.transitions)):
            if i >= len(minimized.transitions):
                break
            elif not minimized.transitions[i][0] in reach:
                minimized.transitions.remove(minimized.transitions[i])
        minimized.final_states = {
            i for i in reach if i in minimized.final_states["token_generic"]
        }
>>>>>>> fa77cb202ea132402aa747848f068697559ce215

        for state in self.transitions:
            if state[0] in reachable:
                for i in self.transitions:
                    if i[0] == state[0]:
                        reachable.add(i[2])
        unreach = []
        unreach_state = []

<<<<<<< HEAD
        
        for i in self.transitions:
            if i[0] not in reachable:
                if i[0] not in unreach:
                    unreach.append(i[0])
                ureach_state.append(i) 
        for i in unreach_state: 
            self.transitions.remove(i)
        self.total_states -= len(unreach)

    def mergeClasses(self):


        final = set()
        non_final = set()
        for token in self.final_states:
            for i in self.final_states[token]:
                final.add(i)

        for transition in self.transitions:
            if transition[0] not in final:
                non_final.add(transition[0])

        classes = [non_final, final]
        last = []
        previous = []

        def findx(state):
            for class_e in last:
                if state in class_e:
                    return class_e
            return None
   
        def removex(state, classes):
            for i in classes:
                for state in i.copy():
                    i.remove(state)
            new_ = []
            for i in classes:
                if i:
                    new_.append(i)
            return new_

        def copyx(classes):
            new_ = []
            for i in classes:
                new_.append(i.copy())
            return new_

        while classes != previous:
            previous = copyx(last)
            for i in self.alphabet:
                last = copyx(classes)
                for e_class in last:
                    relation = []

                    for state in e_class:
                            for transition in self.transitions:
                                if transition[0] == state and transition[1] == i :
                                    target = findx(transition)
                                    listed = False

                    classes = removex(state, classes)
                    for r in relation:
                        if target == r[1]:
                            listed = True

                            for inner in classes:
                                if r[0] in inner:
                                    inner.add(state)
                    if not listed:
                        classes.append({state})
                    relation.append([state, target])

        statesx = []
        for classx in classes:
            new_s = None
            
            if self.initial in classx:
                new_s = self.initial
=======
        while len(new):
            aux = set()

            for i in minimized.transitions:
                if minimized.transition(i[0], i[1]) in alive:
                    if i[0] not in alive:
                        aux.add(i[0])
            alive = alive.union(aux)
            new = aux

        dead = (
            set(
                [minimized.transitions[i][0] for i in range(len(minimized.transitions))]
            )
            - alive
        )

        for i in range(len(minimized.transitions) - 1):
            if i >= len(minimized.transitions):
                break
>>>>>>> fa77cb202ea132402aa747848f068697559ce215
            else:
                try:
                    new_s = classx.pop()
                except KeyError:
                    print("Error")
            
            for transition in self.transitions:
                if transition[2] in classx:
                   transition[2] = new_s

<<<<<<< HEAD
            statesx.append(new_s)
        
        new_i = 0
        for transition in self.transitions.copy():
            if transition[0] in statesx:
                for token in self.final_states:
                    if transition[0] in self.final_states[token]:
                        self.final_states[token].remove(transition[0])
                self.transitions.remove(transition)
        for i in self.transitions.copy():
            if i[2] == transition[0]:
                try:
                    new_i = i[0], i[1], random.choice(list(self.final_states["token_generic"]))
                except KeyError:
                    print("ERROR")
                self.transitions.remove(i) 
        
        self.transitions.append(new_i)
        
        seen = []
        self.total_states = 0
        for i in self.transitions.copy():
            if type(i) == tuple:
                if i[0] not in seen:
                    self.total_states += 1
                    seen.append(i[0])

            if type(i) == int:
                self.transitions.remove(i)
                
        print(statesx)
        print(self.total_states) 
        print(self.alphabet)
        print(self.initial)
        print(self.final_states)
        for i in self.transitions:
            print(i)

        print("ok")
=======
        # classes de equivalencia
        old_class = [
            minimized.final_states,
            set(
                [minimized.transitions[i] for i in range(len(minimized.transitions))]
            ).difference(minimized.final_states),
        ]

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
                    if (xsearch(old_class, self.transition(a, z))) != (
                        xsearch(old_class, self.transition(b, z))
                    ):
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
        print("self")
        for i in self.transitions:
            print(i)
        print("minimized")
        for i in minimized.transitions:
            print(i)
>>>>>>> fa77cb202ea132402aa747848f068697559ce215
