# 按键精灵V1.1
*模拟鼠标点击，可以设置点击坐标、频率，使用热键启停。*

## 编程思路
通过激活码激活软件，故调用RSA库处理激活码校验，同时设计激活界面。激活后调用程序主界面，点击开始按钮开始监测热键。按下指定热键进行坐标定位、启动、停止，退出键退出。

## 文件描述
- `simulate_mouse.py`：提供鼠标模拟类；
- `login_window.py`：绘制激活界面；
- `main_window.py`：绘制程序主界面；
- `ico.py`：生成ICO图标以调用；
- `rsa_crypt.py`：调用RSA库验证密钥；
- `rsa_get_key.py`：调用RSA库获取激活密钥。

## 打包指令
```bash
pyinstaller.exe -F .\login_GUI.py -n 按键精灵V1.1 -w -i .\ico.ico
```

## 其他
**已打包激活功能为单独的类，可以单独使用。**
