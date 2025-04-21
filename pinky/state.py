class Environment:
  def __init__(self, parent=None):
    self.vars = {}       # A dictionary to store variable names and their values
    self.parent = parent # Parent environemt (optional)

  def get_var(self, name):
    #TODO:
    pass

  def set_var(self, name, value):
    #TODO:
    pass

  def new_env(self):
    '''
    Return a new environment that is a child of the current one.
    This is used to create a new nested scope (while, funcs, etc.)
    '''
    return Environment(parent=self)
