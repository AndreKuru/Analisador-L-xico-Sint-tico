class Node:
  def __init__(self, data, above, left, right):
    self.__data = data
    self.above = above
    self.left = left
    self.right = right
    self.nullable = False
    self.pos = None
    self.firstpos = set()
    self.lastpos = set()

  # Getters
  def getData(self):
    return self.__data

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
    self.posByValue = {}
    self.followpos = {}

  # Insere mais um nodo entre o atual e o pai dele
  def insertAbove(self, data):
    newNode = Node(data, self.currentNode.above, self.currentNode, None)
    self.currentNode.setAbove(newNode)
    self.currentNode = newNode

#  def insertAbove(self, newNode):
#    self.currentNode.setAbove(newNode)
#    self.currentNode = newNode

  # Insere mais um nodo entre o atual e o filho mais a direita
  def insertRight(self, data):
    newNode = Node(data, self.currentNode, None, self.currentNode.right)
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
      self.currentNode = self.currentNode.above
      if (self.currentNode == None):
        print("ERROR")

    # Remove o nodo com paretêse
    above = self.currentNode.above
    right = self.currentNode.right
    above.setRight(right)
    right.setAbove(above)
    self.currentNode = right

  # Percorre todos os pais e define a raiz como nodo atual
  def setCurrentNodeToRoot(self):
    while (self.currentNode.above != None):
      self.currentNode = self.currentNode.above

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

  # Percorre pelos nodos filhos recursivamente e define firstpos, lastpos de cada nodo
  # além do pos das folhas,
  # se o nodo é anulável e
  # os followpos
  def generateFirstposLastposPosNullable(self, node):
    if (node.left != None):
      self.generateFirstposLastposPosNullable(node.left)
    if (node.right != None):
      self.generateFirstposLastposPosNullable(node.right)

    # Se o nodo é folha
    if (not node.left and 
        not node.right):

      # E não for cadeia vazia
      if (node.getData() != "&"):
        # adiciona entrada na tabela dos followpos
        self.highestPos += 1
        self.followpos[self.highestPos] = set()

        # agrupa todos os pos de acordo com os seus valores
        if (node.getData() not in self.posByValue):
          self.posByValue[node.getData()] = {self.highestPos}
        else:
          self.posByValue[node.getData()].add(self.highestPos)

        # define o pos, firstpos e lastpos
        node.pos = self.highestPos
        node.firstpos.add(self.highestPos)
        node.lastpos.add(self.highestPos)

        # a folha sempre será não-anulável quando não for cadeia vazia
    
    # Se o nodo é uma operação
    else:
      if (node.getData() == '*'):

          # firstpost, lastpos e nullable
          node.firstpos.add(node.left.firstpos)
          node.lastpos.add(node.left.lastpos)
          node.nullable = True

          # followpos
          for element in node.lastpos:
            self.followpos[element].add(node.firstpos)
        
      if (node.getData() == '?'):

          # firstpost, lastpos e nullable
          node.firstpos.add(node.left.firstpos)
          node.lastpos.add(node.left.lastpos)
          node.nullable = True
        
      if (node.getData() == '+'):

          # firstpost e lastpos
          node.firstpos.add(node.left.firstpos)
          node.lastpos.add(node.left.lastpos)

          # nullable
          if (node.left.nullable == True):
            node.nullable = True

      if (node.getData() == '|'):

          # firstpos
          node.firstpos.add(node.left.firstpos)
          node.firstpos.add(node.right.firstpos)

          # lastpos
          node.lastpos.add(node.left.lastpos)
          node.lastpos.add(node.right.lastpos)

          # nullable
          if (node.left.nullable == True or
              node.right.nullable == True):
            node.nullable = True

      if (node.getData() == '.'):

          # firstpos
          node.firstpos.add(node.left.firstpos)
          if (node.left.nullable == True):
            node.firstpos.add(node.right.firstpos)

          # lastpos
          node.lastpos.add(node.right.lastpos)
          if (node.right.nullable == True):
            node.lastpos.add(node.left.lastpos)

          # nullable
          if (node.left.nullable == True and
              node.right.nullable == True):
            node.nullable = True

          # followpos
          for element in node.left.lastpos:
            self.followpos[element].add(node.right.firstpos)

  # TODO automato (definir estados e transições)