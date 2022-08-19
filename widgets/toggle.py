
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class Toggle(qtw.QCheckBox):
    '''widget for switch style themes'''

    def __init__(
            self,
            width=60,
            bg_color='#E4BAD4',
            circle_color='#CAF7E3',
            animation_curve=qtc.QEasingCurve.OutBounce
    ):
        super().__init__()
        self.setFixedSize(width, 28)
        self.setCursor(qtc.Qt.PointingHandCursor)
        self.bg_color = bg_color
        self.circle_color = circle_color
        self._circle_position = 3
        self.animation = qtc.QPropertyAnimation(self, b'circle_position', self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)
        self.stateChanged.connect(self.start_transition)

    @qtc.pyqtProperty(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def start_transition(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(3)
        self.animation.start()

    # method that extend hit area to all visible widget zone
    def hitButton(self, pos: qtc.QPoint):
        return self.contentsRect().contains(pos)

    # main paint method
    def paintEvent(self, e):
        paint = qtg.QPainter(self)
        # smoothing borders
        paint.setRenderHint(qtg.QPainter.Antialiasing)
        # off outline
        paint.setPen(qtc.Qt.NoPen)

        rect = qtc.QRect(0, 0, self.width(), self.height())
        if not self.isChecked():
            paint.setBrush(qtg.QColor(self.bg_color))
            paint.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)
            paint.setBrush(qtg.QColor(self.circle_color))
            paint.drawEllipse(int(self._circle_position), 3, 22, 22)
        else:
            paint.setBrush(qtg.QColor(self.bg_color))
            paint.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)
            paint.setBrush(qtg.QColor(self.circle_color))
            paint.drawEllipse(int(self._circle_position), 3, 22, 22)

        paint.end()