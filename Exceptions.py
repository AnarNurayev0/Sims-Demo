class InvalidGradeError(Exception):
    def __init__(self, message = 'Grade must be between 0 and 100'):
        self.message = message
        super().__init__(self.message)

#_______________________________________________________________________________________#

class EnrollmentError(Exception):
    def __init__(self, message = 'Student is already enrolled in this subject'):
        self.message = message
        super().__init__(self.message)

#_______________________________________________________________________________________#

class NotFoundError(Exception):
    def __init__(self, message = 'This item is not found'):
        self.message = message
        super().__init__(self.message)

#_______________________________________________________________________________________#

