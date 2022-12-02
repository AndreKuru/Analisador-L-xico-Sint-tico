class Node:
  def __init__(self, data, above, left, right, nullable):
    self.__data = data
    self.__above = above
    self.__left = left
    self.__right = right
    self.__nullable = nullable

  # Setters
  def setRight(self, newNode):
    self.__right = newNode
  
  def setAbove(self, newNode):
    self.__above = newNode

  def setNullable(self, nullable):
    self.__nullable = bool(nullable)

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

  def getNullable(self):
    return self.__nullable

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

  # Insere mais um nodo entre o atual e o pai dele
  def insertAbove(self, data, nullable):
    newNode = Node(data, self.currentNode.getAbove(), self.currentNode, None, nullable)
    self.currentNode.setAbove(newNode)
    self.currentNode = newNode

  def insertAbove(self, newNode):
    self.currentNode.setAbove(newNode)
    self.currentNode = newNode

  # Insere mais um nodo entre o atual e o filho mais a direita
  def insertRight(self, data, nullable):
    newNode = Node(data, self.currentNode, None, self.currentNode.getRight(), nullable)
    self.currentNode.setRight(newNode)
    self.currentNode = newNode

  def insertRight(self, newNode):
    self.currentNode.setRight(newNode)
    self.currentNode = newNode

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

  def setNullable(self, node):
    if (node.getLeft() != None):
      setNullable(node.getLeft())
    if (node.getRight() != None):
      setNullable(node.getRight())

    if (node.getNullable() != True):
      if (node.getData() == "."):
        if (node.getLeft.getNullable and node.getRight.getNullable):
          node.setNullable(True)
        else:
          node.setNullable(False)
          
      if (node.getData() == "|"):
        if (node.getLeft.getNullable or node.getRight.getNullable):
          node.setNullable(True)
        else:
          node.setNullable(False)

      if (node.getData() == "+"):
        if (node.getLeft.getNullable()):
          node.setNullable(True)
        else:
          node.setNullable(False)
