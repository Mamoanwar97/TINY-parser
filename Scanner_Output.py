from PySide2.QtWidgets import QPlainTextEdit

class Scanner_Output(QPlainTextEdit):

    def __init__(self, parent=None):
        super(Scanner_Output, self).__init__(parent)

        self.setReadOnly(True)