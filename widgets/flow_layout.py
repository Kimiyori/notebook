

from PyQt5 import QtWidgets as qtw

from PyQt5 import QtCore as qtc



class FlowLayout(qtw.QLayout):
    """Layout for tags, which contain tag widgets
    and can dynamically resize their positions
    depending on length text in tags or total amount fo tags"""

    # example flow layout took from here
    # https://doc.qt.io/qtforpython/examples/example_widgets_layouts_flowlayout.html
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setContentsMargins(qtc.QMargins(0, 0, 0, 0))

        # list that contain list of Widget items
        self._item_list = []

    def __del__(self):
        # Delete all the items in this layout
        item = self.take_at(0)
        while item:
            item = self.take_at(0)

    def addItem(self, item):
        # Add an item at the end of the layout.
        # This is automatically called when you do addWidget()
        self._item_list.append(item)

    def count(self):
        # Get the number of items in the this layout
        return len(self._item_list)

    def itemAt(self, index):
        # Get the item at the given index
        if index >= 0 and index < len(self._item_list):
            return self._item_list[index]

        return None

    def takeAt(self, index):
        # Remove an item at the given index
        if index >= 0 and index < len(self._item_list):
            return self._item_list.pop(index)

        return None

    def expandingDirections(self):
        # This layout grows only in the horizontal dimension
        return qtc.Qt.Orientations(qtc.Qt.Orientation(0))

    def hasHeightForWidth(self):
        # If this layout's preferred height depends on its width
        return True

    def heightForWidth(self, width):
        # Get the preferred height a layout item with the given width
        height = self._do_layout(qtc.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        # Set the geometry of this layout
        super(FlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        # Get the preferred size of this layout
        return self.minimumSize()

    def minimumSize(self):
        # Get the minimum size of this layout
        size = qtc.QSize()
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())

        size += qtc.QSize(2 * self.contentsMargins().top(),
                          2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        # Layout all the items
        # @param rect (QRect) Rect where in the items have to be laid out
        # @param testOnly (boolean) Do the actual layout
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing()
        for item in self._item_list:
            style = item.widget().style()
            layout_spacing_x = style.layoutSpacing(qtw.QSizePolicy.PushButton,
                                                   qtw.QSizePolicy.PushButton,
                                                   qtc.Qt.Horizontal)

            layout_spacing_y = style.layoutSpacing(qtw.QSizePolicy.PushButton,
                                                   qtw.QSizePolicy.PushButton,
                                                   qtc.Qt.Vertical)
            space_x = spacing + layout_spacing_x
            space_y = spacing + layout_spacing_y
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(qtc.QRect(qtc.QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()
