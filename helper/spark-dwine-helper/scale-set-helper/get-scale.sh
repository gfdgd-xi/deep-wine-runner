#/bin/bash
source /opt/durapps/transhell/transhell.sh
load_transhell_debug

#########>>>>>>>函数段
Get_Dist_Name()
{
    if grep -Eqii "Deepin" /etc/issue || grep -Eq "Deepin" /etc/*-release; then
        DISTRO='Deepin'
    elif grep -Eqi "UnionTech" /etc/issue || grep -Eq "UnionTech" /etc/*-release; then
        DISTRO='UniontechOS'
    elif grep -Eqi "UOS" /etc/issue || grep -Eq "UOS" /etc/*-release; then
        DISTRO='UniontechOS'
    else
	 DISTRO='OtherOS'
	fi
}
#########<<<<<<<

if [ $# -lt 1 ]; then
echo "无参数，无法启动。这是一个set-wine-scale的组件，一般来说，你不会需要单独启动这个脚本"
echo "请参考set-wine-scale.sh使用"
echo "参数为CONTAINER_PATH"
echo "只读取第一个，其他参数会被放弃"
fi

CONTAINER_PATH="$1"

if [ ! -f "$CONTAINER_PATH/user.reg" ];then
	echo "错误：找不到user.reg，退出。你应当在文件解压结束后调用此脚本"
    echo "E: Can not find user.reg. Exit. You should use this script after the extraction"
	exit 1
fi


mkdir -p $HOME/.config/spark-wine/
#####全局参数位置
#####能到这一步的说明已经是没有自定义参数了，直接读全局覆盖没问题
#####

if [ -f "$HOME/.config/spark-wine/scale.txt" ];then
	cat $HOME/.config/spark-wine/scale.txt > $CONTAINER_PATH/scale.txt
	echo "检测到已经设置过全局参数，直接复制"
    echo "全局参数的位置在$HOME/.config/spark-wine/scale.txt，如果需要更换请删除此文件重新生成"
	exit
fi


Get_Dist_Name
if [ "$DISTRO" = "Deepin" ] || [ "$DISTRO" = "UniontechOS" ];then
echo 1.0 > $HOME/.config/spark-wine/scale.txt
cat $HOME/.config/spark-wine/scale.txt > $CONTAINER_PATH/scale.txt
#####就是1倍缩放
exit
fi



dimensions=`xdpyinfo | grep dimensions | sed -r 's/^[^0-9]*([0-9]+x[0-9]+).*$/\1/'`
scale_factor=`zenity --list \
	--width=700 \
	--height=350 \
       --title="${TRANSHELL_CONTENT_YOUR_DIMENSION_IS} $dimensions ${TRANSHELL_CONTENT_PLEASE_CHOOSE_ONE_BELOW}" \
       --column="${TRANSHELL_CONTENT_OPTION}" \
       1.0 \
       1.25 \
	1.5 \
	1.75 \
       2.0`

case "$scale_factor" in 
	"")
	zenity --info --text="${TRANSHELL_CONTENT_1_SCALE_AS_DEFAULT}${TRANSHELL_CONTENT_YOU_CAN_USE_SPARK_WINE_HELPER_SETTINGS_TO_ADJUST}" --width=500 --height=150
	scale_factor="1.0"
	;;
	*)
zenity --info --text="${TRANSHELL_CONTENT_SCALE_IS} $scale_factor ${TRANSHELL_CONTENT_SAVED}！${TRANSHELL_CONTENT_YOU_CAN_USE_SPARK_WINE_HELPER_SETTINGS_TO_ADJUST}" --width=500 --height=150
	;;
esac
echo "$scale_factor" > $HOME/.config/spark-wine/scale.txt
cat $HOME/.config/spark-wine/scale.txt > $CONTAINER_PATH/scale.txt

