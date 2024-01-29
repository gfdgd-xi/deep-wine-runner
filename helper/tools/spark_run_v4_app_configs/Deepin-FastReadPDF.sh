    #set -- "$1" "${2#file://*}"
    local path=$(urldecode "$2")
    path=${path/file:\/\//}
    set -- "$1" "$path"
	if [ "$path" ];then 
    CallProcess "$@"
	else
	CallProcess "$1"
	fi
