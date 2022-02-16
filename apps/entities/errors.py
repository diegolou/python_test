class APHSError (Exception):
  def __init__(self, code, message) -> None:
    self.code = code
    self.message = message
    super().__init__(self.message)
    
  def __str__(self) -> str:
    return f'{self.message}'

