import os
import random
import shutil
import zipfile
import traceback
import subprocess
from getxmlimg import getsavexml

class ProgramInformation:
    programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
    version = "1.6.0Alpha2"
    updateTime = "2022年05月21日"
    websize = ["https://gitee.com/gfdgd-xi/uengine-runner", "https://github.com/gfdgd-xi/uengine-runner"]
    home = os.path.expanduser('~')
    developer = ["gfdgd xi<3025613752@qq.com>", "为什么您不喜欢熊出没和阿布呢<https://weibo.com/u/7755040136>", "星空露光<https://gitee.com/Cynorkyle>", "actionchen<917981399@qq.com>", "柚子<https://gitee.com/Limexb>"]
    lang = os.getenv('LANG')
    # 获取用户桌面目录
    def DesktopPath() -> "获取用户桌面目录":
        for line in open(get_home() + "/.config/user-dirs.dirs"):  # 以行来读取配置文件
            desktop_index = line.find("XDG_DESKTOP_DIR=\"")  # 寻找是否有对应项，有返回 0，没有返回 -1
            if desktop_index != -1:  # 如果有对应项
                break  # 结束循环
        if desktop_index == -1:  # 如果是提前结束，值一定≠-1，如果是没有提前结束，值一定＝-1
            return -1
        else:
            get = line[17:-2]  # 截取桌面目录路径
            get_index = get.find("$HOME")  # 寻找是否有对应的项，需要替换内容
            if get != -1:  # 如果有
                get = get.replace("$HOME", get_home())  # 则把其替换为用户目录（～）
            return get  # 返回目录

# 判断程序以正确方式运行
class Check:
    def CheckDepend():
        depend = ["/usr/bin/uengine", "UEngine", "/usr/bin/adb", "adb", "/usr/bin/uengine-session-launch-helper", "UEngine", "/usr/bin/aapt", "aapt"]
        for i in range(0, len(depend), 2):
            if not os.path.exists(depend[i]):
                print("依赖{}不存在".format(depend[i + 1]))

class ROOT:
    def GetRoot():
        return os.geteuid() == 0

