
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc



class Tag_frame(qtw.QFrame):
    """Widget for frame that used to show tag on FlowLayout"""

    buttonClicked = qtc.pyqtSignal()

    def __init__(self, text=None):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        hbox = qtw.QHBoxLayout()
        hbox.setContentsMargins(4, 2, 4, 2)
        self.setLayout(hbox)
        self.label = qtw.QLabel(text)
        self.label.setObjectName('tt')
        hbox.addWidget(self.label, alignment=qtc.Qt.AlignLeft | qtc.Qt.AlignCenter)
        hbox.addStretch(10)
        self.x_button = qtw.QPushButton('')
        icon = self.style().standardIcon(qtw.QStyle.SP_TitleBarCloseButton)
        self.x_button.setIcon(qtg.QIcon(':/teams/close.png'))
        self.x_button.setSizePolicy(qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Maximum)
        self.x_button.clicked.connect(lambda: self.buttonClicked.emit())
        self.x_button.setObjectName('bb')
        self.x_button.setCursor(qtc.Qt.PointingHandCursor)
        hbox.addWidget(self.x_button)
        self.setObjectName('fram')