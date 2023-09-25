"""一个模拟鼠标的按键精灵

可以设置按键频率、按键位置，使用键盘热键进行启停
"""
from pynput import keyboard, mouse


class SimulateMouse:
    def __init__(self, logger, click_count: int = 1):
        """构造函数"""
        # 创建监听器
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

        self._mouse = mouse.Controller()
        self._click_count = click_count

        self._logger = logger

        # 启动监听器
        self._listener.start()

        # 运行主循环
        self._listener.join()

    def _on_press(self, key):
        self._logger(f"{key} pressed\n")
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl:
            self._mouse.click(mouse.Button.left, self._click_count)

    def _on_release(self, key):
        self._logger(f"{key} released\n")
        if key == keyboard.Key.esc:
            self._listener.stop()


if __name__ == '__main__':
    SM = SimulateMouse(lambda log: print(log, end=""))
