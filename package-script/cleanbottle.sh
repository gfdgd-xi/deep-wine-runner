#!/bin/sh

WINE_CMD="deepin-wine5"
userdir=$USER

remove_file()
{
    echo "============remove [$1]"
    rm -rfv "$1"
}

purge_dir()
{
    echo "=============clean [$1]"
    if [ -e "$1" ]; then
        find "$1" -mindepth 1 -ignore_readdir_race -exec rm -rfv {} \;
    else
        mkdir -p "$1"
    fi
}

clean_gecko()
{
    geckoid=$($WINE_CMD $BottleBase/windows/system32/uninstaller.exe --list | grep Gecko | cut -d"|" -f1)
    echo " gecko GUID: ${geckoid}"
    if [ -n "${geckoid}" ]; then
        echo "uninstall gecko..."
        $WINE_CMD $BottleBase/windows/system32/uninstaller.exe --remove ${geckoid}
    fi
    if [ -e "$BottleBase/windows/system32/gecko" ]; then
        for i in $(ls "$BottleBase/windows/system32/gecko/" | grep -v plugin); do
            echo "=============remove gecko dir [$i]"
            rm -rfv "$BottleBase/windows/system32/gecko/$i"
        done
    fi
}

clean_common_temp()
{
    remove_file "$BottleBase/../winetricks.log"
    purge_dir   "$BottleBase/windows/ControlPanelDB"
    remove_file "$BottleBase/windows/control-panel.db"
    purge_dir   "$BottleBase/windows/temp"
    purge_dir   "$BottleBase/windows/Installer"
    purge_dir   "$BottleBase/users/$userdir/Temp"
    purge_dir   "$BottleBase/users/$userdir/Cookies"
    purge_dir   "$BottleBase/users/$userdir/Recent"
    remove_file "$BottleBase/users/$userdir/Application Data/pcmaster"
    purge_dir   "$BottleBase/users/$userdir/Application Data/wine_gecko"
    purge_dir   "$BottleBase/users/$userdir/Local Settings/History"
    purge_dir   "$BottleBase/users/$userdir/Local Settings/Temporary Internet Files"
    #remove_file "$BottleBase/users/${USER}"
    purge_dir   "$BottleBase/users/Public/Temp"
    remove_file "$BottleBase/../PACKAGE_VERSION"
    remove_file "$BottleBase/../update.policy"
    purge_dir   "$BottleBase/deepin"
}

cleanup_aliwangwang()
{
    if [ ! -e "$BottleBase/Program Files/AliWangWang/AliIM.exe" ]; then return; fi

    echo "++++AliWangWang detected. cleaning..."
    purge_dir   "$BottleBase/Program Files/AliWangWang/profiles"
    purge_dir   "$BottleBase/Program Files/AliWangWang/new"
    purge_dir   "$BottleBase/users/$userdir/Local Settings/Application Data/aef"
    purge_dir   "$BottleBase/users/$userdir/Application Data/AliWangWang"
    purge_dir   "$BottleBase/users/$userdir/Application Data/TaobaoProtect"
    purge_dir   "$BottleBase/users/$userdir/Application Data/wwbizsrv"
}

cleanup_aliworkbench()
{
    if [ ! -e "$BottleBase/Program Files/AliWorkbench/AliWorkbench.exe" ]; then return; fi

    echo "++++AliWorkbench detected. cleaning..."
    purge_dir "$BottleBase/users/Public/Documents/AliWorkbench"
    purge_dir   "$BottleBase/users/$userdir/Local Settings/Application Data/aef/"
    purge_dir   "$BottleBase/users/$userdir/Local Settings/Application Data/AliWorkbench/"
    purge_dir   "$BottleBase/users/$userdir/Application Data/AliWorkbench/"
}

cleanup_flash()
{
    if [ ! -e "$BottleBase/windows/system32/Macromed/Flash/" ]; then return; fi

    echo "++++flash detected. cleaning..."
    remove_file "$BottleBase/users/$userdir/Application Data/Adobe"
    remove_file "$BottleBase/users/$userdir/Application Data/Macromedia"
    remove_file "$BottleBase/windows/system32/FlashPlayerApp.exe"
    remove_file "$BottleBase/windows/ControlPanelDB/FlashPlayerCPLApp.ico"
    remove_file "$BottleBase/windows/system32/FlashPlayerCPLApp.cpl"
    remove_file "$BottleBase/windows/system32/Macromed/Flash/FlashInstall.log"
    #remove_file "$BottleBase/windows/system32/Macromed/Flash/Flash*.dll"
    #remove_file "$BottleBase/windows/system32/Macromed/Flash/Flash*.exe"
}

