# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './qt-mechascan/mainwindow.ui'
#
# Created: Thu Feb 12 14:48:44 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(690, 625)
        MainWindow.setStyleSheet("font: 9pt \"Cantarell\";\n"
                                 "\n"
                                 "\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.dock_hardware = QtWidgets.QDockWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_hardware.sizePolicy().hasHeightForWidth())
        self.dock_hardware.setSizePolicy(sizePolicy)
        self.dock_hardware.setMinimumSize(QtCore.QSize(170, 431))
        self.dock_hardware.setMaximumSize(QtCore.QSize(170, 524287))
        self.dock_hardware.setFloating(False)
        self.dock_hardware.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dock_hardware.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dock_hardware.setObjectName("dock_hardware")
        self.dock_hardware_2 = QtWidgets.QWidget()
        self.dock_hardware_2.setObjectName("dock_hardware_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dock_hardware_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.vl_hardware = QtWidgets.QVBoxLayout()
        self.vl_hardware.setSpacing(0)
        self.vl_hardware.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.vl_hardware.setContentsMargins(6, -1, -1, -1)
        self.vl_hardware.setObjectName("vl_hardware")
        self.check_cam = QtWidgets.QCheckBox(self.dock_hardware_2)
        self.check_cam.setChecked(True)
        self.check_cam.setTristate(True)
        self.check_cam.setObjectName("check_cam")
        self.vl_hardware.addWidget(self.check_cam)
        self.check_tpt = QtWidgets.QCheckBox(self.dock_hardware_2)
        self.check_tpt.setChecked(True)
        self.check_tpt.setTristate(True)
        self.check_tpt.setObjectName("check_tpt")
        self.vl_hardware.addWidget(self.check_tpt)
        self.check_led = QtWidgets.QCheckBox(self.dock_hardware_2)
        self.check_led.setChecked(True)
        self.check_led.setTristate(True)
        self.check_led.setObjectName("check_led")
        self.vl_hardware.addWidget(self.check_led)
        self.cb_auto_home = QtWidgets.QCheckBox(self.dock_hardware_2)
        self.cb_auto_home.setStyleSheet("font: 9pt \"Cqlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))rgb(255, 255, 255)antarell\";\n"
"font: 11pt \"Carlito\";")
        self.cb_auto_home.setChecked(True)
        self.cb_auto_home.setTristate(False)
        self.cb_auto_home.setObjectName("cb_auto_home")
        self.vl_hardware.addWidget(self.cb_auto_home)
        self.widget_2 = QtWidgets.QWidget(self.dock_hardware_2)
        self.widget_2.setObjectName("widget_2")
        self.vl_hardware.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self.dock_hardware_2)
        self.widget.setMinimumSize(QtCore.QSize(0, 90))
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.sb_intensity = QtWidgets.QSpinBox(self.widget)
        self.sb_intensity.setWrapping(True)
        self.sb_intensity.setAccelerated(True)
        self.sb_intensity.setMaximum(100)
        self.sb_intensity.setProperty("value", 100)
        self.sb_intensity.setObjectName("sb_intensity")
        self.gridLayout_3.addWidget(self.sb_intensity, 4, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)
        self.sb_settle_delay = QtWidgets.QSpinBox(self.widget)
        self.sb_settle_delay.setWrapping(True)
        self.sb_settle_delay.setAccelerated(True)
        self.sb_settle_delay.setMaximum(1000)
        self.sb_settle_delay.setProperty("value", 200)
        self.sb_settle_delay.setObjectName("sb_settle_delay")
        self.gridLayout_3.addWidget(self.sb_settle_delay, 3, 1, 1, 1)
        self.sb_end_slot = QtWidgets.QSpinBox(self.widget)
        self.sb_end_slot.setWrapping(True)
        self.sb_end_slot.setAccelerated(True)
        self.sb_end_slot.setMinimum(1)
        self.sb_end_slot.setMaximum(140)
        self.sb_end_slot.setProperty("value", 140)
        self.sb_end_slot.setObjectName("sb_end_slot")
        self.gridLayout_3.addWidget(self.sb_end_slot, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.sb_start_slot = QtWidgets.QSpinBox(self.widget)
        self.sb_start_slot.setWrapping(True)
        self.sb_start_slot.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.sb_start_slot.setAccelerated(True)
        self.sb_start_slot.setMinimum(1)
        self.sb_start_slot.setProperty("value", 1)
        self.sb_start_slot.setObjectName("sb_start_slot")
        self.gridLayout_3.addWidget(self.sb_start_slot, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 5, 0, 1, 1)
        self.vl_hardware.addWidget(self.widget)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.sb_current_slot = QtWidgets.QSpinBox(self.dock_hardware_2)
        self.sb_current_slot.setWrapping(True)
        self.sb_current_slot.setAccelerated(True)
        self.sb_current_slot.setKeyboardTracking(False)
        self.sb_current_slot.setMaximum(140)
        self.sb_current_slot.setProperty("value", 1)
        self.sb_current_slot.setObjectName("sb_current_slot")
        self.gridLayout_2.addWidget(self.sb_current_slot, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.dock_hardware_2)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.vl_hardware.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addLayout(self.vl_hardware)
        self.dock_hardware.setWidget(self.dock_hardware_2)
        self.gridLayout.addWidget(self.dock_hardware, 0, 0, 1, 1)
        self.dockWidget = QtWidgets.QDockWidget(self.centralwidget)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable|QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.dockWidget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockWidget.setObjectName("dockWidget")
        self.dock_image = QtWidgets.QWidget()
        self.dock_image.setObjectName("dock_image")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dock_image)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dockWidget.setWidget(self.dock_image)
        self.gridLayout.addWidget(self.dockWidget, 0, 1, 3, 1)
        self.dock_control = QtWidgets.QDockWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_control.sizePolicy().hasHeightForWidth())
        self.dock_control.setSizePolicy(sizePolicy)
        self.dock_control.setMinimumSize(QtCore.QSize(170, 70))
        self.dock_control.setMaximumSize(QtCore.QSize(170, 70))
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.dock_control.setFont(font)
        self.dock_control.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dock_control.setWindowTitle("")
        self.dock_control.setObjectName("dock_control")
        self.dockWidgetContents_control = QtWidgets.QWidget()
        self.dockWidgetContents_control.setObjectName("dockWidgetContents_control")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.dockWidgetContents_control)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_control = QtWidgets.QHBoxLayout()
        self.horizontalLayout_control.setSpacing(0)
        self.horizontalLayout_control.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_control.setObjectName("horizontalLayout_control")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_control.addItem(spacerItem1)
        self.tb_prev = QtWidgets.QToolButton(self.dockWidgetContents_control)
        self.tb_prev.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/ic_navigate_before_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_prev.setIcon(icon)
        self.tb_prev.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.tb_prev.setObjectName("tb_prev")
        self.horizontalLayout_control.addWidget(self.tb_prev)
        self.tb_play = QtWidgets.QToolButton(self.dockWidgetContents_control)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/resources/ic_play_arrow_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icons/resources/ic_pause_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.tb_play.setIcon(icon1)
        self.tb_play.setObjectName("tb_play")
        self.horizontalLayout_control.addWidget(self.tb_play)
        self.tb_stop = QtWidgets.QToolButton(self.dockWidgetContents_control)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tb_stop.setFont(font)
        self.tb_stop.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/resources/ic_stop_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_stop.setIcon(icon2)
        self.tb_stop.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.tb_stop.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.tb_stop.setObjectName("tb_stop")
        self.horizontalLayout_control.addWidget(self.tb_stop)
        self.tb_next = QtWidgets.QToolButton(self.dockWidgetContents_control)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/resources/ic_navigate_next_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_next.setIcon(icon3)
        self.tb_next.setObjectName("tb_next")
        self.horizontalLayout_control.addWidget(self.tb_next)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_control.addItem(spacerItem2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_control)
        self.dock_control.setWidget(self.dockWidgetContents_control)
        self.gridLayout.addWidget(self.dock_control, 1, 0, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 690, 23))
        self.menubar.setObjectName("menubar")
        self.menuMechascan = QtWidgets.QMenu(self.menubar)
        self.menuMechascan.setObjectName("menuMechascan")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_Edit = QtWidgets.QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.open_act = QtWidgets.QAction(MainWindow)
        self.open_act.setObjectName("open_act")
        self.rotright_act = QtWidgets.QAction(MainWindow)
        self.rotright_act.setObjectName("rotright_act")
        self.fliph_act = QtWidgets.QAction(MainWindow)
        self.fliph_act.setObjectName("fliph_act")
        self.next_act = QtWidgets.QAction(MainWindow)
        self.next_act.setObjectName("next_act")
        self.prev_act = QtWidgets.QAction(MainWindow)
        self.prev_act.setObjectName("prev_act")
        self.rotleft_act = QtWidgets.QAction(MainWindow)
        self.rotleft_act.setObjectName("rotleft_act")
        self.flipv_act = QtWidgets.QAction(MainWindow)
        self.flipv_act.setObjectName("flipv_act")
        self.zin_act = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("edrf")
        self.zin_act.setIcon(icon)
        self.zin_act.setObjectName("zin_act")
        self.zout_act = QtWidgets.QAction(MainWindow)
        self.zout_act.setCheckable(True)
        self.zout_act.setObjectName("zout_act")
        self.open_new_act = QtWidgets.QAction(MainWindow)
        self.open_new_act.setObjectName("open_new_act")
        self.reload_act = QtWidgets.QAction(MainWindow)
        self.reload_act.setObjectName("reload_act")
        self.print_act = QtWidgets.QAction(MainWindow)
        self.print_act.setObjectName("print_act")
        self.save_act = QtWidgets.QAction(MainWindow)
        self.save_act.setObjectName("save_act")
        self.close_act = QtWidgets.QAction(MainWindow)
        self.close_act.setObjectName("close_act")
        self.exit_act = QtWidgets.QAction(MainWindow)
        self.exit_act.setObjectName("exit_act")
        self.fulls_act = QtWidgets.QAction(MainWindow)
        self.fulls_act.setCheckable(True)
        self.fulls_act.setObjectName("fulls_act")
        self.ss_act = QtWidgets.QAction(MainWindow)
        self.ss_act.setCheckable(True)
        self.ss_act.setObjectName("ss_act")
        self.ss_next_act = QtWidgets.QAction(MainWindow)
        self.ss_next_act.setCheckable(True)
        self.ss_next_act.setObjectName("ss_next_act")
        self.resize_act = QtWidgets.QAction(MainWindow)
        self.resize_act.setObjectName("resize_act")
        self.crop_act = QtWidgets.QAction(MainWindow)
        self.crop_act.setObjectName("crop_act")
        self.about_act = QtWidgets.QAction(MainWindow)
        self.about_act.setObjectName("about_act")
        self.zout = QtWidgets.QAction(MainWindow)
        self.zout.setObjectName("zout")
        self.fit_win_act = QtWidgets.QAction(MainWindow)
        self.fit_win_act.setCheckable(True)
        self.fit_win_act.setObjectName("fit_win_act")
        self.prefs_act  = QtWidgets.QAction(MainWindow)
        self.prefs_act .setObjectName("prefs_act ")
        self.props_act = QtWidgets.QAction(MainWindow)
        self.props_act.setObjectName("props_act")
        self.help_act = QtWidgets.QAction(MainWindow)
        self.help_act.setObjectName("help_act")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.actionNext = QtWidgets.QAction(MainWindow)
        self.actionNext.setObjectName("actionNext")
        self.menuMechascan.addAction(self.open_act)
        self.menuMechascan.addAction(self.open_new_act)
        self.menuMechascan.addAction(self.print_act)
        self.menuMechascan.addAction(self.save_act)
        self.menuMechascan.addAction(self.exit_act)
        self.menuView.addAction(self.next_act)
        self.menuView.addAction(self.prev_act)
        self.menuView.addAction(self.reload_act)
        self.menuView.addAction(self.zin_act)
        self.menuView.addAction(self.zout_act)
        self.menuView.addAction(self.rotright_act)
        self.menuView.addAction(self.rotleft_act)
        self.menuView.addAction(self.flipv_act)
        self.menuView.addAction(self.fliph_act)
        self.menuView.addAction(self.fulls_act)
        self.menuView.addAction(self.fit_win_act)
        self.menu_Help.addAction(self.help_act)
        self.menu_Help.addAction(self.about_act)
        self.menu_Help.addAction(self.action)
        self.menu_Edit.addAction(self.crop_act)
        self.menu_Edit.addAction(self.resize_act)
        self.menu_Edit.addAction(self.prefs_act )
        self.menu_Edit.addAction(self.props_act)
        self.menubar.addAction(self.menuMechascan.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.check_cam.setText(_translate("MainWindow", "Camera "))
        self.check_tpt.setText(_translate("MainWindow", "Use Transport"))
        self.check_led.setText(_translate("MainWindow", "Lighting"))
        self.cb_auto_home.setText(_translate("MainWindow", "Return to home"))
        self.label_4.setText(_translate("MainWindow", "Intensity"))
        self.label.setText(_translate("MainWindow", "Start"))
        self.label_3.setText(_translate("MainWindow", "Delay( ms)"))
        self.label_2.setText(_translate("MainWindow", "End"))
        self.label_5.setText(_translate("MainWindow", "Slot"))
        self.tb_prev.setText(_translate("MainWindow", "..."))
        self.tb_play.setText(_translate("MainWindow", "..."))
        self.tb_next.setText(_translate("MainWindow", "..."))
        self.tb_next.setShortcut(_translate("MainWindow", "N"))
        self.menuMechascan.setTitle(_translate("MainWindow", "&File"))
        self.menuView.setTitle(_translate("MainWindow", "&View"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.open_act.setText(_translate("MainWindow", "&Open"))
        self.open_act.setToolTip(_translate("MainWindow", "Open"))
        self.open_act.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.rotright_act.setText(_translate("MainWindow", "Rotate right"))
        self.rotright_act.setShortcut(_translate("MainWindow", "Ctrl+Right"))
        self.fliph_act.setText(_translate("MainWindow", "Flip image horizontally"))
        self.fliph_act.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.next_act.setText(_translate("MainWindow", "Next image"))
        self.next_act.setShortcut(_translate("MainWindow", "Right"))
        self.prev_act.setText(_translate("MainWindow", "Previous image"))
        self.prev_act.setShortcut(_translate("MainWindow", "Left"))
        self.rotleft_act.setText(_translate("MainWindow", "Rotate left"))
        self.rotleft_act.setShortcut(_translate("MainWindow", "Ctrl+Left"))
        self.flipv_act.setText(_translate("MainWindow", "Flip image vertically"))
        self.flipv_act.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.zin_act.setText(_translate("MainWindow", "Zoom &In"))
        self.zin_act.setShortcut(_translate("MainWindow", "Up"))
        self.zout_act.setText(_translate("MainWindow", "Zoom &Out"))
        self.zout_act.setShortcut(_translate("MainWindow", "Down"))
        self.open_new_act.setText(_translate("MainWindow", "Open new window"))
        self.open_new_act.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))
        self.reload_act.setText(_translate("MainWindow", "&Reload image"))
        self.reload_act.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.print_act.setText(_translate("MainWindow", "&Print"))
        self.print_act.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.save_act.setText(_translate("MainWindow", "&Save image"))
        self.save_act.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.close_act.setText(_translate("MainWindow", "Close window"))
        self.close_act.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.exit_act.setText(_translate("MainWindow", "E&xit"))
        self.exit_act.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.fulls_act.setText(_translate("MainWindow", "Fullscreen"))
        self.fulls_act.setShortcut(_translate("MainWindow", "F11"))
        self.ss_act.setText(_translate("MainWindow", "Slideshow"))
        self.ss_act.setShortcut(_translate("MainWindow", "F5"))
        self.ss_next_act.setText(_translate("MainWindow", "Next / Random image"))
        self.resize_act.setText(_translate("MainWindow", "Resize image"))
        self.crop_act.setText(_translate("MainWindow", "Crop image"))
        self.about_act.setText(_translate("MainWindow", "&About"))
        self.zout.setText(_translate("MainWindow", "Zoom &Out"))
        self.zout.setShortcut(_translate("MainWindow", "Down"))
        self.fit_win_act.setText(_translate("MainWindow", "Best &fit"))
        self.fit_win_act.setShortcut(_translate("MainWindow", "F"))
        self.prefs_act .setText(_translate("MainWindow", "Preferences"))
        self.props_act.setText(_translate("MainWindow", "Properties"))
        self.help_act.setText(_translate("MainWindow", "&Help"))
        self.help_act.setShortcut(_translate("MainWindow", "F1"))
        self.action.setText(_translate("MainWindow", "te"))
        self.actionNext.setText(_translate("MainWindow", "next"))

import qt_resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

