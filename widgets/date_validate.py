

from PyQt5 import QtGui as qtg


from datetime import datetime


class DateValidator(qtg.QValidator):
    '''Enforce entry of Date'''

    # Here we indicate the conditions that the search line must follow
    def validate(self, string, index):
        octets = string.split('-')
        # indicates that '-' cannot be deleted
        if len(octets) != 3:
            state = qtg.QValidator.Invalid
        # all symbols must me integers
        elif not all([x.isdigit() for x in octets if x != '']):
            state = qtg.QValidator.Invalid
        # year  must be before current year
        elif octets[0] and int(octets[0]) > datetime.now().year:
            state = qtg.QValidator.Invalid
        # month must be from 1 to 12
        elif octets[1] and int(octets[1]) > 12:
            state = qtg.QValidator.Invalid
        # day must be from 1 to 31
        elif octets[2] and int(octets[2]) > 31:
            state = qtg.QValidator.Invalid
        # any other case is acceptable
        else:
            state = qtg.QValidator.Acceptable
        return (state, string, index)