cleanup_foobar2000()
{
    if [ ! -e "$BottleBase/Program Files/foobar2000/foobar2000.exe" ]; then return; fi

    echo "++++foobar2000 detected. cleaning..."
    purge_dir   "$BottleBase/Program Files/foobar2000/configuration"
    purge_dir   "$BottleBase/Program Files/foobar2000/library"
    purge_dir   "$BottleBase/Program Files/foobar2000/playlists-v1.3"
    remove_file "$BottleBase/Program Files/foobar2000/theme.fth"
}

cleanup_mailmaster()
{
    if [ ! -e "$BottleBase/Program Files/Netease/MailMaster/MailMaster.exe" ]; then return; fi

    echo "++++MailMaster detected. cleaning..."
    remove_file "$BottleBase/Program Files/Netease/MailMaster/account"
    remove_file "$BottleBase/Program Files/Netease/MailMaster/address"
    remove_file "$BottleBase/Program Files/Netease/MailMaster/tmp"
    remove_file "$BottleBase/Program Files/Netease/MailMaster/UpdateTemp"
    remove_file "$BottleBase/Program Files/Netease/MailMaster/applog.txt"
    remove_file "$BottleBase/Program Files/Netease/MailMaster/netlog.txt"
    remove_file "$BottleBase/Program Files/Netease/MailMaster/global.cfg"
    remove_file "$BottleBase/Program Files/Netease/MailMaster/schd.sdb"
}

cleanup_nativeie()
{
    if [ ! -e "$BottleBase/Program Files/Internet Explorer/iexplore.exe.mui" ]; then return; fi

    echo "++++native IE detected. cleaning..."
    purge_dir   "$BottleBase/users/$userdir/Local Settings/Application Data/Microsoft/"

    remove_file "$BottleBase/windows/ie8"
    remove_file "$BottleBase/windows/%DownloadedProgramFiles%"

    #remove all useless gecko files
    remove_file "$BottleBase/windows/system32/gecko"
}

cleanup_qq_before()
{
    if [ ! -e "$BottleBase/Program Files/Tencent/QQ/Bin/QQ.exe" ]; then return; fi

    echo "++++QQ detected. cleaning..."
    if [ -f "$BottleBase/Program Files/Tencent/Qzone/QQPhotoDrawUpdateSvr.exe" ]; then
        remove_file "$BottleBase/Program Files/Tencent/Qzone"
    fi
    if [ -f "$BottleBase/Program Files/Tencent/QQGameMicro/QQGameMicro.exe" ]; then
        remove_file "$BottleBase/Program Files/Tencent/QQGameMicro"
    fi
}

cleanup_qq()
{
    if [ ! -e "$BottleBase/Program Files/Tencent/QQ/Bin/QQ.exe" ]; then return; fi

    echo "++++cleaning QQ remains..."
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent"
    purge_dir   "$BottleBase/users/$userdir/Local Settings/Application Data/Tencent"
    purge_dir   "$BottleBase/users/Public/Application Data/Tencent/QQPCMgr"
    purge_dir   "$BottleBase/users/Public/Application Data/Tencent/QQProtect"
    purge_dir   "$BottleBase/users/Public/Application Data/Tencent/QQDownload"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/Npchrome"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/QQDownload"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/QQMiniDL"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/TXFTN"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/TXPTOP"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/TXSSO"
    purge_dir   "$BottleBase/Program Files/Tencent/QQGameMicro"
    purge_dir   "$BottleBase/Program Files/Tencent/QQMusic"
    remove_file "$BottleBase/Program Files/Tencent/QQ/Plugin/Com.Tencent.QQPet/bin/QQPet"
    remove_file "$BottleBase/Program Files/Tencent/QQ/Users"
}

