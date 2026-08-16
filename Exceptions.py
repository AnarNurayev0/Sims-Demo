class NotFoundError(Exception):
    def __init__(self, message = 'This item is not found'):
        self.message = message
        super().__init__(self.message)

#_______________________________________________________________________________________#
