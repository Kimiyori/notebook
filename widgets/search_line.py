
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class Search_line_edit(qtw.QLineEdit):
    # send signal when clicked and that trigger out method, that we bind in main class
    buttonClicked = qtc.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # seticon through QAction
        self.icon = qtg.QIcon(':/teams/lens.png')
        self.a = qtw.QAction(self.icon, 'search', self)
        # bind click and signal
        self.a.triggered.connect(lambda: self.buttonClicked.emit())
        # add our Icon on the right side of lineedit
        self.addAction(self.a, qtw.QLineEdit.TrailingPosition)