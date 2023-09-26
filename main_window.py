"""主窗口"""
from icon import icon_png
from simulate_mouse import SimulateMouse

import threading
import tkinter as tk
import tkinter.ttk as ttk


class MainWindow:
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

        self._root_window.title("按键精灵V2.0.0")
        self._root_window.iconphoto(True, tk.PhotoImage(data=icon_png))

        self._output_text = tk.Text()  # 文本框
        self._progress_bar = ttk.Progressbar()  # 进度条

        """窗口初始化"""
        select_frame = tk.Frame(self._root_window)  # 选择频率下拉框
        tk.Label(
            select_frame,
            text="按键频率 N (建议100<N<300)",
            font=(self._font, self._font_size)
        ).grid(row=0, column=0)
        cbox = ttk.Combobox(
            select_frame,
            width=4,
            font=(self._font, self._font_size),
            values=[10, 20, 30, 40, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
        )
        cbox.current(5)  # 默认序号
        cbox.grid(row=0, column=1)
        select_frame.pack()

        # 输出文本框
        text_frame = tk.Frame(self._root_window)
        select_frame.update()
        self._output_text = tk.Text(
            text_frame,
            width=select_frame.winfo_width() // 10, height=12,
            font=(self._font, self._font_size), bg="black", fg="yellow",
            undo=True, autoseparators=False
        )
        self._output_text.insert(tk.END, "点击开始后，按住Ctrl开始自动点击，按Esc停止点击。\n")
        self._output_text.pack(expand=True, fill=tk.BOTH)
        text_frame.pack(expand=True, fill=tk.BOTH)

        # 进度条
        bar_frame = tk.Frame(self._root_window)
        self._progress_bar = ttk.Progressbar(bar_frame,
                                             length=select_frame.winfo_width(),
                                             mode="indeterminate",
                                             orient=tk.HORIZONTAL)
        self._progress_bar.pack(fill=tk.BOTH)
        bar_frame.pack(fill=tk.BOTH)

        # 按钮
        button_frame = tk.Frame(self._root_window)
        button_frame.grid_columnconfigure(0, weight=1)  # 设置第一列的权重为1
        button_frame.grid_columnconfigure(1, weight=1)  # 设置第二列的权重为1
        tk.Button(
            button_frame,
            text="开始",
            font=(self._font, self._font_size),
            padx=select_frame.winfo_width() // 8,
            command=lambda: self._detach_thread(self._on_button_start_click, int(cbox.get()))
        ).grid(row=0, column=0, sticky=tk.W)
        tk.Button(
            button_frame,
            text="退出",
            font=(self._font, self._font_size),
            padx=select_frame.winfo_width() // 8,
            command=self._root_window.destroy
        ).grid(row=0, column=1, sticky=tk.E)
        button_frame.pack(fill=tk.BOTH)

        self._root_window.mainloop()

    @staticmethod
    def _detach_thread(target, *args, **kwargs):
        """
        分离线程，后台执行任务
        Args:
            *args:

        Returns:

        """
        task_thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
        task_thread.start()

    def _on_button_start_click(self, freq: int):
        """
        模拟鼠标点击
        Args:
            freq: 点击频率

        Returns:

        """
        self._progress_bar.start()

        def output(log: str):
            self._output_text.insert(tk.END, log)
            self._output_text.see(tk.END)

        SimulateMouse(output, freq)
        self._progress_bar.stop()


if __name__ == '__main__':
    wind = MainWindow(tk.Tk())
