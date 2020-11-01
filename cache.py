class Cache():
  """Object for save variables between test"""

  def __init__(self):
    self.memory = {}

  def get_value(self, code):
    return self.memory.get(code, None)

  def set_value(self, code, value):
    self.memory[code] = value
