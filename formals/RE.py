from dataclasses import dataclass, field
from ast import operand
from cmath import exp
from enum import Enum
from tkinter import W
from Tree import BinaryTree


class ExpressionType(Enum):
    unaryOperation = 1
    binaryOperation = 2
    operand = 3


def getType(char):
    if char == "*" or char == "+" or char == "?":
        return ExpressionType.unaryOperation

    if char == "|" or char == "·":
        return ExpressionType.binaryOperation

    if char.isalnum() or char == "(" or char == ")":
        return ExpressionType.operand

    print("ERROR")


@dataclass
class RE:

    definitions: list[tuple[str, str]]
    expressionsInUse: set[str] = field(default_factory=set)
    expressionsUntouched: set[str] = field(default_factory=set)

    def getDefinition(self, index):
        return self.definitions[index][0]

    def getExpression(self, index):
        return self.definitions[index][1]

    def setExpression(self, index, new_expression):
        self.definitions[index][1] = new_expression

    def openExpression(self, index):
        if self.getDefinition(index) in self.expressionsUntouched:
            self.expressionsUntouched.remove(self.getDefinition(index))

        if self.getDefinition(index) in self.expressionsInUse:
            print("Error")
        self.expressionsInUse.add(self.getDefinition(index))

        fragments = list()
        for i in range(len(self.definitions)):
            fragments = self.definitions[index][1].split(self.definitions[i])

            if len(fragments):
                if self.definitions[i] in self.expressionsInUse:
                    print("Error")

                if self.expressions[index] not in self.expressionsUntouched:
                    self.openExpression(self.expressions[index])

                newExpression = list()
                newExpression.fragments[0]

                for j in range(1, len(fragments)):
                    newExpression.append(self.expressions[index][i])
                    newExpression.append(fragments[j])

                self.setExpression("".join(newExpression))

        self.expressionsInUse.remove(self.expressions[index])

    def generateTree(self, expression_index) -> BinaryTree:

        expression = self.getExpression(expression_index)
        token = self.getDefinition(expression_index)

        # O primeiro símbolo tem de ser um operador
        currentType = getType(expression[0])
        if currentType != ExpressionType.operand:
            print("ERROR")

        # Inicializa a árvore
        tree = BinaryTree(token, expression[0])

        # Insere todos os símbolos da expressão na árvore
        for i in range(1, len(expression)):
            e = expression[i]

            lastType = currentType
            currentType = getType(e)

            if lastType == ExpressionType.binaryOperation:
                if currentType == ExpressionType.operand:
                    tree.insertRight(e)
                else:
                    print("ERROR")
            elif currentType == ExpressionType.operand:
                tree.insertAbove("·")
                tree.insertRight(e)
            else:
                tree.insertAbove(e)

        tree.fillTree

    def generateFAs(self):

        # Inicializa com todas as definições marcadas como intactas
        expresionsUntouched = set()
        for definition, _ in self.definitions:
            expresionsUntouched.add(definition[0])

        # Percorre todas as expressões (ignorando as já abertas)
        for i in range(len(self.definitions)):
            if self.definitions[i][0] in self.expressionsUntouched:
                self.openExpression(i)  # self.openExpression(i)

        self.trees = list()
        # Gera a árvore de cada expressão
        for expression_index in range(len(self.definitions)):
            self.trees.append(self.generateTree(expression_index))

        finite_automatas = list()
        # Gera o autômato de cada árvore
        for tree in self.trees:
            finite_automatas.append(tree.generateFA())

        return finite_automatas
