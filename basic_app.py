import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from display_components import DisplayComponents
from camera_components import CameraComponents
from config_component import ConfigManagement
import cv2

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
        self.cam1_cbx = self.findChild(QtWidgets.QComboBox, 'c1_cbx')
        self.cam2_cbx = self.findChild(QtWidgets.QComboBox, 'c2_cbx')
        self.dual_cb = self.findChild(QtWidgets.QCheckBox, 'dual_cb')
        self.cam1_frame = self.findChild(QtWidgets.QFrame, 'cam1_frame')
        self.cam1_display = self.findChild(QtWidgets.QLabel, 'cam1_display')

        # Get screen resolution
        self._screen_width, self._screen_height = DisplayComponents.get_resolution()

        # Default setting
        self.default_setting()

    def initCamera(self, camera_index: int ):
        self.cap = cv2.VideoCapture(camera_index)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)  # Update frame every 20ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QtGui.QImage(frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
            pix_map = QtGui.QPixmap.fromImage(q_img)
            self.cam1_display.setPixmap(pix_map)



    def full_screen_event_handler(self) -> None:
        """Set application to full screen resolution"""
        if self.isMaximized() == False:
            # Set width and height
            self.title_spacing.setMaximumWidth(int(self._screen_width / 2))
            self.title_spacing.setMinimumWidth(int(self._screen_width / 2))
            # Show
            self.showMaximized()
            return

        # Validate
        self.show_message_box_alert(title="Warning",
                                    content="You're currently in Full-screen mode!")

    def minimum_event_handler(self) -> None:
        """Set application to minimun resolution"""
        if self.isMaximized() == True:
            # Set width and height
            self.title_spacing.setMaximumWidth(int(self._screen_width / 4))
            self.title_spacing.setMinimumWidth(int(self._screen_width / 4))
            # Show
            self.showNormal()
            return

        # Validate
        self.show_message_box_alert(title = "Warning",
                                    content = "You're currently in Normal mode!")

    def hide_event_handler(self) -> None:
        """Set application to backgroud mode"""
        self.showMinimized()

    def setting_mode_handler(self) -> None:
        # Change main widget
        self.stacked_display_widget.setCurrentWidget(self.setting_page)
        # Change color of preview button
        self.setting_btn.setStyleSheet("""
            QPushButton{
                background-color: rgb(218, 145, 0);
                padding-left:100px;
                text-align: left
            }
        """)
        self.preview_btn.setStyleSheet("""
            QPushButton{
                padding-left:100px;
                text-align: left;
                background-color: rgb(255, 255, 255);
            }
        """)

        # Release Cv2 Cap
        try:
            if self.cap.isOpened(): self.cap.release()
        except:
            pass


    def preview_mode_handler(self) -> None:
        # Change main widget
        self.stacked_display_widget.setCurrentWidget(self.preview_page)
        # Change color of setting button
        self.setting_btn.setStyleSheet("""
            QPushButton{
                background-color: rgb(255, 255, 255);
                padding-left:100px;
                text-align: left
            }
        """)
        self.preview_btn.setStyleSheet("""
            QPushButton{
                padding-left:100px;
                text-align: left;
                background-color: rgb(218, 145, 0);
            }
        """)

        # Open Camera
        camera1_config = ConfigManagement.get_sections_config("Camera1")
        index = camera1_config["Camera1"]["index"]
        if index != "":
            self.initCamera(int(index))


    def close_event_handler(self) -> None:
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

    def selected_camera_event_handler(self,index):
        # When user selected None
        if index == 0:
            # Set config
            ConfigManagement.set_config(section = "Camera1",
                                        option = "device_name",
                                        value = "")
            ConfigManagement.set_config(section = "Camera1",
                                        option = "index",
                                        value = "")
            # Alert
            self.show_message_box_alert(title="Alert",
                                        content=f"No device has been selected!")
            return

        # Get selected camera infor
        index -= 1 # First index is just for displayed
        selected_camera = self.__list_camera[index]
        # Validate camera
        camera_index = selected_camera[0]
        isAvailalbe = CameraComponents.is_available_camera(camera_index)

        # When camera is unavailable
        if not isAvailalbe:
            ConfigManagement.set_config(section="Camera1",
                                        option="device_name",
                                        value="")
            ConfigManagement.set_config(section="Camera1",
                                        option="index",
                                        value="")
            self.show_message_box_alert(title = "Alert",
                                        content = f"Cannot connect 0 to device: {selected_camera[1]}")
            return

        # Show state
        self.show_message_box_alert(title="Notification",
                                    content=f"Connected to device: {selected_camera[1]}")
        # # Persist config
        ConfigManagement.set_config(section = "Camera1",
                                    option = "device_name",
                                    value = selected_camera[1])
        ConfigManagement.set_config(section = "Camera1",
                                    option = "index",
                                    value = str(selected_camera[0]))

    def show_message_box_alert(self,
                         title: str,
                         content: str,
                         mode: QtWidgets.QMessageBox = QtWidgets.QMessageBox.Warning,):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(mode)
        # setting message for Message Box
        msg.setText(content)
        # setting Message box window title
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # start the app
        msg.exec_()

    def default_setting(self) -> None:
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

        # Set widget style
        self.set_widget_style()

        # Cam setting combo box with default value
        self.cam1_cbx.clear()
        self.cam1_cbx.addItem("No Devices")
        self.add_camera_info()
        self.cam1_cbx.activated.connect(self.selected_camera_event_handler)

        # Camera1 Display setting
        self.cam1_display.setAlignment(QtCore.Qt.AlignCenter)
        pix_map = QtGui.QPixmap("icons/no_image.jpg")
        self.cam1_display.setFixedSize(640, 480)
        self.cam1_display.setPixmap(pix_map)

    def set_widget_style(self):
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
                        width: 45px;
                        height: 45px;          
                    }
                    QCheckBox::indicator:unchecked{
                        image: url(icons/toggle_off.png);
                        width: 45px;
                        height: 45px;           
                    }
                """)

        self.setting_btn.setStyleSheet("""
                    QPushButton{
                        background-color: rgb(218, 145, 0);
                        padding-left:100px;
                        text-align: left
                    }
                """)

        self.preview_btn.setStyleSheet("""
                    QPushButton{
                        padding-left:100px;
                        text-align: left
                    }
                """)

    def add_camera_info(self) :
        # Get camera infor
        cameras_infor = CameraComponents.get_available_cameras()
        self.__list_camera = []
        # Clear list
        if len(cameras_infor) == 0:
            return

        # Clear list
        self.cam1_cbx.clear()
        self.cam1_cbx.addItem("None")

        # Add item
        for (i,camera_infor) in enumerate(cameras_infor):
            camera_name = camera_infor[1]
            self.cam1_cbx.addItem(f"{i}. {camera_name}")
        self.__list_camera = cameras_infor

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
