

stylesheet_dark = """
    QWidget#widcol{
        background-color: #181818;
    }
    QLabel#count_words{
        color: #ffffff;
    }
    QLabel#notification_text{
        color: #6dc263;
    }
    QTextEdit{
        background-color: #212121;   
        border: 0px;
        background-image: url(pngegg.png);
        background-repeat:  no-repeat;
        background-position:  bottom right;
        color:#ffffff;
    }
    QPushButton#main_buttons{
        background-color: #181818;
        padding-top: 5px;
        border-radius: 8px;
        color: #FFFFFF;
        width: 3em;
        font-size: 16pt;
    }
    QPushButton#main_buttons::hover{
        border-color: #6dc263;
        color: #6dc263;
        border-width: 1px;
        border-style:solid;
    }
    QPushButton#settings_buttons{
        background-color: #181818;
        padding-top: 3px;
        padding-bottom: 3px;
        border-radius: 2px;
        color: #FFFFFF;
        }
    QPushButton#settings_buttons::hover{
        border-color: #6dc263;
        color: #6dc263;
        border-width: 1px;
        border-style:solid;
    }
    QPushButton{
        color: #FFFFFF;
    }
    QPushButton::hover{
        border-color: #6dc263;
        color: #6dc263;
        border-width: 1px;
        border-style:solid;
    }
    QSpinBox {
        color: #6dc263;
        background-color:  #212121;
        border-width: 0px;
        border-color: #212121;
        border-style: solid;

    }
    QFontComboBox{
        color: #6dc263;
        background-color:  #212121;
    }

    QSpinBox::up-arrow {
        color: #FFFFFF;
        image: url(:/teams/spin_up-green.png);

    }
    QSpinBox::down-arrow {
        color: #FFFFFF;
        image: url(:/teams/spin_down-green.png);

    }
    QSpinBox:hover {
        border-width: 1px;
        border-color: #6dc263;
        border-style: solid;
    }
    QListView{
        color: #FFFFFF;
        background-color:  #212121;
        border-width: 0px;
    }
    QStatusBar{
    background-color: #181818;
    color: #FFFFFF;
    }
    QCalendarWidget QAbstractItemView { 
        selection-background-color: #181818; 
        selection-color: #181818;
    }
    QCalendarWidget QWidget {
        color:#FFFFFF;
        alternate-background-color:#6dc263;
        background-color : #212121;
    }
    QCalendarWidget QTableView{
        background-color:#181818;
    }
    QCalendarWidget QToolButton {
        color: white;
        background-color: #212121;
    }
    QCalendarWidget QToolButton#qt_calendar_prevmonth{
        width: 35px;
        qproperty-icon: url(:/teams/calendar_left_green.png);
    }
    QCalendarWidget  QToolButton#qt_calendar_nextmonth{
        width: 35px;
        qproperty-icon: url(:/teams/calendar_right_green.png);
    }
    QCalendarWidget QToolButton#qt_calendar_prevmonth::hover,QCalendarWidget QToolButton#qt_calendar_nextmonth::hover,
    QCalendarWidget QToolButton#qt_calendar_monthbutton::hover,QCalendarWidget QToolButton#qt_calendar_yearbutton::hover{
        border-color: #6dc263;
        color: #6dc263;
        border-width: 1px;
        border-style:solid;
    }
    QToaster {
        border: 1px solid #6dc263;
        border-radius: 4px; 
        background-color: #212121;
        
    }
    QLineEdit {
    background-color:#212121;
    color:#ffffff;
    border: none;
    border-radius:8px;
    }
    QLineEdit::hover {
    border: 1px solid #6dc263;
    }
    QFrame#fram{
    background-color:#212121;
    border-radius: 8px;
    color: #6dc263;
    }
    QFrame::hover#fram {
    border: 1px solid #6dc263;
    }
    QLabel{
    color:#ffffff;
    }

    QPushButton#bb
    {background-color:#212121;
    color:#ffffff;
    border: 0px solid;
    border-radius:px;
    }
        QTableWidget {
    background-color: #212121;
    border: 1px solid #ffffff;
    color: #ffffff;
     selection-background-color:#6dc263;
    }
    QHeaderView::section {
    background-color: #181818;
    padding: 4px;
    border: 1px solid #ffffff;;
    color: #ffffff;
}
QTableWidget QTableCornerButton::section {
background-color: #181818;
}
QHeaderView
{
   background-color: #181818;
    padding: 4px;
    border: 1px solid #ffffff;
}
QAction::hover #right_click{
    background-color: #6dc263;
}

"""

