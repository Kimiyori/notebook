import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtSql as qts
import re
import images
from stylesheets import stylesheet_dark, stylesheet_light
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
from widgets import my_calendar,date_validate,flow_layout,search_line,tag_frame,toaster,toggle

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        '''MainWindow constructor'''
        super().__init__()
        self.setWindowTitle('My Notebook')
        # ----------------
        # set window size
        # ----------------
        self.desktop = qtw.QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.setFixedSize(int(self.width / 2), int(self.height / 2))

        # create main Vbox widget
        layout = qtw.QVBoxLayout()
        # and populate it upper widget
        up = qtw.QWidget()
        layout.addWidget(up)
        # create Hbox layout for upper widget
        up_layout = qtw.QHBoxLayout()
        up.setLayout(up_layout)
        # create upper button that disclose left menu
        Menu_Button = qtw.QPushButton('Menu')
        Menu_Button.setObjectName('main_buttons')

        # create upper right toogle that switch styles
        self.toggle = toggle.Toggle()
        self.toggle.clicked.connect(self.change_style)
        # and append that widgets to upper layout
        up_layout.addWidget(Menu_Button, alignment=qtc.Qt.AlignLeft)
        up_layout.addWidget(self.toggle, alignment=qtc.Qt.AlignRight)

        # create bottomnmain widget that encompass textedit and left menu
        bottom_main_widget = qtw.QWidget()
        layout.addWidget(bottom_main_widget)
        # create layout for main botton widget
        bottom_main_layout = qtw.QHBoxLayout()
        bottom_main_widget.setLayout(bottom_main_layout)

        # start creating our side menu widgets
        self.sideMenuWidget = qtw.QWidget()
        # bind out windget with button
        Menu_Button.clicked.connect(lambda: self.slide_method(self.sideMenuWidget,
                                                              width=1,
                                                              newsize=300,
                                                              property=b'maximumWidth'))
        # set original width of side menu
        self.sideMenuWidget.setMaximumWidth(300)
        bottom_main_layout.addWidget(self.sideMenuWidget)
        # and set to side menu vbox layout
        sideMenuLayout = qtw.QVBoxLayout()
        self.sideMenuWidget.setLayout(sideMenuLayout)

        # connect to out sql database
        self.db = qts.QSqlDatabase.addDatabase('QSQLITE')

        self.db.setDatabaseName('diary.db')
        # check can we open database or not and if not we'll see error window
        if not self.db.open():
            qtw.QMessageBox.critical(
                None, 'DB Connection Error',
                'Could not open database file: '
                f'{self.db.lastError().text()}')
            sys.exit(1)

        # create variable for date format
        self.date_format = 'yyyy-MM-dd'
        # create list of sql dates
        # and fill our list_dates with these dates that will be transmitted to
        # custom calendarwidget for checking existing dates
        query = qts.QSqlQuery()
        query.prepare('SELECT date_of_the_day FROM main_table ')
        query.exec()
        self.list_date = []
        while query.next():
            self.list_date.append(query.value(0))

        # create open button, but later most likely i'll change this button to something else
        save_button = qtw.QPushButton('Save')
        save_button.setObjectName('main_buttons')
        save_button.clicked.connect(self.rewrite_or_insert_data)

        # create search buttons and widget
        search_button = qtw.QPushButton('Search')
        search_button.setObjectName('main_buttons')

        self.search_widget = qtw.QWidget()
        self.search_widget.setMaximumSize(250, 0)
        search_layout = qtw.QVBoxLayout()
        search_layout.setSpacing(15)
        self.search_widget.setLayout(search_layout)

        # create custom date search line for search widget
        self.search_line = search_line.Search_line_edit(self)
        self.search_line.setObjectName('settings_buttons')
        # set our validator for that line
        self.search_line.setValidator(date_validate.DateValidator())
        # and create completer for that line
        self.date_completer = qtw.QCompleter()
        self.date_completer.setMaxVisibleItems(10)
        self.model = qtc.QStringListModel(self.list_date)
        self.date_completer.setModel(self.model)
        # bind completer and line
        self.search_line.setCompleter(self.date_completer)
        # bind with search method button click and enter press
        self.search_line.buttonClicked.connect(self.search)
        self.search_line.returnPressed.connect(self.search)

        # create our line for tag search
        self.search_tag_line = search_line.Search_line_edit(self)
        self.search_tag_line.setPlaceholderText('Type the tags...')
        self.search_tag_line.setObjectName('settings_buttons')
        self.search_tag_line.buttonClicked.connect(self.search_tags)
        self.search_tag_line.returnPressed.connect(self.search_tags)
        # create completer for tag search line
        self.tags_completer = qtw.QCompleter()
        self.tags_completer.setMaxVisibleItems(10)

        # using sqlquery we populate tag_list all existingg tags
        tag_query = qts.QSqlQuery()
        self.tag_list = []
        tag_query.prepare('SELECT tag from tags')
        tag_query.exec()
        while tag_query.next():
            self.tag_list.append(tag_query.value(0))
        # set model for completer and bind with tag search line
        self.model_tags = qtc.QStringListModel(self.tag_list)
        self.tags_completer.setModel(self.model_tags)
        self.search_tag_line.setCompleter(self.tags_completer)

        # add to our search layout all search line
        search_layout.addWidget(self.search_line)
        search_layout.addWidget(self.search_tag_line)

        # when clicked on search button in side widget, our lines is revealed
        search_button.clicked.connect(lambda: self.slide_method(self.search_widget,
                                                                height=1,
                                                                newsize=250,
                                                                property=b'maximumHeight'))

        # create setting button
        settings_button = qtw.QPushButton('Settings')
        settings_button.setObjectName('main_buttons')
        # as always bind with animation
        settings_button.clicked.connect(lambda: self.slide_method(self.settings_menu,
                                                                  height=1,
                                                                  newsize=480,
                                                                  property=b'maximumHeight'))
        # now create our inner widgets for setting button
        self.fonts = qtw.QFontComboBox(self)
        self.fonts.currentFontChanged.connect(self.change_font)

        self.size = qtw.QSpinBox(
            self,
            value=12,
            maximum=100,
            minimum=2,
            prefix='Size ',
            singleStep=2
        )
        self.size.valueChanged.connect(self.change_size)

        self.L_button = qtw.QPushButton('')
        self.L_button.clicked.connect(self.leftAlign)
        self.L_button.setObjectName('settings_buttons')

        self.C_button = qtw.QPushButton('')
        self.C_button.clicked.connect(self.centerAlign)
        self.C_button.setObjectName('settings_buttons')

        self.R_button = qtw.QPushButton('')
        self.R_button.clicked.connect(self.rightAlign)
        self.R_button.setObjectName('settings_buttons')

        self.W_button = qtw.QPushButton('')
        self.W_button.clicked.connect(self.vcenterAlign)
        self.W_button.setObjectName('settings_buttons')

        self.bold_button = qtw.QPushButton('')
        self.bold_button.clicked.connect(self.bold)
        self.bold_button.setObjectName('settings_buttons')

        self.italics_button = qtw.QPushButton('')
        self.italics_button.clicked.connect(self.italics)
        self.italics_button.setObjectName('settings_buttons')

        self.underline_button = qtw.QPushButton('')
        self.underline_button.clicked.connect(self.underline)
        self.underline_button.setObjectName('settings_buttons')

        self.reset_button = qtw.QPushButton('')
        self.reset_button.clicked.connect(self.reset_font)
        self.reset_button.setObjectName('settings_buttons')

        self.Color_button = qtw.QPushButton('', clicked=self.coloropen)
        self.Color_button.setObjectName('settings_buttons')
        self.go_pixmap = qtg.QPixmap(qtc.QSize(32, 32))
        self.color = qtw.QColorDialog(self)
        self.go_pixmap.fill(qtg.QColor('#ffffff'))
        self.connect_icon = qtg.QIcon()
        self.connect_icon.addPixmap(self.go_pixmap)
        self.Color_button.setIcon(self.connect_icon)

        self.bullet_list_button = qtw.QPushButton('')
        self.bullet_list_button.clicked.connect(self.bulletlist)
        self.bullet_list_button.setObjectName('settings_buttons')

        self.number_list_button = qtw.QPushButton('')
        self.number_list_button.clicked.connect(self.numberlist)
        self.number_list_button.setObjectName('settings_buttons')
        # after created inner widgets create main widget for setting menu and layouts for it
        self.settings_menu = qtw.QWidget()
        self.settings_menu.setMaximumSize(250, 0)
        setting_layout = qtw.QVBoxLayout()
        self.settings_menu.setLayout(setting_layout)
        # add fonts and size to first layout
        setting_layout1 = qtw.QHBoxLayout()
        setting_layout.addLayout(setting_layout1)
        setting_layout1.addWidget(self.fonts)
        setting_layout1.addWidget(self.size)
        # and all all other widgets
        setting_layout2 = qtw.QHBoxLayout()
        setting_layout.addLayout(setting_layout2)
        setting_layout2.addWidget(self.L_button)
        setting_layout2.addWidget(self.C_button)
        setting_layout2.addWidget(self.R_button)
        setting_layout2.addWidget(self.W_button)
        setting_layout2.addWidget(self.bold_button)
        setting_layout2.addWidget(self.italics_button)
        setting_layout2.addWidget(self.underline_button)
        setting_layout2.addWidget(self.reset_button)
        setting_layout2.addWidget(self.Color_button)
        setting_layout2.addWidget(self.bullet_list_button)
        setting_layout2.addWidget(self.number_list_button)
        setting_layout2.setSpacing(0)

        # now create calendar
        self.calendar = my_calendar.CalendarWidget(self, list_d=self.list_date)
        self.calendar.setMaximumSize(350, 0)
        self.calendar.selectionChanged.connect(self.change_date)

        self.calendar.currentPageChanged.connect(
            lambda: self.changed_calendar_page(first_day=self.calendar.first_date(pageChanged=True),
                                               last_day=self.calendar.last_date(pageChanged=True)))
        self.calendar.buttonClicked.connect(self.delete_record)
        # and dont forget to add current date through calendar to our search line
        self.search_line.setText(self.calendar.selectedDate().toString(self.date_format))
        # and create calendar button that binds with animation method
        self.calendar_button = qtw.QPushButton('Calendar')
        self.calendar_button.setObjectName('main_buttons')
        self.calendar_button.clicked.connect(lambda: self.slide_method(self.calendar,
                                                                       height=1,
                                                                       newsize=250,
                                                                       property=b'maximumHeight'))
        # and add all of these widgets to our main layout side menu
        sideMenuLayout.addWidget(save_button)
        sideMenuLayout.addWidget(search_button)
        sideMenuLayout.addWidget(self.search_widget)
        sideMenuLayout.addWidget(settings_button)
        sideMenuLayout.addWidget(self.settings_menu)
        sideMenuLayout.addWidget(self.calendar_button)
        sideMenuLayout.addWidget(self.calendar)
        sideMenuLayout.addStretch(0)

        # create right widget, that show records of current day along with tags
        self.right_side_widget = qtw.QWidget()
        self.right_side_layout = qtw.QVBoxLayout()
        self.right_side_widget.setLayout(self.right_side_layout)
        # create widget that show notes for current day
        self.textedit = qtw.QTextEdit(acceptRichText=True)
        self.change_size()

        # create widget that show all tags associated with current date
        self.show_tags = qtw.QWidget()
        self.show_tags.setMinimumHeight(50)
        # create our flow layout
        self.layout_for_tags = flow_layout.FlowLayout()
        # and line for adding tags
        self.line_add_tag = qtw.QLineEdit(self, placeholderText='Type here')
        self.line_add_tag.returnPressed.connect(lambda: self.add_new_tag(self.line_add_tag.text(), new_tag=True))
        # setting that policy allow us to set minimum width of search line
        self.line_add_tag.setSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        self.line_add_tag.setMinimumSize(70, 20)
        # calling this function add our line_add_tag to our widget
        # in the initial stage, if, for example, this is a new post and there are no tags in it yet
        self.add_new_tag()
        # and after all of it set that layout to our main tag widget,
        # because if we dont do it, our place where we show tags will be arbitrary lenth
        self.show_tags.setLayout(self.layout_for_tags)
        # createimportant list:
        # stores, obviously, all tags for current day
        self.all_tags_for_curr_day = []

        # add two widgets that shows noted and tags for current day to our rightside widget
        self.right_side_layout.addWidget(self.textedit)
        self.right_side_layout.addWidget(self.show_tags)

        #sqlquery that used for searching by tags
        self.search_tag_query= qts.QSqlQuery()
        #and table, that shows result of a search
        self.table = qtw.QTableWidget(columnCount=3)
        self.table.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(
            1, qtw.QHeaderView.Stretch)
        self.table.doubleClicked.connect(
            self.get_record)
        # hee we create stacked widges that will be show us
        # either main widget with record of current day
        # or table that show results search for tags
        self.stack = qtw.QStackedWidget()

        self.stack.addWidget(self.table)

        # add widget with notes of curr day to stacked widget
        self.stack.addWidget(self.right_side_widget)
        self.stack.setCurrentWidget(self.right_side_widget)
        # and set to our main bottom layout stacked widget,
        # so all widgets that have to shows on the bottom right side must me added to stacked widget
        bottom_main_layout.addWidget(self.stack)

        # and after all of it we create now central widget for all widgets
        mainWidget = qtw.QWidget()
        mainWidget.setObjectName("widcol")
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

        # here we set a status bar, that count words and characters
        charcount_label = qtw.QLabel("Words: 0    Characters: 0")
        charcount_label.setObjectName('count_words')
        self.textedit.textChanged.connect(
            lambda: charcount_label.setText(
                f'''Words:{len(re.split("(?:(?:[^a-zA-ZА-я]+')|(?:'[^a-zA-ZА-я]+))|(?:[^a-zA-ZА-я']+)",
                                        self.textedit.toPlainText())) - 1}    Characters:{len(self.textedit.toPlainText())}'''))  # in process
        self.statusBar().addPermanentWidget(charcount_label)
        # variable that store date for update before change date
        self.date_for_update = qtc.QDate.currentDate().toString(self.date_format)

        self.set_text()
        # dynamically change style depending on the data on computer
        current_time = datetime.strftime(datetime.now(), "%H:%M:%S")
        start_time = "08:00:00"
        finish_time = "17:00:00"
        if start_time < current_time < finish_time:
            self.set_light_style()
        else:
            self.set_dark_style()
        self.show()

    def search_tags(self):
        # methos for search by tags
        tags = tuple(self.search_tag_line.text().split(','))
        if tags[0]:
            if any(x in self.tag_list for x in tags):
                if len(tags)==1:
                    tags=f"('{tags[0]}')"
                self.search_tag_query.prepare(f"""select m.date_of_the_day date,m.about_the_day text,group_concat(t.tag,'\n') tags
                                from tags t
                                INNER JOIN tagmap tm on t.id=tm.tag_id
                                INNER JOIN main_table m on m.id=tm.main_id
                                where tm.main_id in (SELECT  DISTINCT tm.main_id from tagmap tm
                                 INNER JOIN main_table m on m.id=tm.main_id
                                 INNER JOIN tags t on t.id=tm.tag_id
                                 where t.tag in {tags})
                                 group by tm.main_id
                                order by date(m.date_of_the_day)""" )
                #self.search_tag_query.bindValue(':tags',tags)
                #print(self.search_tag_query.lastError().text())
                self.search_tag_query.exec()
                data=[]
                while self.search_tag_query.next():
                    data.append((
                        self.search_tag_query.value(0),
                        BeautifulSoup(self.search_tag_query.value(1),'html.parser').get_text()[2:],
                        self.search_tag_query.value(2)
                                ))
                self.table.setRowCount(len(data))
                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        self.table.setItem(i, j, qtw.QTableWidgetItem(value))
                self.stack.setCurrentWidget(self.table)
            else:
                toaster.QToaster.showMessage(self, 'None of these tags were found!')
        else:
            toaster.QToaster.showMessage(self, 'Enter the tags!')

    def get_record(self):
        index=self.table.item(self.table.currentRow(),0).text()
        date = qtc.QDate.fromString(index, self.date_format)
        if date!=self.calendar.selectedDate(): 
            self.calendar.setSelectedDate(date)
        else:
            self.stack.setCurrentWidget(self.right_side_widget)

    def delete_tag(self):
        # method that delete tag from current date
        # sender identifies the widget that sent the delete signal and
        # and through it we can get access to text tag from sender widget
        parent = self.sender()
        tag=parent.label.text()
        query = qts.QSqlQuery()
        query.prepare("""DELETE from tagmap
                      WHERE main_id=(select id from main_table where date_of_the_day=:date)
                      AND tag_id=(select id from tags where tag=:tag)""")
        query.bindValue(':date', self.date_for_update)
        query.bindValue(':tag', tag)
        query.exec()
        parent.deleteLater()
        self.all_tags_for_curr_day.remove(tag)
        query.prepare("""select tag_id from tagmap
                              WHERE tag_id=(select id from tags where tag=:tag)""")
        query.bindValue(':tag', tag)
        query.exec()
        query.next()
        if  not query.isValid():
            self.tag_list.remove(tag)
            query.prepare("""DELETE from tags
                                where tag=:tag""")
            query.bindValue(':tag', tag)
            query.exec()
        toaster.QToaster.showMessage(self, 'Tag has been successfully deleted!')

    def add_new_tag(self, tag=None, new_tag=False):
        # method that add new tag
        # if if there are no passed parameters, that method does nothng but add line add tag to show tag widget
        # if among parametres only tag, then show tags widget will be populate
        # with that tag if that tag not among existing tags for current day
        #
        if tag:
            if self.textedit.toPlainText():
                if tag not in self.all_tags_for_curr_day:
                    but = tag_frame.Tag_frame(tag)
                    but.buttonClicked.connect(self.delete_tag)
                    self.layout_for_tags.addWidget(but)
                    self.line_add_tag.setText('')
                    self.all_tags_for_curr_day.append(tag)
                    text = qts.QSqlQuery()
                    if tag not in self.tag_list:
                        self.tag_list.append(tag)
                        text.prepare('insert into tags (tag)'
                                     'values (:tag)')
                        text.bindValue(':tag', tag)
                        text.exec()
                    text.prepare('insert into tagmap (main_id,tag_id)'
                                 'values ((select id from main_table where date_of_the_day=:dat),'
                                 '(select id from tags where tag=:tag))')
                    text.bindValue(':dat', self.date_for_update)
                    text.bindValue(':tag', tag)
                    text.exec()
                else:
                    toaster.QToaster.showMessage(self, 'Tag already exist in that record!')
            else:
                toaster.QToaster.showMessage(self, 'Describe the day before tagging')
        self.layout_for_tags.addWidget(self.line_add_tag)

    def delete_record(self, date=None):
        # METHOD THAT DELETE DATE THAT RIGHT CLICKED IN CALENDAR
        if not date:
            date = self.calendar.selectedDate().toString(self.date_format)

        if date in self.list_date:
            text = qts.QSqlQuery()
            text.prepare("""DELETE FROM tagmap
                          WHERE main_id=(select id from main_table where date_of_the_day=:dat)""")
            text.bindValue(':dat', date)
            text.exec()
            text.prepare('DELETE FROM main_table WHERE date_of_the_day=:dat')
            text.bindValue(':dat', date)
            text.exec()
            for t in self.layout_for_tags._item_list[:-1]:
                cur_tag=t.widget().label.text()
                text.prepare("""select tag_id from tagmap
                                              WHERE tag_id=(select id from tags where tag=:tag)""")
                text.bindValue(':tag', cur_tag)
                text.exec()
                text.next()
                if not text.isValid():
                    text.prepare("""DELETE from tags
                                                    where tag=:tag""")
                    text.bindValue(':tag', cur_tag)
                    text.exec()
                self.tag_list.remove(cur_tag)
                t.widget().deleteLater()
                del self.layout_for_tags._item_list[0]
            self.layout_for_tags.addWidget(self.line_add_tag)
            self.list_date.remove(date)
            self.textedit.setText('')
            self.model.setStringList(self.list_date)

            toaster.QToaster.showMessage(self, 'Record has been successfully delete!!')
        else:
            toaster.QToaster.showMessage(self, 'Sorry, database doesn\'t have notes in this date')

    def changed_calendar_page(self,
                              first_day=None,
                              last_day=None):
        # method that invokes every time when page in calendar changed and
        # extract from sql db only records from first date to last date in the page
        query = qts.QSqlQuery()
        query.prepare('SELECT date_of_the_day FROM main_table where date_of_the_day between :date1 and :date2')
        query.bindValue(':date1', first_day)
        query.bindValue(':date2', last_day)
        query.exec()
        # removes old data from the list
        self.list_date = []
        # and populate with new data
        while query.next():
            self.list_date.append(query.value(0))
        # passing a new list to calendar class, that he can highlight dates in our new selected page
        self.calendar.list_dates = self.list_date
        # update completer in search line
        self.model.setStringList(self.list_date)
        # and set first date new page in search line
        try:
            self.search_line.setText(self.list_date[0])
        except:
            self.search_line.setText(f'{first_day}')

    def search(self):
        # method that calls when search line is activated,
        # but because we already have method for set notes in text widget from change calendar date
        # all that we need is simply change calendar date using date in searchline
        # and we receive succees or fail notification on the bottom left corner through QToaster
        date = qtc.QDate.fromString(self.search_line.text(), self.date_format)
        if self.search_line.text() in self.list_date:
            self.calendar.setSelectedDate(date)
            toaster.QToaster.showMessage(self, 'Records for this date\nwere found successfully')
        else:
            toaster.QToaster.showMessage(self, 'Sorry, there are no\nrecords for this date')

    def closeEvent(self, event):
        # method that calls when application closed for update or create notes in our sql file
        self.rewrite_or_insert_data()

    def set_text(self):
        # method that set text in text widget from sql file using selected date on calendar
        # set text in text widget
        text = qts.QSqlQuery()
        text.prepare("""SELECT about_the_day
                     from main_table
                     where date_of_the_day=:dat""")
        text.bindValue(':dat', self.date_for_update)
        text.exec()
        text.next()
        try:
            self.textedit.setText(text.value(0))
            self.set_color_text()
            self.check_change_text=self.textedit.toPlainText()
        except:
            self.textedit.setText('')

        # delete elements from flow layout list in order to
        # populate then this list new tags for new selected date
        for t in self.layout_for_tags._item_list[:-1]:
            t.widget().deleteLater()
            del self.layout_for_tags._item_list[0]

        # find al tags associated with selected date
        tag = qts.QSqlQuery()
        tag.prepare("""SELECT t.tag
                        from tags t 
                         INNER JOIN tagmap tm on t.id=tm.tag_id
                         INNER JOIN main_table m on m.id=tm.main_id
                         where m.date_of_the_day=:dat""")
        tag.bindValue(':dat', self.date_for_update)
        tag.exec()
        # and populate show tags list with these new tags
        while tag.next():
            self.add_new_tag(tag.value(0))
        # in case if there are no new tags, we simply add line tags edit,
        # because otherwise when we changed date and our old tags will be deleted
        # search line edit remain on its place and doesnt move in the beginning on the line
        # but adding lineedit anew, we update coordinates flow layout and line edit move in the beginning
        if len(self.layout_for_tags._item_list) == 1:
            self.layout_for_tags.addWidget(self.line_add_tag)

    def rewrite_or_insert_data(self):
        # this method invoke when change selected date on calendar in order
        # to update or create records on previous date that were in textedit and tags before change date
        # or to do the same things when closed application
        text = qts.QSqlQuery()
        if self.date_for_update in self.list_date:
            if not self.textedit.toPlainText():
                self.delete_record(date=self.date_for_update)
            else:
                text.prepare('UPDATE main_table SET about_the_day=:note WHERE date_of_the_day=:dat')
                text.bindValue(':dat', self.date_for_update)
                text.bindValue(':note', self.textedit.toHtml())
                text.exec()
        else:
            if self.textedit.toPlainText():
                text.prepare('insert into main_table (date_of_the_day,about_the_day)'
                             'values (:dat,:note)')
                text.bindValue(':note', self.textedit.toHtml())
                text.bindValue(':dat', self.date_for_update)
                text.exec()
                self.list_date.append(self.date_for_update)
                self.model.setStringList(self.list_date)

    def color_close(self):
        if self.styleSheet()== stylesheet_dark:
            for x in  self.layout_for_tags._item_list[:-1]:
                x.widget().x_button.setIcon(qtg.QIcon(':/teams/close-green.png'))
        else:
            for x in  self.layout_for_tags._item_list[:-1]:
                x.widget().x_button.setIcon(qtg.QIcon(':/teams/close.png'))

    def change_date(self):
        # this method calls when changed claendar date and invoke methods
        # that first of all save previous data in sql file
        # and set new text in textwidget and tags in tags widget from that new selected date
        if self.textedit.toPlainText()!=self.check_change_text:
            self.rewrite_or_insert_data()
        self.all_tags_for_curr_day = []
        self.line_add_tag.setText('')
        self.date_for_update = self.calendar.selectedDate().toString(self.date_format)
        self.set_text()
        self.stack.setCurrentWidget(self.right_side_widget)
        self.color_close()

    def set_color_text(self):
        # this method uses for set color text either whe application is start
        # or when change style, so that color and background color always opposite
        if self.styleSheet() == stylesheet_dark:
            cur_text = self.textedit.toHtml()
            cur_text = re.sub(r'color:#000000', 'color:#ffffff', cur_text)
            self.textedit.clear()
            self.textedit.setHtml(cur_text)
            self.textedit.setTextColor(qtg.QColor('#FFFFFF'))
        else:
            cur_text = self.textedit.toHtml()
            cur_text = re.sub(r'color:#ffffff', 'color:#000000', cur_text)
            self.textedit.clear()
            self.textedit.setHtml(cur_text)
            self.textedit.setTextColor(qtg.QColor('#000000'))

    def set_dark_style(self):
        self.setStyleSheet(stylesheet_dark)
        self.search_line.a.setIcon(qtg.QIcon(':/teams/lens_green.png'))
        self.search_tag_line.a.setIcon(qtg.QIcon(':/teams/lens_green.png'))
        self.L_button.setIcon(qtg.QIcon(':/teams/align-left-green.png'))
        self.C_button.setIcon(qtg.QIcon(':/teams/align-center-green.png'))
        self.R_button.setIcon(qtg.QIcon(':/teams/align-right-green.png'))
        self.W_button.setIcon(qtg.QIcon(':/teams/justify-green.png'))
        self.italics_button.setIcon(qtg.QIcon(':/teams/italics-green.png'))
        self.underline_button.setIcon(qtg.QIcon(':/teams/underline-green.png'))
        self.reset_button.setIcon(qtg.QIcon(':/teams/reset-green.png'))
        self.bold_button.setIcon(qtg.QIcon(':/teams/bold-green.png'))
        self.bullet_list_button.setIcon(qtg.QIcon(':/teams/bullet-list-green.png'))
        self.number_list_button.setIcon(qtg.QIcon(':/teams/numbered-list-green.png'))
        self.toggle.circle_color = '#F8EDED'
        self.toggle.bg_color = '#6dc263'
        self.date_completer.popup().setStyleSheet("QListView{color:#6dc263;background-color: #212121;"
                                                  "selection-background-color:#6dc263;"
                                                  "selection-color:#000000;"
                                                  "border: 1px solid #6dc263;}"
                                                  )
        self.tags_completer.popup().setStyleSheet("QListView{color:#6dc263;background-color: #212121;"
                                                  "selection-background-color:#6dc263;"
                                                  "selection-color:#000000;"
                                                  "border: 1px solid #6dc263;}"
                                                  )

        self.set_color_text()

        self.calendar.normal_select = '#6dc263'
        self.calendar.num_color = '#ffffff'
        self.calendar.file_color = '#44783d'
        self.calendar.current_select = '#1dda2d'
        self.calendar.change_color_text()
        self.color_close()

    def set_light_style(self):
        self.setStyleSheet(stylesheet_light)
        self.search_line.a.setIcon(qtg.QIcon(':/teams/lens.png'))
        self.search_tag_line.a.setIcon(qtg.QIcon(':/teams/lens.png'))
        self.L_button.setIcon(qtg.QIcon(':/teams/align-left.png'))
        self.C_button.setIcon(qtg.QIcon(':/teams/align-center.png'))
        self.R_button.setIcon(qtg.QIcon(':/teams/align-right.png'))
        self.W_button.setIcon(qtg.QIcon(':/teams/justify.png'))
        self.italics_button.setIcon(qtg.QIcon(':/teams/italics.png'))
        self.underline_button.setIcon(qtg.QIcon(':/teams/underline.png'))
        self.reset_button.setIcon(qtg.QIcon(':/teams/reset.png'))
        self.bold_button.setIcon(qtg.QIcon(':/teams/bold.png'))
        self.bullet_list_button.setIcon(qtg.QIcon(':/teams/bullet-list.png'))
        self.number_list_button.setIcon(qtg.QIcon(':/teams/numbered-list.png'))
        self.toggle.circle_color = '#CAF7E3'
        self.toggle.bg_color = '#E4BAD4'
        self.date_completer.popup().setStyleSheet("QListView{color:#000000;background-color: #F8EDED;"
                                                  "selection-background-color:#e4a2c2;"
                                                  "selection-color:#000000;"
                                                  "border: 1px solid #e4a2c2;}"
                                                  )
        self.tags_completer.popup().setStyleSheet("QListView{color:#000000;background-color: #F8EDED;"
                                                  "selection-background-color:#e4a2c2;"
                                                  "selection-color:#000000;"
                                                  "border: 1px solid #e4a2c2;}"
                                                  )

        self.set_color_text()

        self.calendar.normal_select = '#E4BAD4'
        self.calendar.num_color = '#000000'
        self.calendar.file_color = '#CAF7E3'
        self.calendar.current_select = '#e4a2c2'
        self.calendar.change_color_text()
        self.color_close()

    def change_style(self):
        # methof for change styles
        if self.styleSheet() == stylesheet_light:
            self.set_dark_style()

        else:
            self.set_light_style()

    def reset_font(self):
        self.textedit.setFontWeight(50)
        self.textedit.setFontItalic(0)
        self.textedit.setFontUnderline(0)
        self.change_size()

    def change_font(self):
        self.textedit.setCurrentFont(qtg.QFont(self.fonts.currentFont()))

    def change_size(self):
        self.textedit.setFontPointSize(self.size.value())

    def bold(self):
        if self.textedit.fontWeight() == 50:
            self.textedit.setFontWeight(qtg.QFont.Bold)
        else:
            self.textedit.setFontWeight(50)

    def italics(self):
        if self.textedit.fontItalic():
            self.textedit.setFontItalic(0)
        else:
            self.textedit.setFontItalic(1)

    def underline(self):
        if self.textedit.fontUnderline():
            self.textedit.setFontUnderline(0)
        else:
            self.textedit.setFontUnderline(1)

    def leftAlign(self):
        self.textedit.setAlignment(qtc.Qt.AlignLeft)

    def rightAlign(self):
        self.textedit.setAlignment(qtc.Qt.AlignRight)

    def centerAlign(self):
        self.textedit.setAlignment(qtc.Qt.AlignCenter)

    def vcenterAlign(self):
        self.textedit.setAlignment(qtc.Qt.AlignVCenter)

    def slide_method(self, parent,
                     width=None,
                     height=None,
                     newsize=None, property=None,
                     curve=qtc.QEasingCurve.OutBack):

        # method for slide widgets
        if width:
            old = parent.width()
        else:
            old = parent.height()

        if old == 0:
            new = newsize
        else:
            new = 0
        self.animation = qtc.QPropertyAnimation(parent, property)
        self.animation.setDuration(300)
        self.animation.setStartValue(old)
        self.animation.setEndValue(new)
        self.animation.setEasingCurve(curve)
        self.animation.start()

    # color widget
    def coloropen(self):
        self.colorwidget()

    def colorwidget(self):
        cur = self.color.getColor()
        if cur.isValid():
            self.go_pixmap.fill(qtg.QColor(cur.name()))
            self.connect_icon.addPixmap(self.go_pixmap)
            self.Color_button.setIcon(self.connect_icon)
            self.textedit.setTextColor(qtg.QColor(cur.name()))

    def bulletlist(self):
        if self.textedit.textCursor().selectedText():
            text=self.textedit.textCursor().selectedText()
        else:
            text ='  '
        self.textedit.insertHtml(f"<ul style='font-size:14px;'><li>{text}</li></ul>")

    def numberlist(self):
        if self.textedit.textCursor().selectedText():
            text=self.textedit.textCursor().selectedText()
        else:
            text ='  '
        self.textedit.insertHtml(f"<ol><li style='font-size:14px;';>{text}</li></ol>")

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    #d=PasswordForm()
    sys.exit(app.exec())