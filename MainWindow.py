from PySide2.QtWidgets import QWidget,QGridLayout,QVBoxLayout,QGroupBox,QPushButton,QFileDialog,QMessageBox
from PySide2.QtGui import QIcon,QPalette,QColor,QFont
from PySide2.QtCore import Qt, QSize
from PySide2 import QtGui
from TINY_editor import TINY_Editor
from Scanner_Output import Scanner_Output
from Lexer import Lexer
from in_out import *
import  os
from Parser_class import *

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        # set title  and geometry for the window
        self.setWindowTitle("TINY Scanner")
        self.setGeometry(800,600,400,200)

        # give orange background to the window
        # palette = self.palette()
        # palette.setColor(QPalette.Window, QColor(0, 0, 0))
        # self.setPalette(palette)
        # self.setAutoFillBackground(True)

        # set minimum width and height for the window
        self.setMinimumHeight(600)
        self.setMinimumWidth(800)
        self.setMaximumHeight(1000)
        self.setMaximumWidth(1200)

        self.center()

        # setup the grid layout design and components
        self.create_grid()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.gpIn)
        self.vbox.addWidget(self.gpOut)
        self.vbox.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.setLayout(self.vbox)

        self._start_communications()

    def _start_communications(self):
        self.runButton.clicked.connect(self._scan)
        self.parseButton.clicked.connect(self._parse)
        self.openButton.clicked.connect(self._scan_from_file)
        self.saveButton.clicked.connect(self._save_tokens)

    def _save_tokens(self):
        path, _ = QFileDialog.getSaveFileName(self,"Save file","/")
        if path == "":
            QMessageBox.warning(self, "No Selected File", "Please select a valid file")
            return

        with open(path, 'w') as file:
            file.write(self.scanner_out.toPlainText())

    def _scan_from_file(self):
        path, _ = QFileDialog.getOpenFileName(self,"Open file","/","*.txt (*.txt)")
        if path == "":
            QMessageBox.warning(self,"No Selected File","Please select a valid file")
            return

        with open(path, 'r') as file:
            text = file.read()
            self.editor.setPlainText(text)

    def _scan(self):
        self.scanner_out.setPlainText("")
        text = self.editor.toPlainText()
        tokens = self.getTokens(text)
        self.scanner_out.setPlainText(tokens)

    def _parse(self):
        text = self.editor.toPlainText()
        parse_text = read_from_editor(text)
        p = Parser(parse_text)
        p.run()
        os.system("SyntaxTree.png")

    def getTokens(self,text):
        scanner = Lexer(text)
        tokens = ""
        while True:
            token = scanner.next_token()
            if token.type == 'EOF':
                return tokens
            tokens += token.value + " , " + token.type + "\n"

    def create_grid(self):
        # make group box with headline then add the gridlayout to it
        self.gpIn = QGroupBox("TINY Language")
        self.gpIn.setFont(QFont("Helvetica", 12))
        self.gpOut = QGroupBox("Scanner Output")
        self.gpOut.setFont(QFont("Helvetica", 12))

        # create gridlayout with spacing between columns and rows
        glIn = QGridLayout()
        glIn.setSpacing(10)
        glOut = QGridLayout()
        glOut.setSpacing(10)

        self.editor = TINY_Editor(self)

        self.scanner_out = Scanner_Output(self)
        palette = self.palette()
        palette.setColor(QPalette.Active,QPalette.Base,QColor(150,150,150))
        self.scanner_out.setPalette(palette)
        self.scanner_out.setAutoFillBackground(True)

        self.runButton = QPushButton("Scan")
        self.runButton.setIcon(QIcon("icons/scan.png"))
        self.runButton.setIconSize(QSize(35, 35))
        self.runButton.setMinimumWidth(100)
        self.runButton.setMinimumHeight(50)

        self.parseButton = QPushButton("Parse")
        self.parseButton.setIcon(QIcon("icons/parse.png"))
        self.parseButton.setIconSize(QSize(35, 35))
        self.parseButton.setMinimumWidth(100)
        self.parseButton.setMinimumHeight(50)

        self.openButton = QPushButton("Open File")
        self.openButton.setIcon(QIcon("icons/upload.png"))
        self.openButton.setIconSize(QSize(35, 35))
        self.openButton.setMinimumWidth(150)
        self.openButton.setMinimumHeight(50)

        self.saveButton = QPushButton("Save Tokens")
        self.saveButton.setIcon(QIcon("icons/save.png"))
        self.saveButton.setIconSize(QSize(35, 35))
        self.saveButton.setMinimumWidth(200)
        self.saveButton.setMinimumHeight(50)

        glIn.addWidget(self.editor, 0, 0, 1, 4)
        glIn.addWidget(self.runButton, 1, 0)
        glIn.addWidget(self.parseButton, 1, 1)
        glIn.addWidget(self.openButton, 1, 2)
        glIn.addWidget(self.saveButton, 1, 3)
        glOut.addWidget(self.scanner_out, 0, 0)

        self.gpIn.setLayout(glIn)
        self.gpOut.setLayout(glOut)

    # to center the application window at the beginning
    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())