stylesheet_light = """
    QWidget#widcol{
        background-color:#F6DFEB;
    }
    QLabel#count_words{
        color: #000000;
    }

    QLabel#notification_text{
        color: #000000;
    }
    QTextEdit{
        background-color: #F8EDED;   
        border: 0px;
        background-image: url(pink.png);
        background-repeat:  no-repeat;
        background-position:  bottom right;
        color:#000000;
    }
    QPushButton#main_buttons{
        background-color: #F6DFEB;
        padding-top: 5px;
        border-radius: 8px;
        color: #FFFFFF;
        width: 3em;
        font-size: 16pt;
    }
    QPushButton#main_buttons::hover{
        border-color: #E4BAD4;
        color: #E4BAD4;
        border-width: 1px;
        border-style:solid;
    }
    QPushButton#settings_buttons{
        background-color: #F6DFEB;
        padding-top: 3px;
        padding-bottom: 3px;
        border-radius: 2px;
        color: #FFFFFF;
        }
    QPushButton#settings_buttons::hover{
        border-color: #E4BAD4;
        color: #E4BAD4;
        border-width: 1px;
        border-style:solid;
    }
    QPushButton{
        color: #FFFFFF;
    }
    QPushButton::hover{
        border-color: #E4BAD4;
        color: #E4BAD4;
        border-width: 1px;
        border-style:solid;
    }
    QSpinBox {
        color: #000000;
        background-color:  #F6DFEB;
        border: 1px solid #E4BAD4;
    }
    QFontComboBox{
        color: #000000;
        background-color:  #F6DFEB;
        border: 1px solid #E4BAD4;
    }
     QListView{
        color: #000000;
        background-color:  #F6DFEB;
        border-width: 0px;
    }
    QSpinBox::up-arrow {
        image: url(:/teams/spin_up.png);
    }
    QSpinBox::down-arrow {
        image: url(:/teams/spin_down.png);   
    }
    QSpinBox:hover {
        border-width: 1px;
        border-color: #E4BAD4;
        border-style: solid;
    }
    QStatusBar{
        background-color: #F6DFEB;
    }
    QCalendarWidget QAbstractItemView { 
        selection-background-color: #F6DFEB; 
        selection-color: #F6DFEB;
    }
    QCalendarWidget QWidget {
        color:#000000;
        alternate-background-color:white;
        background-color : #E4BAD4;
    }
    QCalendarWidget QTableView{
        background-color:#F6DFEB;
    }
    QCalendarWidget QToolButton {
        color: white;
        background-color: #E4BAD4;
    }

    QCalendarWidget QToolButton#qt_calendar_prevmonth{
        width: 35px;
        qproperty-icon: url(:/teams/calendar_left.png);
    }
    QCalendarWidget  QToolButton#qt_calendar_nextmonth{
        width: 35px;
        qproperty-icon: url(:/teams/calendar_right.png);
    }
    QCalendarWidget QToolButton#qt_calendar_prevmonth::hover,QCalendarWidget QToolButton#qt_calendar_nextmonth::hover,
    QCalendarWidget QToolButton#qt_calendar_monthbutton::hover,QCalendarWidget QToolButton#qt_calendar_yearbutton::hover{
        border-color: #CAF7E3;
        color: #CAF7E3;
        border-width: 1px;
        border-style:solid;
    }
    QToaster {
        border: 1px solid #F8EDED;
        border-radius: 4px; 
        background-color: #e4a2c2;
        color:#6dc263;
    }
    QLineEdit {
    background-color: #F8EDED;
    color:#000000;
    border: none;
    border-radius:8px;
    }
    QLineEdit::hover {
    border: 1px solid  #E4BAD4;
    }
    QFrame#fram{
    background-color:#E4BAD4;
    border-radius: 8px;
    color: #ffffff;
    }
    QFrame::hover#fram {
    border-color:#F6DFEB;
    }
    QLabel{
    color:#ffffff;
    }
    QLabel#count_words{
    color:gray;
    }
    QPushButton#bb
    {background-color:#E4BAD4;
    color:#ffffff;
    border: 0px solid;
    border-radius:px;
    }
    QTableWidget {
    background-color: #F8EDED;
    border: 1px solid #ffffff;
    }
    QHeaderView::section {
    background-color: #F6DFEB;
    padding: 4px;
    border: 0px solid #F6DFEB;
}
QTableWidget QTableCornerButton::section {
background-color: #F6DFEB;
}
QHeaderView
{
   background-color: #F6DFEB;
    padding: 4px;
    border: 1px solid #ffffff;
}
"""