#!/usr/bin/env python3
import os
import sys
import getpass
import updatekiller
import PyQt5.QtWidgets as QtWidgets

if __name__ == "__main__":
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    homePath = os.getenv("HOME")
    if len(sys.argv) <= 1:
        print("参数不足")
        sys.exit(1)
    app = QtWidgets.QApplication(sys.argv)
    # 判断是否已下载镜像
    if not os.path.exists(f"{homePath}/.deepin-wine-runner-ubuntu-images/{sys.argv[1]}"):
        QtWidgets.QMessageBox.information(None, "提示", "此镜像未下载解压，无法继续")
        exit()
    commandList = ""
    userName = getpass.getuser()
    for i in sys.argv[3:]:
        commandList += f"'{i}' "
    if commandList.replace(" ", "") == "":
        commandList = "bash"
    # 需要先取消挂载其它目录以防止冲突
    path = f"{homePath}/.deepin-wine-runner-ubuntu-images"
    for i in os.listdir(path):
        archPath = f"{path}/{i}"
        if os.path.isdir(archPath):
            for k in os.listdir(archPath):
                bottlePath = f"{archPath}/{k}"
                if os.path.isdir(bottlePath):
                    if f"{i}/{k}" == sys.argv[1]:
                        continue
                    if os.path.ismount(f"{bottlePath}/dev"):
                        os.system(f"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY bash '{programPath}/UnMount.sh' '{bottlePath}' ")
    os.system("touch /tmp/deepin-wine-runner-qemu-lock")
    # 判断是否挂载
    if not os.path.ismount(f"{homePath}/.deepin-wine-runner-ubuntu-images/{sys.argv[1]}/dev"):
        print("文件暂未挂载，开始挂载")
        if int(sys.argv[2]):
            sys.exit(os.system(f"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY  bash '{programPath}/MountWithoutHome.sh' '{homePath}/.deepin-wine-runner-ubuntu-images/{sys.argv[1]}' '{userName}' {commandList}"))
        else:
            sys.exit(os.system(f"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY  bash '{programPath}/Mount.sh' '{homePath}/.deepin-wine-runner-ubuntu-images/{sys.argv[1]}' '{userName}' {commandList}"))
    sys.exit(os.system(f"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY  chroot '--userspec={userName}:{userName}' '{homePath}/.deepin-wine-runner-ubuntu-images/{sys.argv[1]}/' env 'HOME=/home/{userName}' {commandList}"))
