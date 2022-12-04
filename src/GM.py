import sys
import os

class GM:
    def __init__(self, noterminals, terminals, initial, productions) -> None:
        self.noterminals = noterminals
        self.terminals   = terminals
        self.initial     = initial
        self.productions = productions

    def printGM(self):
        print(f"{self.noterminals}")
        print(f"{self.terminals}")
        print(f"{self.initial}")
        print(f'{self.productions}')
        for i in self.productions:
            print(f"{i} -> {self.productions[i]}")

    def eliminateLR(self):
        for i in (self.productions):
            id = 0
            index = 0
            nonterminal = list(self.productions[i])

            #A → A α |β
            nonterminal = [i.replace(' ', '') for i in nonterminal[index].split('|')]
            nt = nonterminal[id][0]
            a = []
            for j in range(len(nonterminal)): 
                if nonterminal[j][index] == i:
                    a.append(nonterminal[j][index+1])
                    
                    print('there\'s left recursion')

                    id += 1
                    if index >= 0:
                        if len(nonterminal[id]) > 1:
                            b = nonterminal[id][index+1]
                        else:
                            b = nonterminal[id][index]
                        #A → βA′
                        txt = f'{nt}\'->'
                        for w in a:
                            txt += f'{w}{nt}\'|'
                        txt += '&'
                        print(f"{nt}->{b}{nt}'") 
                        #A → αA′|ϵ
                        print(txt)
                    id = 0
         
    def factoring():
        pass

def readGM(file):
    file = open(f'tests/{file}', 'r')
    file_rows = file.readlines()
    file_rows = [rows.rstrip("\n") for rows in file_rows]
    

    initial       = str(file_rows[0][0])  # Producao inicial
    productions = dict()                  # dicionario contendo todas as producoes

    # codigo responsável por ler a Gramatica e encontrar as producoes
    for i in range(len(file_rows)):
        file_one_row = file_rows[i].split(" -> ")
        productions[file_one_row[0]] = {file_one_row[1]}
        productions[file_one_row[0]].add(file_one_row[1])
    

    noterminals    = set(file_rows[row][0] for row in range(0,len(file_rows))) # conjunto de nao terminais da gramática


    # parte responsável por encontrar os não terminais da gramática
    new_fragments = []
    fragments = []
    # vare todas os values do dicionario e separa as producoes por "|"
    for k in productions.keys():
       fragments += productions[k]
    for production in fragments:
       new_fragments += production.split(" | ")
    fragments = new_fragments
    new_fragments = []
    # vare novamente a lista criada anteriormente e separa por todos os terminais para manter
    # somente os que são não terminais
    for noterminal in noterminals:
       for fragment in fragments:
           new_fragments += fragment.split(noterminal)
       fragments = new_fragments
       new_fragments = []

    return initial, productions, noterminals, fragments

    pass


initial, productions, noterminals, terminals = readGM(sys.argv[1])
gm = GM(noterminals, terminals, initial, productions)
gm.eliminateLR()
