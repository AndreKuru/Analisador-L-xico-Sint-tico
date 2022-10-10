class AF:

  def __init__(self, estados, estado_incial, estados_finais, alfabeto, transicoes) -> None:
    self.estados        = estados
    self.estado_inicial = estado_incial
    self.estados_finais = estados_finais
    self.alfabeto       = alfabeto
    self.transicoes     = transicoes

  def imprimirAF(self):
    print(f"Número de estados: {self.estados}")
    print(f"Estado inicial: {self.estado_inicial}") 
    print(f"Estados finais: {self.estados_finais}") 
    print(f"Alfabeto: {self.alfabeto}") 
    print("Transições: ")
    for transicao in self.transicoes:
      print(transicao)
