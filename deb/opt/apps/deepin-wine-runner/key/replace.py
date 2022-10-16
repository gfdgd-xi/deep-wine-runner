#!/usr/bin/python3
import os
import sys
file = open(sys.argv[1], "r")
things = file.read().replace(sys.argv[2], sys.argv[3])
file.close()
file = open(sys.argv[1], "w")
file.write(things)
file.close()