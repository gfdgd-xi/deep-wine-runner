#/bin/bash

cd $(dirname $0)

SHELL_DIR=$(dirname $(realpath $0))
runtime_path=/opt/deepinwine/runtime-i386
echo $runtime_path
if [ -f "$runtime_path/init_runtime.sh" ];then
    source "$runtime_path/init_runtime.sh"

    init_runtime
    init_32bit_config
    echo "use deepinwine runtime"
    "$WINELDPATH" ./gl-wine32
    exit $?
fi

./gl-wine32
exit $?
