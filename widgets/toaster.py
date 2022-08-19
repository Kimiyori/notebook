
from PyQt5 import QtWidgets as qtw

from PyQt5 import QtCore as qtc



class QToaster(qtw.QFrame):
    '''Widget showing specific notification depending on transmitted text'''

    def __init__(self, *args, **kwargs):
        super(QToaster, self).__init__(*args, **kwargs)
        qtw.QHBoxLayout(self)

        self.setSizePolicy(qtw.QSizePolicy.Maximum,
                           qtw.QSizePolicy.Maximum)

        # alternatively:
        # self.setAutoFillBackground(True)
        # self.setFrameShape(self.Box)

        # here we set a timer,that triggered when timeout self.hide func and fade out at the end
        self.timer = qtc.QTimer(singleShot=True, timeout=self.hide)

        # here we set the opacity effect for animation
        self.opacityEffect = qtw.QGraphicsOpacityEffect(opacity=0)
        # and bind with self
        self.setGraphicsEffect(self.opacityEffect)
        # create opacity animation
        self.opacityAni = qtc.QPropertyAnimation(self.opacityEffect, b'opacity')
        self.opacityAni.setStartValue(0.)
        self.opacityAni.setEndValue(1.)
        self.opacityAni.setDuration(100)
        # and bind with self.checkClosed when it finish. It works as follows:
        # after finished animation opacityAni calls self.checkClosed, but our direction Forward, not Backward
        # so this call does nothing. After that it calls self.hide, because we set this func in out timer,that we start
        # in showMessage method and that method change direction on Backward and after that again call checkclosed
        # after finish animation and this time it really closed our QToaster.
        self.opacityAni.finished.connect(self.checkClosed)
        # now create move animation
        self.moveAnimation = qtc.QPropertyAnimation(self, b"pos")
        # and set duration much larger than opacity duration, so that our widget wiil fate in moving, not static
        self.moveAnimation.setDuration(2500)
        # set parameters for animation
        self.corner = qtc.Qt.BottomLeftCorner
        self.marginx = 40
        self.marginy = 70
        self.marginynew = 120

        # set corner and margin

    def checkClosed(self):
        # if we have been fading out, we're closing the notification
        if self.opacityAni.direction() == self.opacityAni.Backward:
            self.close()

    def hide(self):
        # #method that start hiding out frame
        self.opacityAni.setDirection(self.opacityAni.Backward)
        self.opacityAni.setDuration(500)
        self.opacityAni.start()

    def closeEvent(self, event):
        # as i understand deleteLater func need only for performans issues
        # we don't need the notification anymore, delete it!
        self.deleteLater()

    @staticmethod
    def showMessage(parent, message,
                    icon=qtw.QStyle.SP_MessageBoxInformation,
                    timeout=1500):

        self = QToaster(parent)
        parentRect = parent.rect()
        # in sets in out timer time and after it finished out frame star fading
        self.timer.setInterval(timeout)

        # use Qt standard icon pixmaps; see:
        # https://doc.qt.io/qt-5/qstyle.html#StandardPixmap-enum
        if isinstance(icon, qtw.QStyle.StandardPixmap):
            labelIcon = qtw.QLabel()
            self.layout().addWidget(labelIcon)
            icon = self.style().standardIcon(icon)
            size = self.style().pixelMetric(qtw.QStyle.PM_SmallIconSize)
            labelIcon.setPixmap(icon.pixmap(size))
        # set message aout succeess or fail
        self.label = qtw.QLabel(message)
        self.label.setObjectName('notification_text')
        self.layout().addWidget(self.label)
        # here we start our timer
        self.timer.start()

        # raise the widget and adjust its size to the minimum
        self.raise_()
        self.adjustSize()

        geo = self.geometry()
        # now the widget should have the correct size hints, let's move it to the
        # right place
        geo.moveBottomLeft(
            parentRect.bottomLeft() + qtc.QPoint(self.marginx, -self.marginy))
        self.moveAnimation.setStartValue(parentRect.bottomLeft() + qtc.QPoint(self.marginx, -self.marginy))
        self.moveAnimation.setEndValue(parentRect.bottomLeft() + qtc.QPoint(self.marginx, -self.marginynew))
        self.setGeometry(geo)
        self.show()
        self.moveAnimation.start()
        self.opacityAni.start()