class APK:
    def __init__(self, apkPath):
        self.apkPath = apkPath
    def install(self):
        os.system("pkexec /usr/bin/uengine-session-launch-helper -- uengine install --apk='{}'".format(self.apkPath))
    def uninstall(self):
        os.system("pkexec /usr/bin/uengine-session-launch-helper -- uengine uninstall --pkg='{}'".format(self.packageName()))
    def information(self):
        return subprocess.getoutput("aapt dump badging '{}'".format(self.apkPath))
    def activityName(self):
        info = self.information()
        for line in info.split('\n'):
            if "launchable-activity" in line:
                line = line[0: line.index("label='")]
                line = line.replace("launchable-activity: ", "")
                line = line.replace("'", "")
                line = line.replace(" ", "")
                line = line.replace("name=", "")
                line = line.replace("label=", "")
                line = line.replace("icon=", "")
                return line
    # 获取 apk 包名
    def packageName(self):
        info = self.information()
        for line in info.split('\n'):
            if "package:" in line:
                line = line[0: line.index("versionCode='")]
                line = line.replace("package:", "")
                line = line.replace("name=", "")
                line = line.replace("'", "")
                line = line.replace(" ", "")
                return line
    # 获取软件的中文名称
    def chineseLabel(self) -> "获取软件的中文名称":
        info = self.information()
        for line in info.split('\n'):
            if "application-label:" in line:
                line = line.replace("application-label:", "")
                line = line.replace("'", "")
                return line
    # 保存apk图标
    def saveApkIcon(self, iconSavePath) -> "保存 apk 文件的图标":
        try:
            if os.path.exists(iconSavePath):
                os.remove(iconSavePath)
            info = self.information()
            for line in info.split('\n'):
                if "application:" in line:
                    xmlpath = line.split(":")[-1].split()[-1].split("=")[-1].replace("'", "")
                    if xmlpath.endswith('.xml'):
                        xmlsave = getsavexml()
                        print(xmlpath)
                        xmlsave.savexml(self.apkPath, xmlpath, iconSavePath)
                        return
                    else:
                        zip = zipfile.ZipFile(self.apkPath)
                        iconData = zip.read(xmlpath)
                        with open(iconSavePath, 'w+b') as saveIconFile:
                            saveIconFile.write(iconData)
                            return
            print("None Icon! Show defult icon")
            shutil.copy(ProgramInformation.programPath + "/defult.png", iconSavePath)
        except:
            traceback.print_exc()
            print("Error, show defult icon")
            shutil.copy(ProgramInformation.programPath + "/defult.png", iconSavePath)
    def version(self):
        info = self.information()
        for line in info.split('\n'):
            if "package:" in line:
                if "compileSdkVersion='" in line:
                    line = line.replace(line[line.index("compileSdkVersion='"): -1], "")
                if "platform" in line:
                    line = line.replace(line[line.index("platform"): -1], "")
                line = line.replace(line[0: line.index("versionName='")], "")
                line = line.replace("versionName='", "")
                line = line.replace("'", "")
                line = line.replace(" ", "")
                return line
    def saveDesktopFile(self, desktopPath, iconPath):
        showName = self.chineseLabel()
        if showName == "" or showName == None:
            showName = "未知应用"
        self.saveApkIcon(iconPath)
        things = '''[Desktop Entry]
        Categories=app;
        Encoding=UTF-8
        Exec=uengine launch --action=android.intent.action.MAIN --package={} --component={}
        GenericName={}
        Icon={}
        MimeType=
        Name={}
        StartupWMClass={}
        Terminal=false
        Type=Application
        '''.format(self.packageName(), self.activityName(), showName, iconPath, showName, showName)
        File(desktopPath).write(things)
    def run(self):
        UEngine.OpenApp(self.packageName(), self.activityName())

    def buildDeb(self, savePath, qianZhui = True):
        tempPath = "/tmp/uengine-apk-builder-{}".format(int(random.randint(0, 1024)))
        #RunCommandShow("echo '======================================New===================================='")
        #RunCommandShow("echo '创建目录'")
        os.makedirs("{}/DEBIAN".format(tempPath))
        os.makedirs("{}/usr/share/applications".format(tempPath))
        os.makedirs("{}/usr/share/uengine/apk".format(tempPath))
        os.makedirs("{}/usr/share/uengine/icons".format(tempPath))
        apkPackageName = self.packageName()
        if qianZhui:
            apkPackageNameNew = "uengine-dc-" + self.packageName().lower()
        else:
            apkPackageNameNew = self.packageName().lower()
        apkPackageVersion = self.version()
        if apkPackageVersion[0].upper() == "V":
            package = list(apkPackageVersion)
            package.pop(0)
            apkPackageVersion = "".join(package)
        apkChineseLabel = self.chineseLabel()
        apkActivityName = self.activityName()
        iconSavePath = "{}/usr/share/uengine/icons/{}.png".format(tempPath, apkPackageNameNew)
        debControl = '''Package: {}
Version: {}
Architecture: all
Maintainer: {}
Depends: deepin-elf-verify (>= 0.0.16.7-1), uengine (>= 1.0.1)
Section: utils
Priority: optional
Description: {}\n'''.format(apkPackageNameNew, apkPackageVersion, apkChineseLabel, apkChineseLabel)
        debPostinst = '''#!/bin/sh

APK_DIR="/usr/share/uengine/apk"
APK_NAME="{}"
APK_PATH="$APK_DIR/$APK_NAME"
DESKTOP_FILE="{}"


if [ -f $APK_PATH ]; then
    echo "Installing $APK_NAME"
else 
    echo "ERROR: $APK_NAME does not exist."
    exit 0
fi

session_manager=`ps -ef | grep "uengine session-manager" | grep -v grep`
if test -z "$session_manager"; then
    echo "ERROR: app install failed(session-manager is not running)."
    sess_dir="/usr/share/uengine/session_install"
    if [ ! -d $sess_dir ]; then
        mkdir $sess_dir
        chmod 777 $sess_dir
    fi
    apk_name=${{APK_PATH##*/}}
    fileName="$sess_dir/$apk_name"
    echo $DESKTOP_FILE > $fileName
    abistr=""
    if test -n "$abistr"; then
        abi=`echo $abistr |awk -F \= '{{print $2}}'`
        echo $abi >> $fileName
    fi
    chmod 766 $fileName
fi

/usr/bin/uengine-session-launch-helper -- uengine install  --apk="$APK_PATH"

exit 0'''.format(apkPackageNameNew + ".apk", "/usr/share/applications/{}.desktop".format(apkPackageNameNew))
        debPrerm = '''#!/bin/sh

APP_NAME="{}"
DESKTOP_FILE="{}"

session_manager=`ps -ef | grep "uengine session-manager" | grep -v grep`
if test -z "$session_manager"; then
    echo "ERROR: app uninstall failed(session-manager is not running)."
    sess_dir="/usr/share/uengine/session_uninstall"
    if [ ! -d $sess_dir ]; then
        mkdir $sess_dir
        chmod 777 $sess_dir
    fi
    fileName="$sess_dir/$APP_NAME"
    echo $DESKTOP_FILE > $fileName
    chmod 766 $fileName
fi

echo "Uninstalling $APP_NAME"
/usr/bin/uengine-session-launch-helper -- uengine uninstall --pkg="$APP_NAME"

exit 0'''.format(apkPackageName, "/usr/share/applications/{}.desktop".format(apkPackageNameNew))
        desktopFile = '''[Desktop Entry]
Categories=Other;
Exec=uengine launch --action=android.intent.action.MAIN --package={} --component={}
Icon=/usr/share/uengine/icons/{}.png
Terminal=false
Type=Application
GenericName={}
Name={}
'''
        # RunCommandShow("echo '{}' > '{}/DEBIAN/control'".format(debControl, tempPath))
        #RunCommandShow("echo 正在写入文件：'{}/DEBIAN/control'".format(tempPath))
        File("{}/DEBIAN/control".format(tempPath)).write(debControl)
        #RunCommandShow("echo 正在写入文件：'{}/DEBIAN/postinst'".format(tempPath))
        File("{}/DEBIAN/postinst".format(tempPath)).write(debPostinst)
        #RunCommandShow("echo 正在写入文件：'{}/DEBIAN/prerm'".format(tempPath))
        File("{}/DEBIAN/prerm".format(tempPath)).write(debPrerm)
        #RunCommandShow("echo 正在写入文件：'/usr/share/applications/{}.desktop'".format(apkPackageNameNew))
        # write_txt("{}/usr/share/applications/{}.desktop".format(tempPath, apkPackageNameNew), desktopFile)
        self.saveDesktopFile("{}/usr/share/applications/{}.desktop".format(tempPath, apkPackageNameNew),
                             "{}/usr/share/uengine/icons/{}.png".format(tempPath, apkPackageNameNew))
        #BuildUengineDesktop(apkPackageName, apkActivityName, apkChineseLabel,
        #                    "/usr/share/uengine/icons/{}.png".format(apkPackageNameNew),
        #                    "{}/usr/share/applications/{}.desktop".format(tempPath, apkPackageNameNew))
        #RunCommandShow("echo '复制文件'")
        #RunCommandShow("echo '写入 APK 软件图标'")
        #SaveApkIcon(apkPath, iconSavePath)
        self.saveApkIcon(iconSavePath)
        #RunCommandShow("echo '复制 APK 文件'")
        shutil.copy(self.apkPath, "{}/usr/share/uengine/apk/{}.apk".format(tempPath, apkPackageNameNew))
        #RunCommandShow("cp -rv '{}' '{}/usr/share/uengine/apk/{}.apk'".format(apkPath, tempPath, apkPackageNameNew))
        #RunCommandShow("echo '正在设置文件权限……'")
        os.system("chmod 0775 -vR '{}/DEBIAN/postinst'".format(tempPath))
        os.system("chmod 0775 -vR '{}/DEBIAN/prerm'".format(tempPath))
        #RunCommandShow("echo '打包 deb 到桌面……'")
        os.system(
            "dpkg -b '{}' '{}'".format(tempPath, savePath))
        #RunCommandShow("echo '正在删除临时目录……'")
        #shutil.rmtree(tempPath)
        #RunCommandShow("rm -rfv '{}'".format(tempPath))
        #RunCommandShow("echo '完成！'")
        #findApkHistory.append(apkPath)
        #combobox1['value'] = findApkHistory
        #write_txt(get_home() + "/.config/uengine-runner/FindApkBuildHistory.json",
        #          str(json.dumps(ListToDictionary(findApkHistory))))  # 将历史记录的数组转换为字典并写入
        #messagebox.showinfo(title="提示", message="打包完成")
        #DisabledAndEnbled(False)


