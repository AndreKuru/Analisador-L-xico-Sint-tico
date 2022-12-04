from ast import operand
from cmath import exp
from enum import Enum
from tkinter import W
from Tree import BinaryTree

class ExpressionType(Enum):
  unaryOperation  = 1
  binaryOperation = 2
  operand        = 3

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
    return ExpressionType.operand
  
  print("ERROR")

# def isNullable(char):
#   if (char == '*' or
#       char == '?'
#      ):
#      return True
# 
#   return False

def generateTree(expression):

  # O primeiro símbolo tem de ser um operador
  currentType = getType(expression[0])
  if (currentType != ExpressionType.operand):
    print("ERROR")

  # Inicializa a árvore
  tree = BinaryTree(expression[0])

  # Insere todos os símbolos da expressão na árvore
  for i in range(1, len(expression)):
    e = expression[i]

    lastType = currentType
    currentType = getType(e)

    if (lastType == ExpressionType.binaryOperation):
      if (currentType == ExpressionType.operand):
        tree.insertRight(e)
      else:
        print("ERROR")
    elif (currentType == ExpressionType.operand):
      tree.insertAbove('.')
      tree.insertRight(e)
    else:
      tree.insertAbove(e)

  tree.setCurrentNodeToRoot()

  # TODO automato (definir estados e transições)

class RE:

  def __init__(self, definitions, expressions) -> None:
    self.definitions = definitions
    self.expressions = expressions
    self.expressionsInUse = set()
    self.expressionsUntouched = set(definitions)
    
  def openExpression(self, index):
    if (self.expressions[index] in self.expressionsUntouched):
      self.expressionsUntouched.remove(self.expressions[index])

    if (self.expressions[index] in self.expressionsInUse):
      print("Error")
    self.expressionsInUse.append(self.expressions[index])

    fragments = list()
    for i in range(len(self.definitions)):
      fragments = self.expressions[index].split(self.definitions[i])

      if (len(fragments)):
        if (self.definitions[i] in self.expressionsInUse):
          print("Error")
        
        if (self.expressions[index] not in self.expressionsUntouched):
          self.openExpression(self.expressions[index])
        
        newExpression = list()
        newExpression.fragments[0]

        for j in range(1, len(fragments)):
          newExpression.append(self.expressions[index][i])
          newExpression.append(fragments[j])
        
        self.expressions[index] = ''.join(newExpression)

    self.expressionsInUse.remove(self.expressions[index])




  def generateFA(self):
    
    # Percorre todas as expressões (ignorando as já abertas)
    for i in range(len(self.expressions)):
      if (self.expressions[i] in self.expressionsUntouched):
        self.openExpression(i) # self.openExpression(i)

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
