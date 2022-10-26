#!/bin/bash
BASE_DIR=$1
DEBIAN_DIR="$BASE_DIR/DEBIAN"
OPT_DIR="${BASE_DIR}/opt"
declare -a dir_list
PACKAGE_IS_NULL=""
PACKAGE=""
VERSION=""
ARCH=""
DESC=""
LINE_IS_NULL=""
# 判断参数数量
if [ $# -ne 1 ];then
       echo "USAGE: $0 DIR"
       exit 1
fi
# 判断目录
if [ ! -d $1 ];then
    echo "$1 不是目录或者该目录不存在."
    exit 2
fi
function fail(){
    echo -e "$1 \t\t\t[\033[31mFAIL\033[0m]"
}
function ok(){
    echo -e "$1 \t\t\t[\033[32mOK\033[0m]"
}
function scan_dir(){
    echo "-----------------------目录检查开始-------------------------"
    # 扫描目录
    for i in `ls $BASE_DIR`;do
        dir_list[${#dir_list[*]}]=$i
    done
    # 打印目录
    dirs=""
    for i in ${dir_list[*]};do
        if [ $i == "DEBIAN" ];then
            dirs=$dirs+$i
        elif [ $i == "opt" ];then
            dirs=$dirs+$i
        else
            dirs=$dirs+$i
            echo -e "\033[31mInfo: 扫描到不合规目录$i,请检查是否必要。\033[0m"
        fi
    done
    #echo "所有目录:$dirs" | tr '+' ' '
    # 检查DEBIAN目录是否存在
    if [ ! -d $DEBIAN_DIR ];then
        fail "检查DEBIAN目录是否存在\t\t" 
        echo -e "ERROR: ${DEBIAN_DIR}目录不存在\n"
    else
        ok "检查DEBIAN目录是否存在\t\t"
    fi    
    # 检查control文件是否存在
    if [ ! -f ${DEBIAN_DIR}/control ];then
        fail "检查control文件是否存在\t\t"
        echo -e "ERROR: ${DEBIAN_DIR}/control文件不存在\n"
    else
        ok "检查control文件是否存在\t\t"
    fi
    # 检查是否有钩子脚本
    script_num=`ls ${DEBIAN_DIR}/*rm ${DEBIAN_DIR}/*inst 2>/dev/null |wc -l`
    if [ ${script_num} -gt 0 ];then
        fail "检查是否有钩子脚本\t\t"
        echo -e "Note: ${DEBIAN_DIR}/下有钩子脚本,请手动检查是否合规.\n"
    else
        ok "检查是否有钩子脚本\t\t"
    fi
    # 检查opt目录是否存在
    if [ ! -d $OPT_DIR ];then
        fail "检查opt目录是否存在\t\t"
        echo -e "ERROR: ${OPT_DIR}目录不存在\n"
    else
        ok "检查opt目录是否存在\t\t"
    fi    
    # 检查opt/apps目录是否存在
    if [ ! -d $OPT_DIR/apps ];then
        fail "检查opt/apps目录是否存在\t"
        echo -e "ERROR: ${OPT_DIR}/apps目录不存在\n"
    else
        ok "检查opt/apps目录是否存在\t"
    fi    
    # 检查PACKAGE目录名是否正确
    if [ ! -d ${OPT_DIR}/apps/${PACKAGE} ];then
        fail "检查程序目录是否存在\t\t"
        echo -e "ERROR: ${OPT_DIR}/apps/${PACKAGE}目录不存在,可能与control文件中包名不一致,终止后续检查.\n"
        exit 100
    else
        ok "检查程序目录是否存在\t\t"
    fi
    # 检查entries目录
    if [ ! -d ${OPT_DIR}/apps/${PACKAGE}/entries ];then
        fail "检查entries目录是否存在\t\t"
        echo -e "ERROR: ${OPT_DIR}/apps/${PACKAGE}/entries目录不存在\n"
    else
        ok "检查entries目录是否存在\t\t"
    fi
    # 检查applications目录
    if [ ! -d ${OPT_DIR}/apps/${PACKAGE}/entries/applications ];then
        fail "检查applications目录是否存在\t"
        echo -e "ERROR: ${OPT_DIR}/apps/${PACKAGE}/entries/applications目录不存在\n"
    else
        ok "检查applications目录是否存在\t"
    fi
    #检查desktop文件
    if [ ! -f ${OPT_DIR}/apps/${PACKAGE}/entries/applications/${PACKAGE}.desktop ];then
        fail "检查desktop文件是否存在\t\t"
        echo -e "ERROR: ${OPT_DIR}/apps/${PACKAGE}/entries/applications/${PACKAGE}.desktop文件不存在\n"
    else
        ok "检查desktop文件是否存在\t\t"
    fi
    # 检查icons目录    
    if [ ! -d ${OPT_DIR}/apps/${PACKAGE}/entries/icons ];then
        fail "检查icons目录是否存在\t\t"
        echo -e "ERROR: ${OPT_DIR}/apps/${PACKAGE}/entries/icons目录不存在\n"
    else
        ok "检查icons目录是否存在\t\t"
    fi
    # 检查hicolor目录    
    if [ ! -d ${OPT_DIR}/apps/${PACKAGE}/entries/icons/hicolor ];then
        fail "检查hicolor目录是否存在\t\t"
        echo -e "ERROR: ${OPT_DIR}/apps/${PACKAGE}/entries/icons/hicolor目录不存在\n"
    else
        ok "检查hicolor目录是否存在\t\t"
    fi
    # 检查files目录
    if [ ! -d ${OPT_DIR}/apps/${PACKAGE}/files ];then
        fail "检查files目录是否存在\t\t"
        echo -e "ERROR: ${OPT_DIR}/apps/${PACKAGE}/files目录不存在\n"
    else
        ok "检查files目录是否存在\t\t"
    fi
    #检查info文件
    if [ ! -f ${OPT_DIR}/apps/${PACKAGE}/info ];then
        fail "检查info文件是否存在\t\t"
        echo -e "ERROR: ${OPT_DIR}/apps/${PACKAGE}/info文件不存在\n"
    else
        ok "检查info文件是否存在\t\t"
    fi
    echo -e "-----------------------目录检查结束-------------------------\n"
}
function check_icon_type(){
    real_extent_name=`file $1 2>/dev/null| grep -E "SVG|JPEG|PNG" -o`
    if [ ${real_extent_name} == "SVG" ];then
        real_extent_name="svg"
    elif [ ${real_extent_name} == "PNG" ];then
        real_extent_name="png"
    elif [ ${real_extent_name} == "JPEG" ];then
        real_extent_name="jpg"
    fi
    if [ ${real_extent_name} == ${icon_type} ];then
        ok "检查Icon字段\t\t\t"
    else
        fail "检查Icon字段\t\t\t"
        echo -e "ERROR: $1文件扩展名为${icon_type},但实际文件类型为${real_extent_name},可能会影响图标显示.\n"
    fi
}
function check_control(){
    echo "-------------------control文件检查开始----------------------"
    # 包名是否为空
    PACKAGE_IS_NULL=`grep Package ${DEBIAN_DIR}/control  | awk -F ": " '{print $2}'`
    if [ -z $PACKAGE_IS_NULL ];then
        fail "检查Package字段是否为空\t\t"
        echo -e "ERROR: Package字段参数不能为空且:后必须有一个空格.\n"
    else
        ok "检查Package字段是否为空\t\t"
    fi
    # 包名是否是域名倒置
    PACKAGE=`grep Package ${DEBIAN_DIR}/control | awk -F ": " '{print $2}' |grep -E "^(com|cn|edu|org|net|gov)(\.[a-Z0-9]+)+"`
    if [ -z $PACKAGE ];then
                fail "检查Package是否域名倒置\t\t"
                echo -e "ERROR: Package字段参数必须是域名倒置.\n"
    else
                ok "检查Package是否域名倒置\t\t"
    fi
    # 版本
    VERSION=`grep Version ${DEBIAN_DIR}/control  | awk -F ": " '{print $2}'`
    if [ -z $VERSION ];then
                fail "检查Version字段\t\t\t"
                echo -e "ERROR: Version字段不能为空且:后必须有一个空格.\n"
    else
                ok "检查Version字段\t\t\t"
    fi
    # 架构
    ARCH=`grep Architecture ${DEBIAN_DIR}/control  | awk -F ": " '{print $2}'`
    if [ -z $ARCH ];then
                fail "检查Architecture字段\t\t"
                echo -e "ERROR: Architecture字段不能为空且:后必须有一个空格.\n"
    else
        if [ ${ARCH} != "amd64" -a ${ARCH} != "arm64" -a ${ARCH} != "mips64el" -a ${ARCH} != "sw_64" -a ${ARCH} != "all" -a ${ARCH} != "any" ];then
                    fail "检查Architecture字段\t\t"
                    echo -e "ERROR: Architecture字段只能{arm64|amd64|mips64el|sw_64|all|any}\n"
        else
                    ok "检查Architecture字段\t\t"
        fi
    fi
    # 描述
    DESC=`grep Description ${DEBIAN_DIR}/control  | awk -F ": " '{print $2}'`
    if [ -z "$DESC" ];then
                fail "检查Description字段\t\t"
                echo -e "ERROR: Description字段不能为空且:后必须有一个空格.\n"
    else
                ok "检查Description字段\t\t"
    fi
    # 分类
    SECTION=`grep Section ${DEBIAN_DIR}/control  | awk -F ": " '{print $2}'`
    if [ -z "$SECTION" ];then
                fail "检查Section字段\t\t\t"
                echo -e "ERROR: Section字段不能为空且:后必须有一个空格.\n"
    else
                ok "检查Section字段\t\t\t"
    fi
    # 是否有空行，1表示没有空行，0有空行
    grep ^$ ${DEBIAN_DIR}/control 1>/dev/null 2>&1
    LINE_IS_NULL=$? 
    if [ ! $LINE_IS_NULL -eq 1 ];then
                fail "检查是否有空行\t\t\t"
                echo -e "ERROE: control文件中不能有空行.\n"   
    else
                ok "检查是否有空行\t\t\t"
    fi
    echo -e "-------------------control文件检查结束----------------------\n"
}
function check_desktop_file(){
    echo -e "-------------------desktop文件检查开始----------------------"
    # 检查Icon文件是否存在
    icon_path=`grep Icon ${OPT_DIR}/apps/${PACKAGE}/entries/applications/${PACKAGE}.desktop  2>/dev/null|awk -F "=" '{print $2}'`
    icon_is_full_path=`echo ${icon_path} | cut -c 1`
    icon_type=`echo ${icon_path} |rev |cut -c 1-6 |rev | awk -F '.' '{print $2}'`
    if [ -f ${OPT_DIR}/apps/${PACKAGE}/entries/applications/${PACKAGE}.desktop ];then
        if [ ${icon_type} != "png" -a ${icon_type} != "svg" -a ${icon_type} != "jpg" ];then
            fail "检查Icon文件类型\t\t"
            echo -e "ERROR: Icon文件类型必须是jpg/png/svg,您desktop文件中可能没有扩展名。\n"
        else
            ok "检查Icon文件类型\t\t"
            if [ -z $icon_path ];then
                fail "检查Icon字段\t\t\t"
                echo -e "ERROR: Icon字段不能为空且:后面要有一个空格.\n"
            else
                if [ ${icon_is_full_path} == '/' ];then
                    if [ ! -f ${BASE_DIR}${icon_path} ];then
                        fail "检查Icon字段\t\t\t"
                        echo -e "ERROR: ${BASE_DIR}${icon_path}文件不存在.\n"
                    else
                        check_icon_type ${BASE_DIR}${icon_path}
                    fi
                else
                    image_dir="${OPT_DIR}/apps/${PACKAGE}/entries/icons/hicolor/"
                    if [ -f ${image_dir}16x16/apps/${icon_path} ];then
                        check_icon_type ${image_dir}16x16/apps/${icon_path}
                    elif [ -f ${image_dir}24x24/apps/${icon_path} ];then 
                        check_icon_type ${image_dir}24x24/apps/${icon_path}
                    elif [ -f ${image_dir}32x32/apps/${icon_path} ];then 
                        check_icon_type ${image_dir}32x32/apps/${icon_path}
                    elif [ -f ${image_dir}48x48/apps/${icon_path} ];then 
                        check_icon_type ${image_dir}48x48/apps/${icon_path}
                    elif [ -f ${image_dir}128x128/apps/${icon_path} ];then 
                        check_icon_type ${image_dir}128x128/apps/${icon_path}
                    elif [ -f ${image_dir}256x256/apps/${icon_path} ];then 
                        check_icon_type ${image_dir}256x256/apps/${icon_path}
                    elif [ -f ${image_dir}512x512/apps/${icon_path} ];then 
                        check_icon_type ${image_dir}512x512/apps/${icon_path}
                    elif [ -f ${image_dir}scalable/apps/${icon_path} ];then 
                        check_icon_type ${image_dir}scalable/apps/${icon_path}
                    else
                        fail "检查Icon字段\t\t\t"
                        echo -e "ERROR: ${OPT_DIR}/apps/${PACKAGE}/entries/icons/hicolor/{scalable|16x16|32x32|48x48...512}/apps/${icon_path}文件不存在.\n"
                    fi
                fi
            fi
        fi
        # 检查Exec启动程序是否存在
        exec_path=`grep Exec ${OPT_DIR}/apps/${PACKAGE}/entries/applications/${PACKAGE}.desktop 2>/dev/null |awk -F "=" '{print $2}' |awk '{print $1}'`    
        if [ ! -f ${BASE_DIR}${exec_path} ];then
            fail "检查Exec字段\t\t\t"
            echo -e "ERROR: ${BASE_DIR}${exec_path}文件不存在.\n"
        else
            ok "检查Exec字段\t\t\t"
        fi
    else
        fail "检查Icon文件类型\t\t"
        fail "检查Exec字段\t\t\t"
        echo -e "ERROR: ${OPT_DIR}/apps/${PACKAGE}/entries/applications/${PACKAGE}.desktop文件不存在\n"
    fi
    echo -e "-------------------desktop文件检查结束----------------------\n"
}
function check_info_file(){
    echo -e "---------------------info文件检查开始-----------------------"
    appid=`grep appid ${OPT_DIR}/apps/${PACKAGE}/info 2>/dev/null|awk -F ":" '{print $2}' |tr -d "\"" |tr -d , | tr -d ' '`
    arch_num=`grep arch ${OPT_DIR}/apps/${PACKAGE}/info 2>/dev/null |tr -d "[]" |awk -F ',' '{print (NF-1)}'`
    arch=`grep arch ${OPT_DIR}/apps/${PACKAGE}/info 2>/dev/null`
    # 检查appid字段
    if [ -z $appid ];then
        fail "检查appid字段\t\t\t"
        echo -e "ERROR: appid字段不能为空.\n"
    else
        if [ ${PACKAGE} != `echo ${appid} |tr -d "$" |tr -d "\r"` ];then
            fail "检查appid字段\t\t\t"
            echo -e "ERROR: appid字段参数与Package字段参数不一致.\n"
        else
            ok "检查appid字段\t\t\t"
        fi
    fi
    # 检查arch字段
    if [ $arch_num -eq "1" ];then
        if [ $ARCH == `echo $arch | awk -F ":" '{print $2}' | tr -d "[],\""` ];then 
            ok "检查arch字段\t\t\t"
        else
            fail "检查arch字段\t\t\t"
            echo -e "ERROR: arch字段参数与control中不一致.\n"
        fi
    elif [ $arch_num -eq "2" ];then
        fail "检查arch字段\t\t\t"
        echo -e "ERROR: arch字段参数与control中不一致.\n"
    elif [ $arch_num -eq "3" ];then
        if [ $ARCH == "any" -o $ARCH == "all" ];then
            echo $arch | grep "amd64" |grep "arm64" | grep "mips64el" -q 
            if [ $? -eq 0 ];then
                ok "检查arch字段\t\t\t"
            else
                fail "检查arch字段\t\t\t"
                echo -e "ERROR: arch字段参数与control中不一致.\n"
            fi
        else
            fail "检查arch字段\t\t\t"
            echo -e "ERROR: arch字段参数与control中不一致.\n"
        fi
    else
        fail "检查arch字段\t\t\t"
        echo -e "ERROR: arch字段参数太多或\n"
    fi
    # 检查json语法
    tail -n 2 ${OPT_DIR}/apps/${PACKAGE}/info | grep -q ","  
    if [ $? -eq 0 ];then
        fail "检查json语法\t\t\t"
        echo -e "ERROR: info文件倒数第二行有多余的,号.\n"
    else
        ok "检查json语法\t\t\t"
    fi    
    echo -e "---------------------info文件检查结束-----------------------\n"
}
check_control
scan_dir
check_desktop_file
check_info_file
