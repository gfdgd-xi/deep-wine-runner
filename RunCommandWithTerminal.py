#!/usr/bin/env python3
import sys
from Model import *
if len(sys.argv) < 2:
    print("请加入需要的命令")
    sys.exit(1)
o = ""
for i in sys.argv[1:]:
    o += f"'{i}' "
OpenTerminal(o)