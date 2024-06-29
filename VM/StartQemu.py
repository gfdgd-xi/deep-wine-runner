#!/usr/bin/env python3
import os
import sys
import json
import traceback

def ReadTXT(file: str):
    with open(file, "r") as file:
        things = file.read()
    return things

# 运行
command = "qemu-system-x86_64"
#if "--kvm" in sys.argv:
#    command = "kvm"
programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
homePath = os.path.expanduser('~')
try:
    setting = json.loads(ReadTXT(f"{homePath}/.config/deepin-wine-runner/QemuSetting.json"))
except:
    print("无法读取配置")
    traceback.print_exc()
    sys.exit(1)
option = f"-nic model=rtl8139 --hda \"$HOME/Qemu/Windows/Windows.qcow2\" -usb -m {setting['Memory']}M -smp {setting['CPU']} "
if setting["EnableKVM"]:
    command = "kvm"
if setting["EnableRDP"]:
    option += "-net user,hostfwd=tcp::3389-:3389 "
if setting["EnableVNC"]:
    option += f"-display gtk -display vnc=:{setting['VNC']} "
if setting["EnableSound"]:
    option += "-soundhw all "
if os.path.exists(f"{homePath}/.config/deepin-wine-runner/QEMU-EFI"):
    if os.path.exists("/usr/share/qemu/OVMF.fd"):
        option += "--bios /usr/share/qemu/OVMF.fd "
    elif os.path.exists(f"{programPath}/OVMF.fd"):
        option += f"--bios {programPath}/OVMF.fd "
os.system(f"{command} {option}")
