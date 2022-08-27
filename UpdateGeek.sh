echo                            
echo '   mmm                #     '
echo ' m"   "  mmm    mmm   #   m '
echo ' #   mm #"  #  #"  #  # m"  '
echo ' #    # #""""  #""""  #"#   '
echo '  "mmm" "#mm"  "#mm"  #  "m '
echo
echo
cd /tmp
echo 提示：
echo Geek Uninstaller 官网访问较慢，所以请耐心等待
aria2c -x 16 -s 16 https://geekuninstaller.com/geek.zip
unzip geek.zip
cd `dirname $0`
cp -rv /tmp/geek.exe ./
if [[ $? == 0 ]];then
	exit
fi
echo "拷贝失败，申请使用 sudo 拷贝"
sudo cp -rv /tmp/geek.exe ./