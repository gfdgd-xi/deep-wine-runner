#!/bin/bash
CPU_CORES=$(($(grep -c processor < /proc/cpuinfo)*2))
make build-python -j$CPU_CORES
make install-to-qemu-python -j$CPU_CORES
exit 0