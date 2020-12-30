from PySide2.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PySide2.QtGui import QColor, QPainter, QTextFormat, QFont, QTextCharFormat, QBrush, QTextCursor
from PySide2.QtCore import Qt, QRect, QSize

class TINY_Editor(QPlainTextEdit):

    class _NumberArea(QWidget):
        def __init__(self, editor):
            super().__init__(editor)
            self.codeEditor = editor

        def sizeHint(self):
            return QSize(self.editor.lineNumberAreaWidth(), 0)

        def paintEvent(self, event):
            self.codeEditor.lineNumberAreaPaintEvent(event)

    def __init__(self, parent=None):

        super(TINY_Editor, self).__init__(parent)
        self.setFont(QFont("Courier New", 11))
        self.lineNumberArea = TINY_Editor._NumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.findHighlightFormat = QTextCharFormat()
        self.findHighlightFormat.setBackground(QBrush(QColor("red")))
        self.searchTxtBx = None

    def lineNumberAreaWidth(self):
        digits = 5
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(229, 248, 255, 255)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), QColor(233, 233, 233, 255))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                fFont = QFont("Courier New", 10)
                painter.setPen(QColor(130, 130, 130, 255))
                painter.setFont(fFont)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def clear_format(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        cursor.clearSelection()
        self.setTextCursor(cursor)

