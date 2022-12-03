#!/usr/bin/env python3
import os
import sys
import getpass
import PyQt5.QtWidgets as QtWidgets

if __name__ == "__main__":
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    homePath = os.getenv("HOME")
    if len(sys.argv) <= 2:
        print("参数不足")
        sys.exit(1)
    app = QtWidgets.QApplication(sys.argv)
    # 判断是否已下载镜像
    if not os.path.exists(f"{homePath}/.deepin-wine-runner-ubuntu-images/{sys.argv[1]}"):
        QtWidgets.QMessageBox.information(None, "提示", "此镜像未下载解压，无法继续")
        exit()
    commandList = ""
    userName = getpass.getuser()
    for i in sys.argv[2:]:
        commandList += f"'{i}' "
    # 判断是否挂载
    if not os.path.ismount(f"{homePath}/.deepin-wine-runner-ubuntu-images/{sys.argv[1]}/proc"):
        print("文件暂未挂载，开始挂载")
        sys.exit(os.system(f"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY  bash '{programPath}/Mount.sh' '{homePath}/.deepin-wine-runner-ubuntu-images/{sys.argv[1]}' '{userName}' {commandList}"))
    sys.exit(os.system(f"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY  chroot '--userspec={userName}:{userName}' '{homePath}/.deepin-wine-runner-ubuntu-images/{sys.argv[1]}/' env 'HOME=/home/{userName}' {commandList}"))
