from Xlib.display import Display
from typing import Tuple
class DisplayComponents():
    @staticmethod
    def get_resolution(display_index :int = 0) -> Tuple[int,int]:
        try:
            screen = Display(f':{display_index}').screen()
            # Get resolution
            screen_width = int(screen.width_in_pixels)
            screen_height = int(screen.height_in_pixels)
            return (screen_width,screen_height)

        except Exception as e:
            raise Exception(e)
