#!/bin/bash

SHELL_DIR=$(dirname $(realpath $0))

# 函数：获取所有应用列表
# 函数：获取所有应用列表
get_apps_list() {
    local apps_list=()
    local app_dirs=($(find /opt/apps -mindepth 1 -maxdepth 1 -type d -exec test -f {}/files/run.sh \; -print))
    
    if [ ${#app_dirs[@]} -eq 0 ]; then
        zenity --error --text="请至少在应用商店安装一个wine应用后启动" --width 200
        exit 1
    fi
    
    for app_dir in "${app_dirs[@]}"; do
        local package_name=$(basename "$app_dir")
        local run_script="$app_dir/files/run.sh"
        local bottle_name="无法读取"
        local version="无法读取"
        local use_spark="否"
        
        if [ -f "$run_script" ]; then
            bottle_name=$(grep -oP 'BOTTLENAME="\K[^"]+' "$run_script")
            version=$(grep -oP 'APPVER="\K[^"]+' "$run_script")
            
            if [ -z "$version" ]; then
                version="无法读取"
            fi
            # START_SHELL_PATH=XXX/spark_run_v4.sh
            if grep START_SHELL_PATH= "$run_script" | grep spark_run_v4.sh; then
                use_spark="是"
            fi
        fi
        
        local app_name=$(get_app_name "$package_name")
        
        apps_list+=("$app_name" "$package_name" "$bottle_name" "$version" "$use_spark")
    done
    
    echo "${apps_list[@]}"
}

# 函数：获取应用名称
get_app_name() {
    local app_name_orig=$(grep -m 1 '^Name=' "/usr/share/applications/$1.desktop" | cut -d '=' -f 2)
    local app_name_i18n=$(grep -m 1 "^Name\[$LANGUAGE\]\=" "/usr/share/applications/$1.desktop" | cut -d '=' -f 2)
    local app_name=""
    
    if [ -z "$app_name_i18n" ]; then
        app_name="$app_name_orig"
    else
        app_name="$app_name_i18n"
    fi
    
    echo "$app_name"
}

# 函数：选择应用
select_app() {
    local apps_list=($(get_apps_list))
    local app=$(zenity --print-column=2 --width=800 --height=600 --list --title="选择应用" --text="选择要执行的应用" --column="应用名" --column="包名" --column="容器名" --column="版本号" --column="是否使用星火wine助手" "${apps_list[@]}")
    
    if [ -n "$app" ]; then
        local app_dir="/opt/apps/$app"
        local run_script="$app_dir/files/run.sh"
        local use_spark="否"
            if if grep START_SHELL_PATH= "$run_script" | grep spark_run_v4.sh; then
                use_spark="是"
            fi
        if [ "$use_spark" == "是" ]; then
            select_spark_action "$app" "$(get_app_name $app)"
        else
            select_non_spark_action "$app" "$(get_app_name $app)"
        fi
    fi
}

select_non_spark_action(){
    local app="$1"
    local app_name="$2"
    local options=("在终端中打开" "打开容器目录" "清理并重置容器目录" "更多操作")
    local choice=$(zenity --width=800 --height=600 --list --title="选择操作" --text="选择要对$app_name执行的操作" --column="操作" "${options[@]}")
        case "$choice" in
        "在终端中打开")
            local app_dir="/opt/apps/$app"
            local run_script="$app_dir/files/run.sh"
            x-terminal-emulator -e "$run_script"
            ;;
         "打开容器目录")
    local app_dir="/opt/apps/$app"
    local run_script="$app_dir/files/run.sh"
    local bottle_name=$(grep -oP 'BOTTLENAME="\K[^"]+' "$run_script")
    xdg-open file:///home/$(whoami)/.deepinwine/${bottle_name}
         ;;
         "清理并重置容器目录")
    local app_dir="/opt/apps/$app"
    local run_script="$app_dir/files/run.sh"
    local bottle_name=$(grep -oP 'BOTTLENAME="\K[^"]+' "$run_script")
    $SHELL_DIR/../kill.sh ${bottle_name}
    rm -rf /home/$(whoami)/.deepinwine/${bottle_name}/*
    zenity --info --width=300 --text="操作已完成，请重启Wine应用查看"
    ;;
    	"更多操作")
    	if [ -e /usr/bin/deepin-wine-runner ];then
    	/usr/bin/deepin-wine-runner
    	elif [ $(command -v spark-store) ];then
    	spark-store spk://store/tools/spark-deepin-wine-runner
    	elif [ $(command -v deepin-home-appstore-client) ];then
    	xdg-open  appstore://deepin-home-appstore-client?app_detail_info/spark-deepin-wine-runner
    	else
    	xdg-open https://gitee.com/gfdgd-xi/deep-wine-runner/releases
    	fi
    	
    	;;
         esac
         
}

# 函数：选择星火wine助手操作
select_spark_action() {
    local app="$1"
    local app_name="$2"
    local options=("在终端中打开" "打开容器目录" "清理并重置容器目录" "修改应用缩放" "修改全局缩放" "更多操作")
    local choice=$(zenity --width=800 --height=600 --list --title="选择操作" --text="选择要对$app_name执行的操作" --column="操作" "${options[@]}")
    
    case "$choice" in
        "在终端中打开")
            local app_dir="/opt/apps/$app"
            local run_script="$app_dir/files/run.sh"
            x-terminal-emulator -e "$run_script"
            ;;
        "打开容器目录")
    local app_dir="/opt/apps/$app"
    local run_script="$app_dir/files/run.sh"
    local bottle_name=$(grep -oP 'BOTTLENAME="\K[^"]+' "$run_script")
    xdg-open file:///home/$(whoami)/.deepinwine/${bottle_name}
         ;;
         "清理并重置容器目录")
    local app_dir="/opt/apps/$app"
    local run_script="$app_dir/files/run.sh"
    local bottle_name=$(grep -oP 'BOTTLENAME="\K[^"]+' "$run_script")
    $SHELL_DIR/../spark_kill.sh ${bottle_name}
    rm -rf /home/$(whoami)/.deepinwine/${bottle_name}/*
    zenity --info --width=300 --text="操作已完成，请重启Wine应用查看"
    ;;
        "修改应用缩放")
            select_scale_action "应用" "$app"
            ;;
        "修改全局缩放")
            select_scale_action "全局" "$app"
            ;;
        "更多操作")
    	if [ -e /usr/bin/deepin-wine-runner ];then
    	/usr/bin/deepin-wine-runner
    	elif [ $(command -v spark-store) ];then
    	spark-store spk://store/tools/spark-deepin-wine-runner
    	elif [ $(command -v deepin-home-appstore-client) ];then
    	xdg-open  appstore://deepin-home-appstore-client?app_detail_info/spark-deepin-wine-runner
    	else
    	xdg-open https://gitee.com/gfdgd-xi/deep-wine-runner/releases
    	fi
    	;;
        *)
            ;;
    esac
}

# 函数：选择缩放操作
select_scale_action() {
    local scale_type="$1"
    local app="$2"
    local app_dir="/opt/apps/$app"
    local run_script="$app_dir/files/run.sh"
    local bottle_name=$(grep -oP 'BOTTLENAME="\K[^"]+' "$run_script")
    local scale_factors=("1.0" "1.25" "1.5" "1.75" "2.0" "2.5" "3.0" "3.5" "4.0" "恢复默认")
    local choice=$(zenity --width=800 --height=600 --list --title="选择缩放比例" --text="选择要设置的缩放比例" --column="比例" "${scale_factors[@]}")
    
    if [ -n "$choice" ]; then
        local scale_factor="$choice"
        
        if [ "$scale_type" == "应用" ]; then
		if [ "$scale_factor" == "恢复默认" ];then
		rm $HOME/.deepinwine/$bottle_name/scale.txt
		else
            $SHELL_DIR/scale-set-helper/set-wine-scale.sh -s "$scale_factor" "$HOME/.deepinwine/$bottle_name"
            	fi
        elif [ "$scale_type" == "全局" ]; then
            if [ "$scale_factor" == "恢复默认" ];then
		rm $HOME/.config/spark-wine/scale.txt
		else
            echo "$scale_factor" > "$HOME/.config/spark-wine/scale.txt"
            find "$HOME/.deepinwine/" -name "scale.txt" -type f -print -exec rm -rf {} \;
            fi
        fi
    fi
    zenity --info --width=300 --text="操作已完成，请重启Wine应用查看"
}

select_app

