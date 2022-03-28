"""生成图形化窗口。

例程:

wind = MainGUI(tk.Tk())

wind.init_window()
"""
import threading
import tkinter as tk
import tkinter.ttk as ttk
import keyboard

import simulate_mouse


class MainGUI(object):
    """生成图形化窗口。"""

    def __init__(self, root: tk.Tk):
        """构造函数。"""
        # 根窗口
        self.root_window = root
        self.root_window.title("按键精灵V1.1")
        self.root_window.iconbitmap("./ico")
        self.root_window.resizable(False, False)

        self.sm = simulate_mouse.SimulateMouse()  # 模拟鼠标类的实例。
        self.output_text = tk.Text()  # 文本框。
        self.bar = ttk.Progressbar()  # 进度条。

    def init_window(self):
        """窗口初始化。"""
        # 选择频率下拉框
        select_frame = tk.Frame(self.root_window)
        tk.Label(select_frame,
                 text="按键频率N(建议100<N<300)",
                 font=("楷体", 16), ).grid(row=0, column=0, )
        select_list = [10, 20, 30, 40, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
        cbox = ttk.Combobox(select_frame, width=4, font=("楷体", 16), values=select_list)
        cbox.current(5)  # 默认序号
        cbox.grid(row=0, column=1, )
        select_frame.pack()

        # 输出文本框
        text_frame = tk.Frame(self.root_window)
        select_frame.update()
        self.output_text = tk.Text(text_frame,
                                   width=select_frame.winfo_width() // 10, height=12,
                                   font=("楷体", 14), bg="black", fg="yellow",
                                   undo=True, autoseparators=False, )
        self.output_text.insert(tk.END,
                                "按CTRL+ALT+1记录按键坐标\n"
                                "按CTRL+ALT+2开始自动点击\n"
                                "按CTRL+ALT+3停止自动点击\n")
        self.output_text.pack()
        text_frame.pack()

        # 进度条
        bar_frame = tk.Frame(self.root_window)
        self.bar = ttk.Progressbar(bar_frame,
                                   length=select_frame.winfo_width(),
                                   mode="indeterminate",
                                   orient=tk.HORIZONTAL)
        self.bar.pack()
        bar_frame.pack()

        # 按钮
        button_frame = tk.Frame(self.root_window)
        tk.Button(button_frame, text="开始", font=("楷体", 14), padx=select_frame.winfo_width() // 8,
                  command=lambda: self.thread_detach(self.do_task, int(cbox.get()))).grid(row=0, column=0, )
        tk.Button(button_frame, text="退出", font=("楷体", 14), padx=select_frame.winfo_width() // 8,
                  command=self.root_window.destroy).grid(row=0, column=1, )
        button_frame.pack()

        self.root_window.mainloop()

    # 分离线程，后台执行任务。
    @staticmethod
    def thread_detach(func, *args):
        task_thread = threading.Thread(target=func, args=args)
        task_thread.setDaemon(True)
        task_thread.start()

    # 执行任务
    def do_task(self, freq: int):
        self.bar.start()
        while True:
            self.sm.del_data()
            if keyboard.is_pressed('ctrl+alt+1'):
                self.sm.get_mouse_position()
                insert_text = "记录按键坐标：" + str(self.sm.mouse_position) + '\n'
                self.output_text.insert(tk.END, insert_text)
                # print("记录坐标：", self.sm.mouse_position)
                break

        while True:
            if keyboard.is_pressed('ctrl+alt+2'):
                insert_text = "开始自动点击！\n"
                self.output_text.insert(tk.END, insert_text)
                while not keyboard.is_pressed('ctrl+alt+3'):
                    self.sm.mouse_click(freq)
                insert_text = "停止自动点击！\n"
                self.output_text.insert(tk.END, insert_text)
                break
        self.bar.stop()


if __name__ == '__main__':
    wind = MainGUI(tk.Tk())
    wind.init_window()
