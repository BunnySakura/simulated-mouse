"""激活窗口"""
from main_window import MainWindow
import ico
from rsa_crypt import RsaEncrypt

import tkinter as tk
from tkinter import messagebox as tkmsg
import uuid
import os


class LoginWindow:
    _font = "楷体"  # 字体
    _font_size = 16  # 字体大小

    def __init__(self, root: tk.Tk):
        """
        初始化窗口
        
        Args:
            root: 根窗口
        """
        self._root_window = root

        self._root_window.minsize(
            self._root_window.winfo_screenwidth() // 2,
            self._root_window.winfo_screenheight() // 2
        )  # 设置窗口最小大小

        # 文本框自适应窗口大小
        self._root_window.grid_rowconfigure(1, weight=1)
        self._root_window.grid_columnconfigure(0, weight=1)

        # 初始化窗口内容
        self._root_window.title("未激活")
        self._root_window.iconbitmap("./ico")
        tk.Label(
            self._root_window, text="请输入激活码", font=(self._font, self._font_size)
        ).grid(row=0, column=0)
        self._input_key = tk.Text(self._root_window, font=(self._font, self._font_size))  # 密钥输入框
        self._input_key.grid(row=1, column=0, sticky=tk.NSEW)
        tk.Button(
            self._root_window, text="激活", font=(self._font, self._font_size), command=self._active
        ).grid(row=2, column=0, sticky=tk.W)
        tk.Button(
            self._root_window, text="退出", font=(self._font, self._font_size), command=self._root_window.destroy
        ).grid(row=2, column=0, sticky=tk.E)

        self._check()
        self._root_window.mainloop()

    @staticmethod
    def _generate_unique_id() -> str:
        # 使用设备的MAC地址生成唯一ID
        mac_address = uuid.getnode()
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(mac_address)))

    def _warning_pop_up(self):
        # 警告弹窗
        device_uuid = self._generate_unique_id()
        tkmsg.showinfo(
            title="警告",
            message="未检测到激活码或激活码错误。\n复制下方设备ID发送到python@py.com,重新获取激活码！\n"
                    + device_uuid,
        )
        self._input_key.delete(1.0, tk.END)
        self._input_key.insert(tk.END, device_uuid)

    def _open_main_window(self):
        # 销毁当前顶级窗口的所有控件
        for widget in self._root_window.winfo_children():
            widget.destroy()
        MainWindow(self._root_window)

    def _active(self):
        self._save_key()
        self._check()

    def _check(self):
        """检查激活码"""
        device_uuid = self._generate_unique_id()
        if not os.path.isfile("./key"):
            self._warning_pop_up()
        else:
            rsa = RsaEncrypt()
            with open("./key", 'rb') as key_file:
                key = key_file.read()
            if rsa.rsa_decrypt(key) == device_uuid:
                self._open_main_window()
            else:
                self._warning_pop_up()

    def _save_key(self):
        """保存激活码"""
        with open("./key", 'wb') as key_file:
            key = self._input_key.get("1.0", tk.END)
            key_file.write(key.encode())


if __name__ == '__main__':
    wind = LoginWindow(tk.Tk())
