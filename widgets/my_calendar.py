
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts



class CalendarWidget(qtw.QCalendarWidget):
    '''rewrite calendar widget so that he can highlight date where exist notes
     and particularly highlight current date'''

    # signal that received when pressed right click to delete record in calendar
    buttonClicked = qtc.pyqtSignal()

    def __init__(self, parent=None,
                 num_color='#000000',
                 normal_select='#E4BAD4',
                 file_color='#CAF7E3',
                 current_select='#e4a2c2',
                 list_d=qts.QSqlDatabase):
        super().__init__(parent,
                         verticalHeaderFormat=qtw.QCalendarWidget.NoVerticalHeader,
                         gridVisible=False)
        # find all child(i.e. date in cell) and apply to them tableOfView, that we can index them
        self.table = self.findChild(qtw.QTableView)
        # set filter
        self.table.viewport().installEventFilter(self)
        # set parameters
        self.num_color = num_color
        self.normal_select = normal_select
        self.file_color = file_color
        self.list_dates = list_d
        self.current_select = current_select

        self.change_color_text()

    def eventFilter(self, source, event):
        # eventfilter captured when pressed right click on the date and call menu to delete record attached to that date
        if (event.type() == qtc.QEvent.MouseButtonPress and
                event.buttons() == qtc.Qt.RightButton and
                source is self.table.viewport()):
            # create menu
            menu = qtw.QMenu(self)
            delete = qtw.QAction('Delete record')
            menu.addAction(delete)
            delete.setObjectName('right_click')
            # that connect point where we click to table where stored our child dates from calendar
            # and using even.pos() it find out what date we choose in the table of dates
            index = self.table.indexAt(event.pos())
            # set date on which we right cliced
            date = qtc.QDate().fromString(
                self.date_by_index(self.table.model().index(index.row(), index.column()), pageChanged=True),
                'yyyy-MM-dd')
            self.setSelectedDate(date)
            # bind with igntal that bind with delete method in main class
            delete.triggered.connect(lambda: self.buttonClicked.emit())
            # show our menu
            menu.exec_(self.mapToGlobal(event.pos()))
        return super(CalendarWidget, self).eventFilter(source, event)

    def first_date(self, pageChanged):
        # index(1,0) mnean 1 row and 0 column
        # i dont know why, but row indexes starts at 1 and column indexes  starts at 0, so index(1,0) mean that we extract first date in the page
        return self.date_by_index(
            self.table.model().index(1, 0), pageChanged)

    def last_date(self, pageChanged=False):
        # index(6,6) mean 6 row and 6 column or last date on the page,explanation above
        return self.date_by_index(
            self.table.model().index(6, 6), pageChanged)

    def date_by_index(self, index: qtc.QModelIndex, pageChanged=False):
        """ Return Date by index of model of QTableView """
        # if method call when page was changed
        if pageChanged:
            date = qtc.QDate(self.yearShown(),
                             self.monthShown(),
                             self.table.model().index(3, 3).data())
        else:
            date = self.selectedDate()
        day = index.data()
        mnth = date.month()  # current month always the same as current date
        if day > 15 and index.row() < 3:  # qcalendar always display 6 rows( and 0 - is header)
            mnth = date.month() - 1
        if day < 15 and index.row() > 4:
            mnth = date.month() + 1
        return qtc.QDate(date.year(), mnth, day).toString('yyyy-MM-dd')

    # set the same color on all numbers of date,
    # because in origin class, dates on saturday and sunday highlight idifferent color
    def change_color_text(self):
        for d in (qtc.Qt.Saturday, qtc.Qt.Sunday):
            fmt = self.weekdayTextFormat(d)
            fmt.setForeground(qtg.QColor(self.num_color))
            font = qtg.QFont()
            font.setFamily('Times')
            fmt.setFont(font)
            self.setWeekdayTextFormat(d, fmt)

    # main method for painting cells in calendar
    def paintCell(self, painter, rect, date):
        # smotthing circles
        painter.setRenderHint(qtg.QPainter.Antialiasing)
        # rect as main bodyfor ellipse
        r = qtc.QRect(qtc.QPoint(), min(rect.width(), rect.height()) * qtc.QSize(1, 1))
        r.moveCenter(rect.center())
        painter.setPen(qtc.Qt.NoPen)
        # paint selected dates
        if date == self.selectedDate():
            painter.setBrush(qtg.QColor(self.normal_select))
            painter.drawEllipse(r)
            painter.setPen(qtg.QPen(qtg.QColor(self.num_color)))
            painter.drawText(rect, qtc.Qt.AlignCenter, str(date.day()))
        # paint dates if on that date exist notes
        elif qtc.QDate.toString(date, 'yyyy-MM-dd') in self.list_dates:
            painter.setBrush(qtg.QColor(self.file_color))
            painter.drawEllipse(r)
            painter.setPen(qtg.QPen(qtg.QColor(self.num_color)))
            painter.drawText(rect, qtc.Qt.AlignCenter, str(date.day()))
        # paint current date
        elif date == date.currentDate():
            painter.setBrush(qtg.QColor(self.current_select))
            painter.setPen(qtg.QColor(0, 0, 0, 0))
            painter.drawEllipse(r)
            painter.setPen(qtg.QPen(qtg.QColor(self.num_color)))
            painter.drawText(rect, qtc.Qt.AlignCenter, str(date.day()))
        # paint all other dates
        else:
            super(CalendarWidget, self).paintCell(painter, rect, date)