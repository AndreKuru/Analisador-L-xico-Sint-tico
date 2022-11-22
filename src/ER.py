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

class ER:

  def __init__(self, definitions, expressions) -> None:
    trees = list()

    count = 0
    isNewExpression = False

    # Substitui todas definições por suas respectivas expressões em cada expressão existente
    while (isNewExpression == True and count < 50):
      isNewExpression = False

      for expression in expressions:
        fragments = list()
        for i in range(len(definitions)):
          fragments = expression.split(definitions(i))

          if (len(fragments)):
            isNewExpression = True
            newExpression = list()
            newExpression.fragments[0]

            for j in range(1, len(fragments)):
              newExpression.append(expression[i])
              newExpression.append(fragments[j])
            
            expression = ''.join(newExpression)
    
    if (count >= 50):
      print("ERROR")

    # Gera a árvore de cada expressão
    for expression in expressions:
      trees.append(generateTree(expression))

    # TODO
    # Define os nodos anuláveis
    # Gera tabela a partir da árvore
    # Gera automato a partir da tabela
