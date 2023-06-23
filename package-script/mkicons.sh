#!/bin/bash

tmp="mktemp"
Bottle_dir="$HOME/.deepinwine"
icon_dir="icons/hicolor"

#public_bottle_name="Deepin-WeChat"
#deb_package_name="deepin.com.wechat"
#exec_path="c:\\Program Files\\Tencent\\WeChat\\WeChat.exe"

make_png()
{
    icon_size=$(ls $icon_dir)
    icon_res=$(./icotool -l $tmp)

    echo "make png"
    echo "icon src list:"
    echo "$icon_res"

    for size in $icon_size;do
        echo ""
        size_reg="width=$(echo $size | awk -Fx '{print $1}')"
        echo "make icon for: $size_reg"
        size_reg=$(./icotool -l $tmp | grep "$size_reg")

        if [ -n "$size_reg" ];then
            icon_path="$icon_dir/$size/apps/${deb_package_name}.png"
            ./icotool -x $size_reg $tmp -o "$icon_path"
            ls -l "$icon_path"
        else
            echo "not fond size: $size"
        fi
    done
}

make_svg()
{
    echo "make svg"

    icon_res=$(./icotool -l $tmp)

    echo "icon src list:"
    echo "$icon_res"

    for size in 256 128 64 48 32 16;do
        size_reg="width=$size"
        echo "make icon for: $size_reg"
        size_reg=$(./icotool -l $tmp | grep "$size_reg" | tail -1)
        echo "cmd: $size_reg"

        if [ -n "$size_reg" ];then
            rm tmp.png
            ./icotool -x $size_reg $tmp -o tmp.png
            if [ -f tmp.png ]; then
                inkscape -z --without-gui -f tmp.png -l "$icon_dir/48x48/apps/${deb_package_name}.svg"
                file "$icon_dir/48x48/apps/${deb_package_name}.svg"
                return
            fi
        else
            echo "not fond size: $size"
        fi
    done

}

make_icon()
{
    PE_file=$(echo "$exec_path" | sed -e 's/\\/\//g')
    PE_file="$Bottle_dir/$public_bottle_name/$(echo "${PE_file/c:/drive_c}")"
    echo "Get icon form: $PE_file"

    if ./wrestool "$PE_file" -x -t14 > $tmp && [ -s $tmp ]; then
        if command -v inkscape > /dev/null 2>&1; then
            make_svg
        else
            make_png
        fi
    else
	cp deepin-wine-runner.svg "$tmp"
	if command -v inkscape > /dev/null 2>&1; then
	    make_svg
	else
	    make_png
	fi
        echo "wrestool failed"
    fi
    rm $tmp
}

if [ -z "$exec_path" ] || [ -z "$deb_package_name" ] || [ -z "$public_bottle_name" ];then
    echo "mkicon args is invaild"
    exit 0
fi

if [ -f "$icon_dir/48x48/apps/${deb_package_name}.svg" ];then
    echo "don't need make icons"
    exit 0
fi
make_icon