class UEngine:
    def UengineAppManager():
        os.system("uengine launch --package=org.anbox.appmgr --component=org.anbox.appmgr.AppViewActivity")
    def OpenApp(appPackage, appActivity):
        os.system("uengine launch --package={} --component={}".format(appPackage, appActivity))
    # 清空 uengine 数据
    def UengineDataClean() -> "清空 uengine 数据":
        shutil.rmtree("{}/.local/share/applications/uengine/".format(ProgramInformation.home))
        shutil.rmtree("/data/uengine")
    def RemoveUengineCheck():
        os.remove("/usr/share/uengine/uengine-check-runnable.sh")
    def CPUCheck():
        return subprocess.getoutput("uengine check-features")
    def BuildUengineRootImage():
        os.system(ProgramInformation.programPath + "/root-uengine.sh")
    def OpenUengineRootData():
        os.system("xdg-open /data/uengine/data/data")
    def InstallRootUengineImage():
        if not os.path.exists:
            os.mkdir("/tmp/uengine-runner")
        File("/tmp/uengine-runner/install.sh").write("sudo dpkg -i /tmp/uengine-runner/u*.deb\nsudo apt install -f")
        os.system("wget -P '/tmp/uengine-runner' 'https://hub.fastgit.xyz/gfdgd-xi/uengine-runner/releases/download/U1.2.15/uengine-android-image_1.2.15_amd64.deb' && pkexec bash '/tmp/uengine-runner/install.sh'")
    class Services:
        def Open():
            os.system("pkexec systemctl enable uengine-container uengine-session && systemctl start uengine-container uengine-session")
        def Close():
            os.system("pkexec systemctl disable uengine-container uengine-session")
        def Restart():
            os.system("pkexec systemctl restart uengine*")
    class InternetBridge:
        def Open():
            os.system("pkexec uengine-bridge.sh start")
        def Close():
            os.system("pkexec uengine-bridge.sh stop")
        def Restart():
            os.system("pkexec uengine-bridge.sh restart")
        def Reload():
            os.system("pkexec uengine-bridge.sh reload")
        def ForceReload():
            os.system("pkexec uengine-bridge.sh force-reload")

