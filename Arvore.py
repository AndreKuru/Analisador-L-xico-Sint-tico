class Node:
    def __init__(self, data, above, nullable, leaf):
        self.data = data
        self.left = none
        self.right = none
        self.above = above
        self.nullable = nullable

    def setLeft(self, newNode):
        self.left = newNode

    def setRight(self, newNode):
        self.right = newNode

class BinaryTree:
    def __init__(self, currentNode):
        self.currentNode = currentNode

    def insertAbove(self, newNode):
        self.newNode.setLeft(self.currentNode)
        self.currentNode = newNode

    def insertRight(self, newNode):
        self.currentNode.setRight(newNode)
        self.currentNode = newNode

