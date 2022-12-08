from dataclasses import dataclass
import sys
import os


@dataclass
class FrozenGM:

    noterminals: list[str]
    terminals: list[str]
    initial: str
    productions: list[tuple[int, list[int | str]]]


@dataclass
class GM:

    noterminals: set[str]
    terminals: set[str]
    initial: str
    productions: dict[str, set[str]]

    def printGM(self):
        print(f"{self.noterminals}")
        print(f"{self.terminals}")
        print(f"{self.initial}")
        print(f"{self.productions}")
        for i in self.productions:
            print(f"{i} -> {self.productions[i]}")

    def eliminateLR(self):
        auxdic = dict()
        for i in self.productions:
            id = 0
            index = 0
            nonterminal = list(self.productions[i])

            # A → A α |β
            nonterminal = [i.replace(" ", "") for i in nonterminal[index].split("|")]
            nt = nonterminal[id][0]
            auxdic[f"{nt}"] = list()
            auxdic[f"{nt}'"] = list()
            a = []
            for j in range(len(nonterminal)):
                if nonterminal[j][index] == i:
                    if nonterminal[j][index + 1] != i:
                        if nonterminal[j][index + 1] == nonterminal[j][index + 2]:
                            a.append(str(nonterminal[j][index + 1] * 2))
                        else:
                            a.append(nonterminal[j][index + 1])

                    print("there's left recursion")

                    id += 1
                    if index >= 0:
                        if len(nonterminal[id]) > 1:
                            b = nonterminal[id][-1]
                        else:
                            b = nonterminal[id][-1]
                        # A → βA′
                        auxdic[f"{nt}"] = f"{b}{nt}'"
                        print(f"{nt}->{b}{nt}'")
                        txt = ""
                        for w in a:
                            txt += f"{w}{b}{nt}'|"
                        txt += "&"
                        auxdic[f"{nt}'"] = txt
                        # A → αA′|ϵ
                        # print(txt)

                    id = 0
        print(auxdic["("])
        for key, value in auxdic.items():
            if key.isalpha() or key[0].isalpha():
                strValue = str(value)
                self.productions[key] = set([strValue])
        for key, value in self.productions.items():
            print(key, value)

    def factoring():
        pass




"""initial, productions, noterminals, terminals = readGM(sys.argv[1])
gm = GM(noterminals, terminals, initial, productions)
gm.eliminateLR()
gm.printGM()
"""