class Adb:
    def __init__(self, ip=""):
        self.ip = ip

    def connect(self):
        os.system(f"adb connect {self.ip}")

    class Service:
        def Open():
            os.system("adb start-server")
        def Close():
            os.system("adb kill-server")
        def Kill():
            os.system("killall adb")

    def boolAndroidInstallOtherAppSetting(self):
        return subprocess.getoutput(f"adb -s {self.ip} shell settings get secure install_non_market_apps").replace(" ", "") == "1"

    def setAndroidInstallOtherAppSetting(self, op: bool):
        os.system(f"adb -s {self.ip} shell settings put secure install_non_market_apps {int(op)}")

class File:
    def __init__(self, filePath):
        self.filePath = filePath
    def read(self):
        f = open(self.filePath, "r")  # 设置文件对象
        str = f.read()  # 获取内容
        f.close()  # 关闭文本对象
        return str  # 返回结果
    def write(self, things) -> "写入文本文档":
        TxtDir = os.path.dirname(self.filePath)
        print(TxtDir)
        if not os.path.exists(TxtDir):
            os.makedirs(TxtDir, exist_ok=True)
        file = open(self.filePath, 'w', encoding='UTF-8')  # 设置文件对象
        file.write(things)  # 写入文本
        file.close()  # 关闭文本对象

class UengineRunner:
    def CleanHistory():
        shutil.rmtree(ProgramInformation.home + "/.config/uengine-runner")

if __name__ == "__main__":
    print("本 API 不支持直接运行，请通过引入的方式使用此 API")
    adb = Adb("192.168.250.2:5555")
    print(adb.boolAndroidInstallOtherAppSetting())

    quit()

if not ROOT.GetRoot():
    print("请获取 ROOT 权限以便更好的使用该 API")