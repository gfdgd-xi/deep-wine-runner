#!/bin/bash
cd `dirname $0`
pyuic5 -o ui_mainwindow.py mainwindow.ui
pyrcc5 -o program_resources.py  program_resources.qrc