#/bin/bash

source /opt/durapps/transhell/transhell.sh
load_transhell_debug

until [ "$IS_CLOSE" = "1" ];do

CHOSEN_SETTINGS=`zenity --list \
	--width=700 \
	--height=350 \
       --title="${TRANSHELL_CONTENT_WELCOME_AND_CHOOSE_ONE_TO_RUN}" \
       --column="${TRANSHELL_CONTENT_OPTION}" \
	"${TRANSHELL_CONTENT_SET_GLOBAL_SCALE}" \
       "${TRANSHELL_CONTENT_SET_APP_SCALE}" \
	"${TRANSHELL_CONTENT_SYNC_APP_SCALE_WITH_GLOBAL}" \
	"${TRANSHELL_CONTENT_ONLY_AVAILABLE_TO_SPARK_DWINE_HELPER_APP}" `

echo "$CHOSEN_SETTINGS"
case "$CHOSEN_SETTINGS" in 
	"${TRANSHELL_CONTENT_SET_GLOBAL_SCALE}")
########
	zenity --info --text="${TRANSHELL_CONTENT_THIS_WILL_NOT_TAKE_EFFECT_IN_DEEPIN_BECAUSE_READ_ENVIRONMENT_FIRST}" --width=500 --height=150

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
	zenity --info --text="${TRANSHELL_CONTENT_1_SCALE_AS_DEFAULT}" --width=500 --height=150
	scale_factor="1.0"
	;;
	*)
zenity --info --text="${TRANSHELL_CONTENT_SCALE_IS} $scale_factor ${TRANSHELL_CONTENT_SAVED}" --width=500 --height=150
	;;
esac
echo "$scale_factor" > $HOME/.config/spark-wine/scale.txt


	;;
########




	"${TRANSHELL_CONTENT_SET_APP_SCALE}")
	zenity --info --text="${TRANSHELL_CONTENT_PLEASE_CHOOSE_WINE_BOTTLE_DIRECTORY}" --width=500 --height=150
	CONTAINER_PATH=`zenity --file-selection --filename="$HOME/.deepinwine/" --directory`
	
	if [ ! -f "$CONTAINER_PATH/user.reg" ];then
	zenity --info --text="${TRANSHELL_CONTENT_ERROR_NO_USER_REG_AS_NOT_A_WINE_BOTTLE}" --width=500 --height=150
	
	else
	
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
       2.0 \
	${TRANSHELL_CONTENT_SYNC_SCALE_WITH_GLOBAL} `

case "$scale_factor" in 
	"")
	zenity --info --text="${TRANSHELL_CONTENT_1_SCALE_AS_DEFAULT}。" --width=500 --height=150
	scale_factor="1.0"
/opt/durapps/spark-dwine-helper/scale-set-helper/set-wine-scale.sh -s $scale_factor $CONTAINER_PATH
	;;
	"${TRANSHELL_CONTENT_SYNC_SCALE_WITH_GLOBAL}")
	zenity --info --text="${TRANSHELL_CONTENT_WILL_SYNC_SCALE_WITH_GLOBAL}" --width=500 --height=150
	rm $CONTAINER_PATH/scale.txt
	;;
	*)
zenity --info --text="${TRANSHELL_CONTENT_SCALE_IS} $scale_factor ${TRANSHELL_CONTENT_SAVED}" --width=500 --height=150
/opt/durapps/spark-dwine-helper/scale-set-helper/set-wine-scale.sh -s $scale_factor $CONTAINER_PATH
	;;
esac


fi
	;;
	"${TRANSHELL_CONTENT_SYNC_APP_SCALE_WITH_GLOBAL}")
	find ${HOME}/.deepinwine/ -name "scale.txt" -type f -print -exec rm -rf {} \;
	zenity --info --text="${TRANSHELL_CONTENT_BOTTLES_BELOW_HAVE_SYNCED_SCALE_WITH_GLOBAL}：\n`cd ${HOME}/.deepinwine/ && ls`" --width=500 --height=150
	;;
	"${TRANSHELL_CONTENT_ONLY_AVAILABLE_TO_SPARK_DWINE_HELPER_APP}")
	
	;;

	*)
	IS_CLOSE="1"
	;;


esac
done
