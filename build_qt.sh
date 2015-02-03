#!/bin/bash
pyuic5 -x -o main_window.py ./qt-mechascan/mainwindow.ui
pyrcc5 -no-compress  ./qt-mechascan/qt_resources.qrc -o qt_resources_rc.py

