import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from main_window import ColonelKDEApp

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("/home/ucadmin/Development/Colonel-Katie/The_Colonel.png"))
    window = ColonelKDEApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()