cleanup_tim()
{
    if [ ! -e "$BottleBase/Program Files/Tencent/TIM/Bin/TIM.exe" ]; then return; fi

    echo "++++cleaning TIM remains..."
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent"
    purge_dir   "$BottleBase/users/$userdir/Local Settings/Application Data/Tencent"
    purge_dir   "$BottleBase/users/Public/Application Data/Tencent/QQPCMgr"
    purge_dir   "$BottleBase/users/Public/Application Data/Tencent/QQProtect"
    purge_dir   "$BottleBase/users/Public/Application Data/Tencent/QQDownload"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/Npchrome"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/QQDownload"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/QQMiniDL"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/TXFTN"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/TXPTOP"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/TXSSO"
    purge_dir   "$BottleBase/Program Files/Tencent/QQGameMicro"
    purge_dir   "$BottleBase/Program Files/Tencent/QQMusic"
    purge_dir   "$BottleBase/Program Files/Tencent/SSPlus"
    remove_file "$BottleBase/Program Files/Tencent/TIM/Users"
}

cleanup_wxwork()
{
    if [ ! -e "$BottleBase/Program Files/WXWork/WXWork.exe" ]; then return; fi

    echo "++++cleaning WXWork remains..."
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent"
}

cleanup_wechat()
{
    if [ ! -e "$BottleBase/Program Files/Tencent/WeChat/WeChat.exe" ]; then return; fi

    echo "++++cleaning WeChat remains..."
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent"
}

cleanup_baidupan()
{
    if [ ! -e "$BottleBase/Program Files/baidu/BaiduNetdisk/baidunetdisk.exe" ]; then return; fi

    echo "++++cleaning baidu net disk remains..."
    purge_dir   "$BottleBase/users/$userdir/Application Data/BaiduYunGuanjia"
    purge_dir   "$BottleBase/users/$userdir/Application Data/BaiduYunKernel"
    purge_dir   "$BottleBase/BaiduNetdiskDownload"
    purge_dir   "$BottleBase/Program Files/baidu/Download"
    remove_file "$BottleBase/Program Files/baidu/BaiduNetdisk/users"
}

cleanup_foxmail()
{
    if [ ! -e "$BottleBase/Program Files/Foxmail 7.2/Foxmail.exe" ]; then return; fi

    echo "++++cleaning Foxmail remains..."
    purge_dir   "$BottleBase/users/$userdir/Application Data/HBuilder"
    remove_file "$BottleBase/Program Files/Foxmail 7.2/Storage"
    remove_file "$BottleBase/Program Files/Foxmail 7.2/FMStorage.list"
}

cleanup_hbuilder()
{
    if [ ! -e "$BottleBase/Program Files/HBuilder/HBuilder.exe" ]; then return; fi

    echo "++++cleaning HBuilder remains..."
    purge_dir   "$BottleBase/users/$userdir/Application Data/HBuilder"
    purge_dir   "$BottleBase/users/$userdir/HBuilder"
    purge_dir   "$BottleBase/users/$userdir/HBuilder settings"
    $WINE_CMD reg DELETE "HKCU\\Software\\HBuilder" /f
}

cleanup_thunderspeed()
{
    if [ ! -e "$BottleBase/Program Files/Thunder Network/Thunder/Program/Thunder.exe" ]; then return; fi

    echo "++++cleaning ThunderSpeed remains..."
    purge_dir   "$BottleBase/users/$userdir/AppData/LocalLow/Thunder Network"
    purge_dir   "$BottleBase/users/Public/Application Data/Thunder Network"
    purge_dir   "$BottleBase/users/Public/Thunder Network"
    purge_dir   "$BottleBase/Program Files/Thunder Network/Thunder/Data/ThunderPush"
    purge_dir   "$BottleBase/Program Files/Thunder Network/Thunder/Data/SmallHornCtrlCenter"
    purge_dir   "$BottleBase/Program Files/Thunder Network/Thunder/XLApp"
}

cleanup_qqdownload()
{
    if [ ! -e "$BottleBase/Program Files/Tencent/QQDownload/QQDownload.exe" ]; then return; fi

    echo "++++QQDownload detected. cleaning..."
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent/TXSSO/SetupLogs"
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent/Logs"
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent/QQDownload"
    #mkdir -p    "$BottleBase/users/$userdir/Application Data/Tencent/QQDownload/115248456/Setting"
}

