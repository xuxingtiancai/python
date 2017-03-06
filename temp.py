class ContextController:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.old_value = globals()[name]
    def __enter__(self):
        globals()[self.name] = self.value
	  return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        globals()[self.name] = self.old_value

with ContextController('c_NoTargetCardRatio', 0) as context:
    response = self.GetPostRun(r'我想听音乐')
    self.assertTrue(response.ReplyText is not None)
