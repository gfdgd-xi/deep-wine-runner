#!/bin/bash

#最终生成的包的描述
export app_description="Deepin-plantsvszombies"
#应用程序英文名
export app_name="Deepin-plantsvszombies"
#应用程序中文名
export app_name_zh_cn="Deepin-plantsvszombies"
#desktop文件中的分类
export desktop_file_categories="Network;"
#desktop文件中StartupWMClass字段。用于让桌面组件将窗口类名与desktop文件相对应。这个值为实际运行的主程序EXE的文件名，wine/crossover在程序运行后会将文件名设置为窗口类名
export desktop_file_main_exe="PlantsVsZombies.exe"
export exec_path="c:/Program Files/plantsvszombies/PlantsVsZombies.exe"
#最终生成的包的包名,包名的命名规则以deepin开头，加官网域名（需要前后对调位置），如还不能区分再加上应用名
export deb_package_name="Deepin-plantsvszombies"
#最终生成的包的版本号，版本号命名规则：应用版本号+deepin+数字
export deb_version_string="1"
#读取和最终解压的包名
export bottle_name="Deepin-plantsvszombies"

export package_depends="deepin-wine6-stable:amd64 (>= 6.0.0.12-1), deepin-wine-helper (>= 5.1.25-1)"
export apprun_cmd="deepin-wine6-stable"
#export package_depends="deepin-wine5-stable:amd64 (>= 5.0.29-1), deepin-wine-helper (>= 5.1.25-1)"
#export apprun_cmd="deepin-wine5-stable"

# rm -fr final.dir/
# rm -fr icons/
# rm -fr staging.dir/

./script-packager.sh $@
