"""密钥激活窗口。"""
import tkinter as tk
import tkinter.messagebox as tkmsg
import wmi
import os

import main_GUI
import ico
import rsa_crypt


class LoginGUI(object):
    def __init__(self, root: tk.Tk):
        """构造函数。"""
        # 根窗口
        self.root_window = root
        self.root_window.title("未激活")
        self.root_window.iconbitmap("./ico")
        self.root_window.resizable(False, False)
        self.entry_key = tk.Text()  # 密钥输入框。

        self.check()

    def init_window(self):
        """初始化窗口。"""
        # login_window = tk.Frame(self.root_window)
        tk.Label(self.root_window, text="请输入激活码", font=("楷体", 14), ).grid(row=0, column=0)
        self.entry_key = tk.Text(self.root_window, width=64, height=5, font=("楷体", 14))
        self.entry_key.grid(row=1, column=0)
        tk.Button(self.root_window, text="激活", font=("楷体", 14),
                  command=self.save_key).grid(row=2, column=0, sticky=tk.W)
        tk.Button(self.root_window, text="退出", font=("楷体", 14),
                  command=self.root_window.destroy).grid(row=2, column=0, sticky=tk.E)
        # login_window.pack()

    def check(self):
        """检查激活码。"""
        self.destroy_frame()
        self.init_window()
        hardware_id = wmi.WMI()
        board_id = hardware_id.Win32_BaseBoard()[0].SerialNumber.strip()
        # print(board_id)

        if not os.path.isfile("./key"):
            tkmsg.showinfo(title="警告",
                           message="未检测到激活码\n"
                                   "复制最下方数据\n"
                                   "发送到bh.3rd@qq.com\n"
                                   "重新获取激活码！\n" + str(board_id), )
            self.entry_key.insert(tk.END, str(board_id))
            self.root_window.mainloop()
        else:
            rsa = rsa_crypt.Encrypt()
            with open("./key", 'rb') as key_file:
                key = key_file.read()
            if rsa.rsa_decrypt(key) == board_id:
                self.destroy_frame()
                main_GUI.MainGUI(self.root_window).init_window()
            else:
                tkmsg.showinfo(title="警告",
                               message="激活码错误\n"
                                       "复制最下方数据\n"
                                       "发送到bh.3rd@qq.com\n"
                                       "重新获取激活码！\n" + str(board_id), )
                self.entry_key.insert(tk.END, str(board_id))
                self.root_window.mainloop()

    def save_key(self):
        """保存激活码。"""
        with open("./key", 'wb') as key_file:
            print(self.entry_key.get("0.0", tk.END))
            key_file.write(self.entry_key.get("0.0", tk.END).encode())
        self.check()

    def destroy_frame(self):
        """清空窗口。"""
        for widget in self.root_window.winfo_children():
            widget.destroy()


if __name__ == '__main__':
    wind = LoginGUI(tk.Tk())
