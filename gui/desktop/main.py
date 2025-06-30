import sys
from PySide6.QtWidgets import QApplication
from .main_window import ColonelKDEApp

def main():
    app = QApplication(sys.argv)
    window = ColonelKDEApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()