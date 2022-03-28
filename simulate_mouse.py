"""一个模拟鼠标的按键精灵。

可以设置按键频率、按键位置，使用键盘热键进行启停。

例程:

foo = SimulateMouse()

foo.get_mouse_position()

foo.mouse_click(100)
"""
import pyautogui
import keyboard


class SimulateMouse(object):
    """模拟鼠标操作。

    设置好频率，获取鼠标X、Y坐标，按热键启停。

    Attributes:
        screen_size: 包含屏幕尺寸的元组，两个整数。
        mouse_position: 包含鼠标坐标的元组，两个整数。
        frequency: 点击频率。
    """

    def __init__(self):
        """构造函数。"""
        self.screen_size = ()
        self.mouse_position = ()
        self.frequency = 0

    def get_screen_size(self):
        """获取屏幕分辨率。"""
        self.screen_size += pyautogui.size()

    def get_mouse_position(self):
        """获取鼠标坐标，以左上角为坐标原点。"""
        self.mouse_position += pyautogui.position()

    def mouse_click(self, freq: int):
        """以给定频率执行鼠标左击。

        Args:
            freq: 频率。
        """
        pyautogui.click(self.mouse_position, clicks=freq, )

    def del_data(self):
        """清空并刷新数据。"""
        del self.mouse_position, self.screen_size
        self.screen_size = ()
        self.mouse_position = ()


if __name__ == '__main__':
    SM = SimulateMouse()
    while True:
        if keyboard.is_pressed('ctrl+alt+1'):
            SM.get_mouse_position()
            print("记录坐标：", SM.mouse_position)
            break

    while not keyboard.is_pressed('ctrl+alt+3'):
        if keyboard.is_pressed('ctrl+alt+2'):
            SM.mouse_click(100)