cleanup_qqcrm()
{
    if [ ! -e "$BottleBase/Program Files/Tencent/BizQQ/Bin/QQCRM.exe" ]; then return; fi

    echo "++++QQCRM detected. cleaning..."
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent/Logs"
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent/QQCRM/STemp"
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent/TXSSO"
}

cleanup_qqeim()
{
    if [ ! -e "$BottleBase/Program Files/Tencent/QQEIM/Bin/QQEIM.exe" ]; then return; fi

    echo "++++QQEIM detected. cleaning..."
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent/Logs"
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent/QQEIM/STemp"
    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent/TXSSO"
}

cleanup_richez()
{
    if [ ! -e "$BottleBase/GTJA/RichEZ/TdxW.exe" ]; then return; fi

    echo "++++Richez detected. cleaning..."
    remove_file "$BottleBase/GTJA/RichEZ/JBPlugins/pyerr"
    remove_file "$BottleBase/GTJA/RichEZ/RichET/bin/flyingfish.log"
    purge_dir   "$BottleBase/GTJA/RichEZ/RichET/fflog"
    purge_dir   "$BottleBase/GTJA/RichEZ/RichET/tmp"
    remove_file "$BottleBase/GTJA/RichEZ/T0002/customcfg_gtjazd.zip"
    remove_file "$BottleBase/GTJA/RichEZ/T0002/hq_cache"
    purge_dir   "$BottleBase/GTJA/RichEZ/T0002/tmp"
    remove_file "$BottleBase/GTJA/RichEZ/T0002/xml_cache"
    remove_file "$BottleBase/GTJA/RichEZ/webs/web_cache"
}

software_cleaner_before()
{
    cleanup_qq_before
}

cleanup_qqlite()
{
    if [ ! -e "$BottleBase/Program Files/Tencent/QQLite/Bin/QQ.exe" ]; then return; fi

    echo "++++cleaning QQ Lite remains..."

    purge_dir   "$BottleBase/users/$userdir/Application Data/Tencent"
    purge_dir   "$BottleBase/users/$userdir/Local Settings/Application Data/Tencent"
    purge_dir   "$BottleBase/users/Public/Application Data/Tencent"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/Npchrome"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/QQDownload"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/QQMiniDL"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/TXFTN"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/TXPTOP"
    remove_file "$BottleBase/Program Files/Common Files/Tencent/TXSSO"
    remove_file "$BottleBase/Program Files/Tencent/QQLite/Users"
}

cleanup_youku()
{
    if [ ! -e "$BottleBase/Program Files/YouKu/YoukuClient/YoukuDesktop.exe" ]; then return; fi

    echo "++++cleaning YouKu remains..."
    purge_dir "$BottleBase/Program Files/YouKu/YoukuClient/repaire"
    purge_dir "$BottleBase/users/$userdir/Application Data/youku"
    purge_dir "$BottleBase/users/$userdir/Application Data/ytmediacenter"
}

software_cleaner()
{
    cleanup_aliwangwang
    cleanup_aliworkbench
    #cleanup_flash
    cleanup_foobar2000
    cleanup_mailmaster
    cleanup_nativeie
    cleanup_qq
    cleanup_tim
    cleanup_qqdownload
    cleanup_qqeim
    cleanup_qqcrm
    cleanup_richez
    cleanup_qqlite
    cleanup_youku
    cleanup_foxmail
    cleanup_thunderspeed
    cleanup_wechat
    cleanup_wxwork
    cleanup_baidupan
    cleanup_hbuilder
}

#=============================================

if [ -z "$1" ]; then
    echo "prefix should be given"
    exit 1
fi

BottlePath=$1
BottleBase=${BottlePath}/drive_c

if [ ! -d "${BottlePath}" ]; then
    echo "prefix do not exists"
    exit 2
fi

#if [ ! -e "${BottlePath}/.update-timestamp" ]; then
#    echo "invalid prefix"
#    exit 3
#fi

echo "clean $BottlePath"
export WINEPREFIX=${BottlePath}
/usr/lib/i386-linux-gnu/deepin-wine5/wineserver -k

software_cleaner_before
clean_gecko
software_cleaner
clean_common_temp

exit 0
