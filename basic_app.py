from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from display_components import DisplayComponents
import sys

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
        self.title_spacing = self.findChild(QtWidgets.QFrame, 'title_spacing')
        self.close_btn = self.findChild(QtWidgets.QPushButton, 'close_btn')
        self.preview_btn = self.findChild(QtWidgets.QPushButton, 'preview_btn')
        self.setting_btn = self.findChild(QtWidgets.QPushButton, 'setting_btn')
        self.stacked_display_widget = self.findChild(QtWidgets.QStackedWidget, 'stacked_display_widget')
        self.setting_page = self.findChild(QtWidgets.QWidget, 'setting_page')
        self.preview_page = self.findChild(QtWidgets.QWidget, 'preview_page')
        self.cam1_cbx = self.findChild(QtWidgets.QComboBox, 'cam1_cbx')
        self.cam2_cbx = self.findChild(QtWidgets.QComboBox, 'cam2_cbx')
        self.dual_cb = self.findChild(QtWidgets.QCheckBox, 'dual_cb')

        # Get screen resolution
        self._screen_width, self._screen_height = DisplayComponents.get_resolution()

        # Default setting
        self.default_setting()

    def full_screen_event_handler(self):
        """Set application to full screen resolution"""
        if self.isMaximized() == False:
            # Set width and height
            self.title_spacing.setMaximumWidth(int(self._screen_width / 2))
            self.title_spacing.setMinimumWidth(int(self._screen_width / 2))
            # Show
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

    def minimum_event_handler(self):
        """Set application to minimun resolution"""
        if self.isMaximized() == True:
            # Set width and height
            self.title_spacing.setMaximumWidth(int(self._screen_width / 4))
            self.title_spacing.setMinimumWidth(int(self._screen_width / 4))
            # Show
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

    def hide_event_handler(self):
        """Set application to backgroud mode"""
        self.showMinimized()

    def setting_mode_handler(self):
        self.stacked_display_widget.setCurrentWidget(self.setting_page)

    def preview_mode_handler(self):
        self.stacked_display_widget.setCurrentWidget(self.preview_page)

    def close_event_handler(self):
        """Close the application"""
        answer = QtWidgets.QMessageBox.question(
            self,
            'Confirmation',
            'Do you want to quit?',
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No
        )
        # When user click Yes
        if answer == QtWidgets.QMessageBox.StandardButton.Yes:
            self.close()

    def default_setting(self):
        # Set default Windows resolution
        self.setWindowTitle("Camera Application")
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(int(self._screen_width / 2), int(self._screen_height * 3 / 4))
        # Default mode
        self.stacked_display_widget.setCurrentWidget(self.setting_page)

        # Set spacing
        self.title_spacing.setMaximumWidth(int(self._screen_width / 4))
        self.title_spacing.setMinimumWidth(int(self._screen_width / 4))

        # Button setting
        large_icon_size = QtCore.QSize(40, 40)
        medium_icon_size = QtCore.QSize(30, 30)

        self.cam1_cbx.setStyleSheet("""
            QComboBox{
                border: 2px solid #ced4da;
                border-radius: 4px;
            }
            QComboBox:drop-down{
                border: 0px;
            }
            QComboBox::down-arrow {
                image: url(icons/arrow_down.png);
                width: 20px;
                height: 20px;
            }
            QComboBox::on {
                border: 4px;
            }
        """)

        self.cam2_cbx.setStyleSheet("""
            QComboBox{
                border: 2px solid #ced4da;
                border-radius: 4px;
            }
            QComboBox:drop-down{
                border: 0px;
            }
            QComboBox::down-arrow {
                image: url(icons/arrow_down.png);
                width: 20px;
                height: 20px;
            }
        """)

        self.dual_cb.setStyleSheet("""
            QCheckBox{
                color: rgb(255, 255, 255);            
            }
            QCheckBox::indicator{
                width: 30px;
                height: 30px;
            }
            QCheckBox::indicator:checked{
                image: url(icons/toogle_on.png);            
            }
            QCheckBox::indicator:unchecked{
                image: url(icons/toggle_off.png);            
            }
        """)

        # Exit Button
        self.exit_btn.clicked.connect(self.close_event_handler)
        self.exit_btn.setToolTip("Exit")
        self.exit_btn.setIcon(QtGui.QIcon('icons/exit.png'))
        self.exit_btn.setIconSize(large_icon_size)
        # Close Button
        self.close_btn.setIcon(QtGui.QIcon('icons/exit_2.png'))
        self.close_btn.setIconSize(QtCore.QSize(30,30))
        self.close_btn.clicked.connect(self.close_event_handler)

        # Maximize Windows Button
        self.max_btn.clicked.connect(self.full_screen_event_handler)
        self.max_btn.setToolTip("Maximize")
        self.max_btn.setIcon(QtGui.QIcon('icons/maximize.png'))
        self.max_btn.setIconSize(large_icon_size)

        # Minimize Windows Button
        self.min_btn.clicked.connect(self.minimum_event_handler)
        self.min_btn.setToolTip("Minimize")
        self.min_btn.setIcon(QtGui.QIcon('icons/minimize.png'))
        self.min_btn.setIconSize(large_icon_size)

        # Minimize Windows Button
        self.hide_btn.clicked.connect(self.hide_event_handler)
        self.hide_btn.setToolTip("Hide")
        self.hide_btn.setIcon(QtGui.QIcon('icons/hide.png'))
        self.hide_btn.setIconSize(large_icon_size)

        # Feature setup
        self.setting_btn.setIcon(QtGui.QIcon('icons/setting.png'))
        self.setting_btn.setIconSize(medium_icon_size)
        self.setting_btn.clicked.connect(self.setting_mode_handler)
        self.preview_btn.setIcon(QtGui.QIcon('icons/camera.png'))
        self.preview_btn.setIconSize(medium_icon_size)
        self.preview_btn.clicked.connect(self.preview_mode_handler)


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
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
