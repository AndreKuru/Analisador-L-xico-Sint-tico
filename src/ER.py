from ast import operator
from cmath import exp
from enum import Enum
from tkinter import W
from Tree import BinaryTree

class ExpressionType(Enum):
  unaryOperation  = 1
  binaryOperation = 2
  operator        = 3

def getType(char):
  if (char == '*' or
      char == '+' or
      char == '?'
     ):
    return ExpressionType.unaryOperation

  if (char == '|' or
      char == '.'
     ):
    return ExpressionType.binaryOperation

  if (char.isalnum() or
      char == '(' or
      char == ')'
     ):
    return ExpressionType.operator
  
  print("ERROR")

def isNullable(char):
  if (char == '*' or
      char == '?'
     ):
     return True

  return False

def generateTree(expression):

    # O primeiro símbolo tem de ser um operador
    currentType = getType(expression[0])
    if (currentType != ExpressionType.operator):
      print("ERROR")

    # Inicializa a árvore
    tree = BinaryTree(expression[0])

    # Insere todos os símbolos da expressão na árvore
    for i in range(1, len(expression)):
      e = expression[i]

      lastType = currentType
      currentType = getType(e)
      nullable = isNullable(e)

      if (lastType == ExpressionType.binaryOperation):
        if (currentType == ExpressionType.operator):
          tree.insertRight(e, nullable)
        else:
          print("ERROR")
      elif (currentType == ExpressionType.operator):
        tree.insertAbove('.', False)
        tree.insertRight(e, nullable)
      else:
        tree.insertAbove(e, nullable)

#    # TODO
#    # Define os nodos anuláveis
#    # Gera tabela a partir da árvore
#    # Gera automato a partir da tabela

class ER:

  def __init__(self, definitions, self.expressions) -> None:
    self.definitions = definitions
    self.self.expressions = self.expressions
    self.expressionsInUse = set()
    self.expressionsUntouched = set(definitions)
    
  def openExpression(index):
    if (self.expressions[index] in self.expressionsUntouched):
      self.expressionsUntouched.remove(self.expressions[index])

    if (self.expressions[index] in self.expressionsInUse):
      print("Error")
    self.expressionsInUse.append(self.expressions[index])

    fragments = list()
      for i in range(len(self.definitions)):
        fragments = self.expressions[index].split(self.definitions[i])

        if (len(fragments)):
          if (self.definitions[i] in expressionsInUse)
            print("Error")
          
          if (self.expressions[index] not in expressionsUntouched)
            openExpression(self.expressions[index])
          
          newExpression = list()
          newExpression.fragments[0]

          for j in range(1, len(fragments)):
            newExpression.append(self.expressions[index][i])
            newExpression.append(fragments[j])
          
          self.expressions[index] ''.join(newExpression)

    self.expressionsInUse.remove(self.expressions[index])




  def generateAF():
    
  for i in range(len(self.expressions)):
    if (self.expressions[i] in self.expressionsUntouched):
      openExpression(i) # self.openExpression(i)

  self.trees = list()
  # Gera a árvore de cada expressão
  for expression in self.expressions:
    self.trees.append(generateTree(expression))

#
#
#    trees = list()
#
#    count = 0
#    isNewExpression = False
#
#    # Substitui todas definições por suas respectivas expressões em cada expressão existente
#    while (isNewExpression == True and count < 50):
#      isNewExpression = False
#
#      for self.expressions[index] in self.expressions:
#        fragments = list()
#        for i in range(len(definitions)):
#          fragments = self.expressions[index].split(definitions(i))
#
#          if (len(fragments)):
#            isNewExpression = True
#            newExpression = list()
#            newExpression.fragments[0]
#
#            for j in range(1, len(fragments)):
#              newExpression.append(self.expressions[index][i])
#              newExpression.append(fragments[j])
#            
#            self.expressions[index] = ''.join(newExpression)
#    
#    if (count >= 50):
#      print("ERROR")
#
#    # Gera a árvore de cada expressão
#    for self.expressions[index] in self.expressions:
#      trees.append(generateTree(self.expressions[index]))
#
#
