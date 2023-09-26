# 按键精灵

*一个`Tkinter`的demo，用于学习`Tkinter`的布局方法以及简单的`GUI`程序设计。*

## 程序逻辑

1. 通过**RSA加密算法**实现登陆窗口的激活码设计，激活后销毁所有控件进入主界面。
2. 在主界面点击**开始**按钮实现后台监听按键，并在触发`Ctrl`时在指针位置模拟鼠标左键点击；触发`Esc`时退出按键监听。
3. 主界面点击**退出**按钮，退出程序。

## 文件描述

- `simulate_mouse.py`: 监听按键并模拟键鼠
- `login_window.py`:绘制登陆激活界面
- `main_window.py`:绘制主界面
- `icon.py`: 将图标嵌入程序
- `rsa_crypt.py`: 调用RSA库验证密钥

## 安装依赖

```shell
pip install -r requirements.txt
```

## 打包

- `pyinstaller`
    - 安装：
      ```shell
      pip install pyinstaller
      ```

    - 打包：
      ```shell
      pyinstaller --clean -F main_window.py -w -i icon.ico -n 按键精灵
      ```

- `nuitka`
    - 安装：
      ```shell
      pip install nuitka
      pip install zstandard
      ```

    - 打包：
      ```shell
      python -m nuitka --standalone --show-memory --show-progress --follow-import-to=need --enable-plugin=tk-inter --output-dir=output --windows-disable-console --windows-icon-from-ico=icon.ico --lto=yes --onefile -o 按键精灵 main_window.py
      ```
