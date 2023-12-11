#!/bin/bash
zipPath=$1
tempPath=/tmp/wine-runner-$RANDOM
if [[ $1 == "--help" ]]; then
    echo ©2020~`date +%Y` gfdgd xi
    echo
    echo '  --help' Show help
    echo '  --no-clean' "Don't clean temp file after running"
    exit
fi
echo                                                                     
echo 'm     m   "                         mmmmm                                    '
echo '#  #  # mmm    m mm    mmm          #   "# m   m  m mm   m mm    mmm    m mm '
echo '" #"# #   #    #"  #  #"  #         #mmmm" #   #  #"  #  #"  #  #"  #   #"  "'
echo ' ## ##"   #    #   #  #""""         #   "m #   #  #   #  #   #  #""""   #    '
echo ' #   #  mm#mm  #   #  "#mm"         #    " "mm"#  #   #  #   #  "#mm"   #    '
echo                                                                             
echo                                                                             
echo                                                                             
echo 'mmmmm                         m""      #             #                  " '
echo '#    # m   m          mmmm  mm#mm   mmm#   mmmm   mmm#         m   m  mmm '
echo '#mmmm" "m m"         #" "#    #    #" "#  #" "#  #" "#          #m#     # '
echo '#    #  #m#          #   #    #    #   #  #   #  #   #          m#m     # '   
echo '#mmmm"  "#           "#m"#    #    "#m##  "#m"#  "#m##         m" "m  mm#mm'
echo '        m"            m  #                 m  #                       '
echo '       ""              ""                   ""                       '
echo
echo ©2020~`date +%Y` gfdgd xi
echo
echo Temp Path: $tempPath
mkdir -pv $tempPath
7z x -o$tempPath
bash $tempPath/run.sh
if [[ $1 != "--no-clean" ]]; then
    rm -rfv $tempPath
fi