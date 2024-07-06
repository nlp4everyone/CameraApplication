import sys, cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from camera_components import CameraComponents
from config_component import ConfigManagement
from datetime import datetime
from base_ui_app import BaseUI
from typing import Literal
now = datetime.now()

class Feature_MainWindow(BaseUI):
    def __init__(self):
        super().__init__()
        # Load default UI setting
        self.default_setting()

        self.cap = None
        # Load camera config
        index, device = self.load_camera_config()
        # Verify camera
        state = self.verify_camera_info(index=index, device_name=device)
        index = 0 if not state else int(index) + 1
        self.cam1_cbx.setCurrentIndex(index)

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
        selected_camera = self.get_available_cameras()[index]

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

    def default_setting(self):
        #  Inherit function from parent class
        super().default_setting()

        # UI button event
        self.exit_btn.clicked.connect(self.close_event_handler)
        self.close_btn.clicked.connect(self.close_event_handler)
        self.max_btn.clicked.connect(self.full_screen_event_handler)
        self.min_btn.clicked.connect(self.minimum_event_handler)
        self.hide_btn.clicked.connect(self.hide_event_handler)

        # Feature button event
        self.setting_btn.clicked.connect(self.setting_mode_handler)
        self.preview_btn.clicked.connect(self.preview_mode_handler)

        # Cam setting combo box with default value
        self.cam1_cbx.clear()
        self.cam1_cbx.addItem("No Devices")
        self.append_list_cameras()
        self.cam1_cbx.activated.connect(self.selected_camera_event_handler)


    def full_screen_event_handler(self) -> None:
        # When scrren is maximized!
        if self.isMaximized():
            self.show_message_box_alert(title="Warning",
                                        content="You're currently in Full-screen mode!")

        # Inherit function from parent class
        super().full_screen_event_handler()

    def minimum_event_handler(self) -> None:
        # When scrren is maximized!
        if not self.isMaximized():
            self.show_message_box_alert(title="Warning",
                                        content="You're currently in Normal mode!")

        # Inherit function from parent class
        super().minimum_event_handler()

    def setting_mode_handler(self) -> None:
        # Inherit function from parent class
        super().setting_mode_handler()

        # Release Cv2 Cap
        if self.cap != None:
            if self.cap.isOpened(): self.cap.release()

    def preview_mode_handler(self) -> None:
        # Inherit function from parent class
        super().preview_mode_handler()

        # Load camera
        index, device = self.load_camera_config()
        # Verify camera
        state = self.verify_camera_info(index=index, device_name=device)

        # When no camera is suitable
        cbx_index = 0 if not state else int(index) + 1
        self.cam1_cbx.setCurrentIndex(cbx_index)

        if cbx_index != 0:
            # Default setting
            self.initCamera(int(index))
            fps = self.cap.get(5)
            self.add_notification(f"Connect to device: {device} with default FPS: {fps}")


    def get_available_cameras(self):
        return CameraComponents.get_available_cameras()

    def append_list_cameras(self) :
        # Get camera infor
        cameras_infor = self.get_available_cameras()

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

    def load_camera_config(self, section_name :Literal["Camera1","Camera2"] = "Camera1"):
        # Load config
        camera1_config = ConfigManagement.get_sections_config(section_name)
        index = camera1_config[section_name]["index"]
        device = camera1_config[section_name]["device_name"]
        return index, device

    def verify_camera_info(self, index :int, device_name :str):
        # Verify step
        # When index is None, set default
        if index == "":
            return False

        # No available devices
        list_device = self.get_available_cameras()
        if len(list_device) == 0:
            return False

        index = int(index)
        # Not correct index
        if index > len(list_device) -1:
            return False

        # Verify if saved device name is current device
        if list_device[index][1] == device_name:
            return True
        return False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Feature_MainWindow()
    ui.show()
    sys.exit(app.exec_())
