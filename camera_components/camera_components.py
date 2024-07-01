import os
import platform
import cv2
class CameraComponents():

    @staticmethod
    def get_property() -> list:
        """Get camera properties (index, name) at current machine"""
        # Currently only support Linux
        os_name = platform.system()
        if os_name != "Linux":
            raise Exception("Only supporting for Linux OS")

        # Check if the video4linux directory exists
        camera_dir = '/sys/class/video4linux'
        if not os.path.exists(camera_dir):
            raise Exception(f"Path: {camera_dir} is not existed!")

        # Get infor
        camera_info = []
        # Iterate over devices in the video4linux directory
        for device in os.listdir(camera_dir):
            # Get the device index from the device name (e.g., video0, video1, ...)
            index = int(device[-1])
            # Read the device name from the device file
            with open(f'/sys/class/video4linux/{device}/name', 'r') as f:
                camera_name = f.read().strip()
            # Append camera index and name to the list
            camera_info.append((index, camera_name))

        return camera_info

    @staticmethod
    def isAvailableCamera(index: int) -> bool:

        # Check if camera is available
        cap = cv2.VideoCapture(index)
        return True if cap.isOpened() else False


