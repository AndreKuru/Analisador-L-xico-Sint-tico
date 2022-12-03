class Node:
  def __init__(self, data, above, left, right):
    self.__data = data
    self.__above = above
    self.__left = left
    self.__right = right
    self.nullable = False
    self.pos = None
    self.firstpos = set()
    self.lastpos = set()

  # Setters
  def setRight(self, newNode):
    self.__right = newNode
  
  def setAbove(self, newNode):
    self.__above = newNode

  # Getters
  def getData(self):
    return self.__data

  def getLeft(self):
    return self.__left

  def getRight(self):
    return self.__right

  def getAbove(self):
    return self.__above

  def getAboveData(self):
    if (self.above == None):
      print("Error")
    return self.__above.getData()

  # Others
  def isLeaf(self) -> bool:
    if (self.__right == None and
        self.__left == None):
      return True
    else:
      return False

class BinaryTree:

  # Inicializa a árvore com um ponteiro para o nodo atual
  def __init__(self, data):
    self.currentNode = Node(data, None, None, None, False)
    self.highestPos = 0

  # Insere mais um nodo entre o atual e o pai dele
  def insertAbove(self, data):
    newNode = Node(data, self.currentNode.getAbove(), self.currentNode, None)
    self.currentNode.setAbove(newNode)
    self.currentNode = newNode

#  def insertAbove(self, newNode):
#    self.currentNode.setAbove(newNode)
#    self.currentNode = newNode

  # Insere mais um nodo entre o atual e o filho mais a direita
  def insertRight(self, data):
    newNode = Node(data, self.currentNode, None, self.currentNode.getRight())
    self.currentNode.setRight(newNode)
    self.currentNode = newNode

#  def insertRight(self, newNode):
#    self.currentNode.setRight(newNode)
#    self.currentNode = newNode

  # Percorre os pais até achar um parentêse, remove da árvore e define o filho dele como nodo atual
  def closeBracket(self):

    if (self.currentNode == '('):
      print("ERROR")

    while (self.currentNode.getData() != '('):
      self.currentNode = self.currentNode.getAbove()
      if (self.currentNode == None):
        print("ERROR")

    # Remove o nodo com paretêse
    above = self.currentNode.getAbove()
    right = self.currentNode.getRight()
    above.setRight(right)
    right.setAbove(above)
    self.currentNode = right

  # Percorre todos os pais e define a raiz como nodo atual
  def setCurrentNodeToRoot(self):
    while (self.currentNode.getAbove() != None):
      self.currentNode = self.currentNode.getAbove()

#  # Checa e define o nodo passado como anulável de acordo com seu valor e filhos
#  def setIfNullable(self, node):
#    if (node.getLeft() != None):
#      self.setIfNullable(node.getLeft())
#    if (node.getRight() != None):
#      self.setIfNullable(node.getRight())
#
#    if (not node.getNullable()):
#      if (node.getData() == "."):
#        if (node.getLeft.getNullable and node.getRight.getNullable):
#          node.setNullable(True)
#        else:
#          node.setNullable(False)
#          
#      if (node.getData() == "|"):
#        if (node.getLeft.getNullable or node.getRight.getNullable):
#          node.setNullable(True)
#        else:
#          node.setNullable(False)
#
#      if (node.getData() == "+"):
#        if (node.getLeft.getNullable()):
#          node.setNullable(True)
#        else:
#          node.setNullable(False)

  # Percorre pelos nodos filhos recursivamente e define firstpos, lastpos de cada um
  # além do pos das folhas e
  # se o nodo é anulável
  def generateFirstposLastposPosNullable(self, node):
    if (node.getLeft() != None):
      self.generateFirstposLastposPosNullable(node.getLeft())
    if (node.getRight() != None):
      self.generateFirstposLastposPosNullable(node.getRight())

    # Se o nodo é folha
    if (not node.getLeft() and 
        not node.getRight()):

      self.highestPos += 1
      node.pos = self.highestPos
      node.firstpos.add(self.highestPos)
      node.lastpos.add(self.highestPos)
    
    # Se o nodo é uma operação
    else:
      if (node.getData() == '*' or
          node.getData() == '?'):

          node.firstpos.add(node.getLeft().firstpos)
          node.lastpos.add(node.getLeft().lastpos)
          node.nullable = True
        
      if (node.getData() == '+'):

          node.firstpos.add(node.getLeft().firstpos)
          node.lastpos.add(node.getLeft().lastpos)

          if (node.getLeft().nullable == True):
            node.nullable = True

      if (node.getData() == '|'):

          node.firstpos.add(node.getLeft().firstpos)
          node.firstpos.add(node.getRight().firstpos)

          node.lastpos.add(node.getLeft().lastpos)
          node.lastpos.add(node.getRight().lastpos)

          if (node.getLeft().nullable == True or
              node.getRight().nullable == True):
            node.nullable = True

      if (node.getData() == '.'):

          node.firstpos.add(node.getLeft().firstpos)
          if (node.getLeft().nullable == True):
            node.firstpos.add(node.getRight().firstpos)

          node.lastpos.add(node.getRight().lastpos)
          if (node.getRight().nullable == True):
            node.lastpos.add(node.getLeft().lastpos)

          if (node.getLeft().nullable == True and
              node.getRight().nullable == True):
            node.nullable = True

  # TODO followpos
  # TODO automato (definir estados e transições)