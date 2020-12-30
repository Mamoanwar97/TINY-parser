from PySide2.QtWidgets import QApplication
from MainWindow import MainWindow

# import sys to run the application
import sys

# run the application and show the window
app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()
sys.exit(0)