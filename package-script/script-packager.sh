#!/bin/bash
#export elephant_deb_package_name=""
run_sh_dir=""
elephant_run_sh_dir=""
start_shell="/opt/deepinwine/tools/spark_run_v4.sh"
if [[ -n "$SPECIFY_SHELL_PATH" ]] && [[ "$SPECIFY_SHELL_PATH" == "/opt/apps"* ]];then
    start_shell="$SPECIFY_SHELL_PATH"
fi

wine_name="deepin-wine6-stable"
if [ -n "$apprun_cmd" ];then
    wine_name=${apprun_cmd%%/bin*}
    wine_name=${wine_name##*/}
fi

# export public_bottle_name="$deb_package_name"
# 为了满足用户自定义容器名的需求，更改
export public_bottle_name="$bottle_name"

CheckTool()
{
    a=$(which $1)
    if [ $? -ne 0 ]
    then
        echo "missing $1, need to install package \"$2\""
        exit
    fi
}
CheckParamE()
{
    if [ -z "$1" ]
    then
        echo "$2"
        exit 1
    fi
}
CheckPathExists()
{
    if [ ! -d "$1" ]
    then
        echo "$2"
        exit 1
    fi
}
RepalceVal()
{
    VALUE="$3"
    VALUE=$(echo ${VALUE//\\/\/})
    find "$1" -type f -exec sed -i "s#$2#$VALUE#" {} \;
}
TranslateTemplateFile()
{
    RepalceVal "$1" "@app_description@" "$app_description"
    RepalceVal "$1" "@app_name@" "$app_name"
    RepalceVal "$1" "@app_name_zh_cn@" "$app_name_zh_cn"
    RepalceVal "$1" "@deb_date@" "$deb_date"
    #RepalceVal "$1" "@deb_package_name@" "$deb_package_name"
    RepalceVal "$1" "@deb_packager@" "$deb_packager"
    RepalceVal "$1" "@deb_version_string@" "$deb_version_string"
    RepalceVal "$1" "@desktop_file_categories@" "$desktop_file_categories"
    #RepalceVal "$1" "@desktop_file_icon@" "$deb_package_name"
    RepalceVal "$1" "@desktop_file_main_exe@" "$desktop_file_main_exe"
    RepalceVal "$1" "@public_bottle_name@" "$public_bottle_name"
    RepalceVal "$1" "@old_package@" "$old_package_name"
    RepalceVal "$1" "@package_depends@" "$package_depends"
    RepalceVal "$1" "@mime_type@" "$mime_type"
    RepalceVal "$1" "@activex_name@" "$activex_name"
    RepalceVal "$1" "@make_autostart@" "$make_autostart"
    RepalceVal "$1" "@send_to_desktop@" "$send_to_desktop"
    RepalceVal "$1" "@exec_path@" "$EXEC_PATH"
}

TranslateTemplateFileUos()
{
    TranslateTemplateFile "$1"
    RepalceVal "$1" "@deb_package_name@" "$deb_package_name"
    RepalceVal "$1" "@desktop_file_icon@" "$deb_package_name"
    RepalceVal "$1" "@run_sh_dir@" "$run_sh_dir"
    RepalceVal "$1" "@start_shell_path@" "$start_shell"
    RepalceVal "$1" "@apprun_cmd@" "$wine_name"
    RepalceVal "$1" "@patch_loader@" "$patch_loader"
    RepalceVal "$1" "@version_info@" "$version_info"
    RepalceVal "$1" "@patch_version@" "$hack_patch_version"
}

Check_icons()
{
    if [[ -n $(find icons/ -name ${1}.svg) ]];then
        echo "${1}.svg"
    elif [[ -n $(find icons/ -name ${1}.png) ]];then
        echo "${1}.png"
    else
        exit 1
    fi
}

set_version_info()
{
    if [ $# -ne 3 ];then
    echo "invalid parameter"
    return 2
    fi

    file=$1
    key=$2
    new_value=$3
    cat $file | while read line; do
    name=`echo $line|awk -F '=' '{print $1}'`
    if [ "$name" = "$key" ];then
        line_num=`cat -n $file |grep $key|awk '{print $1}'`
        old_value=`echo $line|awk -F '=' '{print $2}'`
        sed -i ''$line_num's/'$old_value'/'$new_value'/g' $file
        return 0
    fi
    done
    return 1
}

checkInstallVersion()
{
    ver=$(dpkg -l $1 | grep ii | awk '{print $3}')
    if [ -z "$ver" ];then
        echo "$1 未安装"
        exit 0
    elif [ "$ver" != "$2" ];then
        echo "$1 版本不是$2"
        exit 1
    else
        echo $ver
    fi
}

checkWineDepends()
{
    WINE5LIBVER="5.0.28-1"
    WINE6LIBVER="6.0.0.11-1"
    WINEHELPERVER="5.1.25-1"

    if [ "$wine_name" == "deepin-wine5-stable" ];then
        checkInstallVersion ${wine_name}-i386 $WINE5LIBVER
        checkInstallVersion $wine_name $WINE5LIBVER
        echo "$WINE5LIBVER" > "$outfiles/wine_archive.md5sum"
    else
        checkInstallVersion ${wine_name}-i386 $WINE6LIBVER
        checkInstallVersion $wine_name $WINE6LIBVER
        echo "$WINE6LIBVER" > "$outfiles/wine_archive.md5sum"
    fi
    checkInstallVersion deepin-wine-helper $WINEHELPERVER
    checkInstallVersion deepin-wine-plugin $WINEHELPERVER

    cp /usr/lib/i386-linux-gnu/deepin-wine/gtkGetFileNameDlg "$outfiles"

    7z a -snh -snl -t7z -mx=9 -ms=on -mmt=on -m0=BCJ2 -m1=LZMA2:d=64m:fb=273 "$outfiles/wine_archive.7z" /usr/lib/i386-linux-gnu/deepin-wine5-stable/*
    echo "$WINELIBVER" > "$outfiles/wine_archive.md5sum"

    7z a -snh -snl -t7z -mx=9 -ms=on -mmt=on -m0=BCJ2 -m1=LZMA2:d=64m:fb=273 "$outfiles/helper_archive.7z" /opt/deepinwine/tools/*
    echo "$WINEHELPERVER" > "$outfiles/helper_archive.md5sum"
}

CheckTool "fakeroot" "fakeroot"

CheckParamE "$app_description" "App description not given"
CheckParamE "$app_name" "App name not given"
CheckParamE "$app_name_zh_cn" "App zh-cn name not given"
#CheckParamE "$desktop_file_categories" "Categories of desktop file not given"
#CheckParamE "$desktop_file_icon" "Icon file of desktop file not given"
CheckParamE "$desktop_file_main_exe" "Main exe filename not given
===>Wine set this value to WMClass of app window, Dock/Launcher need this for matching"
CheckParamE "$deb_package_name" "Package name not given"
CheckParamE "$deb_version_string" "Package version not given"

CheckParamE "$package_depends" "Package depends not given"

if [[ "$package_depends" == *"libc6"* ]];then
    echo "wine依赖直接改为deepin-wine5-stable或者deepin-wine6-stable"
    exit
fi

if [[ "$package_depends" != *"$wine_name"* ]];then
    echo "wine 依赖和执行的wine命令不匹配"
    exit
fi

BottlePath="$HOME/.deepinwine/$public_bottle_name"

./mkicons.sh
desktop_file_icon=$(Check_icons $deb_package_name)
#Replace USER value to string
EXEC_PATH=$(echo "$exec_path" | sed -e "s/$USER/\$USER/g")

if [ -n "$desktop_file_categories" ] && [ -z "$desktop_file_icon" ]; then
    echo "not found icon file"
    exit 1
fi

if [ -z "$deb_packager" ];then deb_packager="Deepin WINE Team";fi
if [ -z "$deb_packager_email" ];then deb_packager_email="penghao@linuxdeepin.com";fi
if [ -z "$deb_date" ];then deb_date=`date -R`;fi

echo "+++++ Empire Starts here. +++++"
echo "app description:     $app_description"
echo "app name:            $app_name"
echo "app name zh-cn:      $app_name_zh_cn"
echo "date:                $deb_date"
echo "deb package name:    $deb_package_name"
echo "deb packager:        $deb_packager"
echo "packager email:      $deb_packager_email"
echo "version:             $deb_version_string"
echo "app categories:      $desktop_file_categories"
echo "desktop icon:        $desktop_file_icon"
echo "app main executable: $desktop_file_main_exe"
echo "origin bottle name:  $origin_bottle_name"
echo "public bottle name:  $public_bottle_name"
echo "old package name:    $old_package_name"
echo "package depends:     $package_depends"
echo "mime type:           $mime_type"
echo "activex name:        $activex_name"
echo "bottle path:         $BottlePath"
echo "make autostart:      $make_autostart"
echo "send to desktop:     $send_to_desktop"
echo "exec file path:      $EXEC_PATH"
echo "run shell path:      $start_shell"
echo "run wine cmd:        $wine_name"

curdir=`pwd`
stgdir="$curdir/staging.dir"
dstdir="$curdir/final.dir"
outdir="$dstdir/opt/apps/$deb_package_name"
outentries="$outdir/entries"
outfiles="$outdir/files"
run_sh_dir="/opt/apps/$deb_package_name/files"
uos_package_save="$curdir/package_save/uos"

export DEB_HOST_ARCH=i386
PKG_FILE="${deb_package_name}_${deb_version_string}_i386.deb"

CheckPathExists "$curdir/debian"            "debian package building scripts lost."
CheckPathExists "$curdir/template"          "package template scripts lost."
echo "=====>Preparing packaging environment..."
if [ -d "$stgdir" ]; then rm -rf "$stgdir"; fi
mkdir -p "$stgdir"
if [ -d "$dstdir" ]; then rm -rf "$dstdir"; fi
mkdir -p "$dstdir"
mkdir -p "$outentries"
mkdir -p "$outfiles"
if [ ! -d "$uos_package_save" ]; then mkdir -p "$uos_package_save"; fi

echo "<=====done."

if [ -n "$1" ] && [ -f "/opt/apps/$deb_package_name/files/files.7z" ]; then
    echo "Use last bottle file"
    cp /opt/apps/$deb_package_name/files/files.7z "$outfiles/"
else
    CheckPathExists "$BottlePath" "Original bottle $BottlePath do NOT exist."

    echo "=====>Clean bottle..."
    ./cleanbottle.sh $BottlePath
    echo "<=====done."
 
    echo "=====>Creating program files archive..."
    cp -r $BottlePath/* "$stgdir"
    # Dir links in profile should been recreated when deploy.
    find "$stgdir/drive_c/users/$USER" -type l -exec rm "{}" \;
    # Remove packager personal information. We will expand user name when deploy.
    sed -i "s#$USER#@current_user@#" $stgdir/*.reg
    mv "$stgdir/drive_c/users/$USER" "$stgdir/drive_c/users/@current_user@"
    # Merge additional files for this package.
    if [ -d "$curdir/specified/$deb_package_name/bottle" ]; then
        cp -ruv $curdir/specified/$deb_package_name/bottle/* $stgdir
    else
        cp -ruv $curdir/specified/temp/bottle/* $stgdir
    fi

    if [ -f "$curdir/specified/$deb_package_name/root/opt/apps/$deb_package_name/files/extensions.so" ]; then
        if [ ! -f "$stgdir/winx" ]; then
            mkdir -p "$stgdir/winx"
        fi
        ln -s /opt/apps/$deb_package_name/files/extensions.so "$stgdir/winx/extensions.so"
        ls -l "$stgdir/winx/extensions.so"
    fi

    7z a -snh -snl -t7z -mx=9 -ms=on -mmt=on -m0=BCJ2 -m1=LZMA2:d=64m:fb=273 "$outfiles/files.7z" "$stgdir/*"
fi

md5sum "$outfiles/files.7z" | awk '{print $1}' > "$outfiles/files.md5sum"

echo "<=====done."
echo "=====>Creating additional files..."
cd "$outdir"
if [ -d "$dstdir/debian" ]; then
    rm -rf "$dstdir/debian"
fi
cp -r "$curdir/debian/" "$dstdir"
TranslateTemplateFileUos "$dstdir/debian/"
if [ -d "$curdir/specified/$deb_package_name/root/" ]; then
    echo "copy root files.."
    cp -ruv $curdir/specified/$deb_package_name/root/* "$dstdir"
    if [ -d "$dstdir/usr/" ]; then
        echo "$dstdir/usr/* /usr" &>> "$dstdir/debian/install"
    fi
fi
cp "$curdir/template/run.sh" "$outfiles"
TranslateTemplateFileUos "$outfiles/run.sh"
cp "$curdir/template/info" "$outdir"
TranslateTemplateFileUos "$outdir/info"

#if no desktop_file_categories, don't create desktop
if [ -n "$desktop_file_categories" ]; then
    mkdir -p "$outentries/applications"
    mkdir -p "$dstdir/usr/share/applications"
    cp "$curdir/template/target.desktop" "$outentries/applications/$deb_package_name.desktop"
    cp "$curdir/template/target.desktop" "$dstdir/usr/share/applications/$deb_package_name.desktop"
    TranslateTemplateFileUos "$outentries/applications/$deb_package_name.desktop"

    # TODO: We should generate icons from main program automatically.
    cd "$curdir/icons"
    find -iname "$desktop_file_icon" -exec dirname "{}" \; | xargs -I "{}" mkdir -p "$outentries/icons/{}"
    find -iname "$desktop_file_icon" -exec cp "{}" "$outentries/icons/{}" \;

fi
# 写入 postrm 自动删除卸载残留脚本
$dstdir/DEBIAN/postrm
systemVersion=`cat /etc/os-version`
systemVersion=${systemVersion,,}  # 获取系统版本
# 判断系统是否为 UOS
if [[ "uos" == *"$systemVersion"* ]]; then
    # 如果系统是 UOS，使用默认的打包方式
    cd "$dstdir"
    echo "$outdir/* /opt/apps/$deb_package_name" &>> "debian/install"
    echo "<=====done."

    echo "=====>Creating deb package..."
    fakeroot "debian/build" "$dstdir"
    echo "<=====done."

    echo "=====> Removing temporary files..."
    mv "$dstdir/$PKG_FILE" "$uos_package_save"
 
    #rm -rf "$stgdir"
    #rm -rf "$dstdir"
    echo "<=====done."
    echo -e "\n\nDeb file generated: $PKG_FILE\n"
    echo "+++++ all done. +++++"
    
    exit 0
fi
# 非 UOS 操作系统，使用修改后的 dpkg-deb -b 打包方式
# 参考 @虚幻的早晨 在 https://bbs.deepin.org/post/240570 和 https://wwd.lanzouy.com/ipwOt082k9qb 的建议和代码进行修改
# 这里有个小坑坑，记录一下，如果想要使用 dpkg-deb -b 打包，需要修改 debian/control，修改为如下内容才能正常被 dpkg-deb 打包（删除空行和添加 Version）：
# Source: @deb_package_name@
# Section: non-free/otherosfs
# Priority: optional
# Maintainer: @deb_packager@
# Build-Depends: debhelper (>= 3.0), fakeroot
# Standards-Version: 3.7.3.0
# Package: @deb_package_name@
# Depends: @package_depends@
# Recommends: libcapi20-3, libcups2, libdbus-1-3, libfontconfig1, libfreetype6, libglu1-mesa | libglu1, libgnutls30 | libgnutls28 | libgnutls26, libgsm1, libgssapi-krb5-2, libjpeg62-turbo | libjpeg8, libkrb5-3, libodbc1, libosmesa6, libpng16-16 | libpng12-0, libsane | libsane1, libsdl2-2.0-0, libtiff5, libv4l-0, libxcomposite1, libxcursor1, libxfixes3, libxi6, libxinerama1, libxrandr2, libxrender1, libxslt1.1, libxxf86vm1
# Replaces: @old_package@
# Provides: @old_package@
# Conflicts: @old_package@
# Architecture: @Arch@
# Multi-Arch: foreign
# Description:  @app_description@
# Version:@deb_version_string@

cd "$dstdir"
echo "<=====done."
echo "=====>Creating deb package..."
mv debian DEBIAN
dpkg-deb -Z xz -z 0 -b  ./ ../package_save/uos
echo "<=====done."
exit 0
