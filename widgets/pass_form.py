
from PyQt5 import QtWidgets as qtw



class PasswordForm(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.password = qtw.QLineEdit(self)
        self.password.setEchoMode(qtw.QLineEdit.Password)
        self.password.setPlaceholderText('Enter password')
        loginLayout = qtw.QFormLayout()
        loginLayout.addRow("Password", self.password)
        self.buttons = qtw.QDialogButtonBox(qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.control)
        self.buttons.rejected.connect(self.reject)
        layout = qtw.QVBoxLayout(self)
        layout.addLayout(loginLayout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)
        self.show()
    def reject(self):
        self.close()
    def control(self):
        if self.password.text()==PASSWORD:
            MainWindow()
            self.close()