from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from display_components import DisplayComponents

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load UI
        loadUi("ui/main_windows.ui",self)

        # Get children
        self.exit_btn = self.findChild(QtWidgets.QPushButton, 'exit_btn')
        self.max_btn = self.findChild(QtWidgets.QPushButton, 'max_btn')
        self.min_btn = self.findChild(QtWidgets.QPushButton, 'min_btn')
        self.hide_btn = self.findChild(QtWidgets.QPushButton, 'hide_btn')


        # Default setting
        self.default_setting()

    def full_screen_event(self):
        """Set application to full screen resolution"""
        if self.isMaximized() == False:
            self.showMaximized()
            return
        # Validate
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        # setting message for Message Box
        msg.setText("You're currently in Full-screen mode!")
        # setting Message box window title
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # start the app
        msg.exec_()

    def minimum_event(self):
        """Set application to minimun resolution"""
        if self.isMaximized() == True:
            self.showNormal()
            return
        # Validate
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        # setting message for Message Box
        msg.setText("You're currently in Normal mode!")
        # setting Message box window title
        msg.setWindowTitle("Warning")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # start the app
        msg.exec_()

    def hide_event(self):
        """Set application to backgroud mode"""
        self.showMinimized()
    def close_event(self):
        """Close the application"""
        self.close()

    def default_setting(self):
        # Get screen resolution
        screen_width, screen_height = DisplayComponents.get_resolution()
        # Set default Windows resolution
        self.setWindowTitle("Camera Application")
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(int(screen_width / 2), int(screen_height * 3 / 4))

        # Button setting
        button_size = QtCore.QSize(40, 40)
        # Exit Button
        self.exit_btn.clicked.connect(self.close_event)
        self.exit_btn.setToolTip("Exit")
        self.exit_btn.setIcon(QtGui.QIcon('icons/exit.png'))
        self.exit_btn.setIconSize(button_size)

        # Maximize Windows Button
        self.max_btn.clicked.connect(self.full_screen_event)
        self.max_btn.setToolTip("Maximize")
        self.max_btn.setIcon(QtGui.QIcon('icons/maximize.png'))
        self.max_btn.setIconSize(button_size)

        # Minimize Windows Button
        self.min_btn.clicked.connect(self.minimum_event)
        self.min_btn.setToolTip("Minimize")
        self.min_btn.setIcon(QtGui.QIcon('icons/minimize.png'))
        self.min_btn.setIconSize(button_size)

        # Minimize Windows Button
        self.hide_btn.clicked.connect(self.hide_event)
        self.hide_btn.setToolTip("Hide")
        self.hide_btn.setIcon(QtGui.QIcon('icons/hide.png'))
        self.hide_btn.setIconSize(button_size)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
