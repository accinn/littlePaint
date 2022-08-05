class Pila:

  def __init__(self):
    self.items = []

  def apilar(self, x):
    self.items.append(x)

  def desapilar(self):
    if self.esta_vacia():
      raise ValueError('La pila esta vacia')
    return self.items.pop()

  def tope(self):
    return None if self.esta_vacia() else self.items[-1]

  def esta_vacia(self):
    return len(self.items) == 0
   
  def __str__(self):
    return str(self.items)

# preguntar sobre el control, porque no deshace hasta volver al original, es decir la grilla en su estado original?