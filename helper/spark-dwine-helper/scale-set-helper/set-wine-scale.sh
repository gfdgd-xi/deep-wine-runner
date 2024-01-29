#!/bin/bash

help() {
    cat <<EOF
用法：$0 [-h|--help] [-s|--set-scale-factor] path
-h|--help               显示这个帮助
-s|--set-scale-factor   直接指定缩放。支持1.0，1.25，1.5，1.75，2.0	
path                    容器目录

                                         本脚本具有超级兔力。
--------------------------------------------------------------------
Usage: $0 [-h|--help] [-s|--set-scale-factor] path
-h|--help               Show this text
-s|--set-scale-factor   Set scale factor direcly. Support 1.0，1.25，1.5，1.75，2.0	
path                    Wine Container directory path

                                         This script have super bunny power.
EOF
}
#########################帮助文件结束#############################

parse_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
        -h|--help)
            help
            exit
            ;;
	-s|--set-scale-factor)
	appointed_scale_factor="$2"
    
	;;

	"bunny")
		cat /opt/durapps/spark-dwine-helper/scale-set-helper/bunny.txt
	exit

	;;

        *)
            CONTAINER_PATH="$1"

            ;;
    esac
    shift
    done
}
################
parse_args "$@"

#####先看看PATH对不对
if [ ! -f "$CONTAINER_PATH/user.reg" ];then
	echo "错误：找不到user.reg，退出。你应当在文件解压结束后调用此脚本。"
	echo "如果你不清楚如何使用这个脚本，请使用 $0 -h"
    echo "E: Can not find user.reg. Exit. You should use this script after the extraction"
	echo "If you don't know how to use this script, try $0 -h"
	exit 1
fi


if [ "$appointed_scale_factor" = "" ];then
#########未指定下，读取$CONTAINER_PATH/scale.txt。如果没有，优先$DEEPIN_WINE_SCALE设置，然后是手动

if [ ! -f "$CONTAINER_PATH/scale.txt" ];then
	
	echo "E: No SCALE profile found. try to use DEEPIN_WINE_SCALE"
	echo "错误：没有检测到缩放设置，读取DEEPIN_WINE_SCALE"
	if [ "$DEEPIN_WINE_SCALE" = "" ];then
		echo "E: No DEEPIN_WINE_SCALE found. Use get-scale.sh to Set "
		echo "错误：没有检测到DEEPIN_WINE_SCALE，用get-scale.sh设置"
		/opt/durapps/spark-dwine-helper/scale-set-helper/get-scale.sh "$CONTAINER_PATH"
		wine_scale=`cat $CONTAINER_PATH/scale.txt`
		echo "检测到的缩放倍数为:$wine_scale"
		echo "Scale is $wine_scale"
	else
		echo "$DEEPIN_WINE_SCALE" > $CONTAINER_PATH/scale.txt
		wine_scale=`cat $CONTAINER_PATH/scale.txt`
		echo "检测到的缩放倍数为:$wine_scale"
		echo "Scale is $wine_scale"
fi
else
wine_scale=`cat $CONTAINER_PATH/scale.txt`

echo "检测到的缩放倍数为:$wine_scale"
echo "Scale is $wine_scale"


fi
#####非deepin发行版似乎没有这个变量，暂时不清楚这个变量是哪个组件做的



else
#######指定了缩放倍数
echo "使用了--set-scale-factor，直接指定"
echo "--set-scale-factor detected. Arrange directly"


if [ "$appointed_scale_factor" != "1.0" ] && [ "$appointed_scale_factor" != "1.25" ] && [ "$appointed_scale_factor" != "1.5" ]  && [ "$appointed_scale_factor" != "1.75" ] && [ "$appointed_scale_factor" != "2.0" ] ;then
echo "无法识别的倍数：$appointed_scale_factor，请参看$0 -h"
echo "Unrecognizable number. Use $0 -h to get help"
exit 1
fi
#######没问题了再用
echo "$appointed_scale_factor" > $CONTAINER_PATH/scale.txt
wine_scale=`cat $CONTAINER_PATH/scale.txt`

fi

########开始设置
########如果环境变量里没指定了APPRUN_CMD（在run.sh中）就替换，如果有就直接用来设置

if [ "$APPRUN_CMD" = "" ];then
echo "没有检测到APPRUN_CMD环境变量，执行sed替换。如果要使用wine原生提供的方法，请在环境变量中指定(export)"
case "$wine_scale" in
       1.0*)
            reg_text="\"LogPixels\"=dword:00000060"
            ;;
        1.25*)
            reg_text="\"LogPixels\"=dword:00000078"
            ;;
        1.5*)
            reg_text="\"LogPixels\"=dword:00000090"
            ;;
        1.75*)
            reg_text="\"LogPixels\"=dword:000000A8"
            ;;
        2.0*)
            reg_text="\"LogPixels\"=dword:000000C0"
            ;;
	*)
		reg_text="\"LogPixels\"=dword:00000060"
		#可能不是Xorg
		;;
    esac

#####根据scale设置dword值


LogPixels_line=(`sed -n -e "/"LogPixels"/=" $CONTAINER_PATH/user.reg`)
#####关键词行数取得
until [ "${#LogPixels_line[@]}" = "0" ];do


line_num=${LogPixels_line[0]}

sed -i "$line_num"c\ "$reg_text" "$CONTAINER_PATH/user.reg"
LogPixels_line=(${LogPixels_line[@]:1})
done

echo "已经完成替换。位置：$CONTAINER_PATH/user.reg"
echo "在以下行数进行了替换，内容为$reg_text"
echo `sed -n -e "/"LogPixels"/=" $CONTAINER_PATH/user.reg`
echo "---------------------------------------"

else
#####用wine提供的方法

case "$wine_scale" in
       1.0*)
            dpi="96"
            ;;
        1.25*)
            dpi="120"
            ;;
        1.5*)
            dpi="144"
            ;;
        1.75*)
            dpi="168"
            ;;
        2.0*)
            dpi="192"
            ;;
	*)
		dpi="96"
		#可能不是Xorg或者是其他错误
		;;
    esac
echo "用$APPRUN_CMD执行指令"
echo "指令为"
echo "env WINEPREFIX="$CONTAINER_PATH" $APPRUN_CMD reg ADD 'HKCU\Control Panel\Desktop' /v LogPixels /t REG_DWORD /d $dpi /f"

env WINEPREFIX="$CONTAINER_PATH" $APPRUN_CMD reg ADD 'HKCU\Control Panel\Desktop' /v LogPixels /t REG_DWORD /d $dpi /f

fi
