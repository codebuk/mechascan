# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './qt-mechascan/mainwindow.ui'
#
# Created: Fri Feb 20 23:56:23 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(741, 754)
        MainWindow.setStyleSheet("font: 9pt \"Cantarell\";\n"
"QGroupBox {\n"
"    border: 2px solid gray;\n"
"    border-radius: 5px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; /* position at the top center */\n"
"    padding: 0 3px;\n"
"    \n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 741, 23))
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
        self.dock_control = QtWidgets.QDockWidget(MainWindow)
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
        self.dock_control.setFloating(False)
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
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_control.addItem(spacerItem)
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
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_control.addItem(spacerItem1)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_control)
        self.dock_control.setWidget(self.dockWidgetContents_control)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dock_control)
        self.dock_hardware = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_hardware.sizePolicy().hasHeightForWidth())
        self.dock_hardware.setSizePolicy(sizePolicy)
        self.dock_hardware.setMinimumSize(QtCore.QSize(170, 600))
        self.dock_hardware.setMaximumSize(QtCore.QSize(170, 524287))
        self.dock_hardware.setFloating(False)
        self.dock_hardware.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dock_hardware.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.RightDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dock_hardware.setObjectName("dock_hardware")
        self.dock_hardware_2 = QtWidgets.QWidget()
        self.dock_hardware_2.setObjectName("dock_hardware_2")
        self.layoutWidget = QtWidgets.QWidget(self.dock_hardware_2)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 186, 525))
        self.layoutWidget.setObjectName("layoutWidget")
        self.vl_hardware = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.vl_hardware.setSpacing(0)
        self.vl_hardware.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.vl_hardware.setContentsMargins(6, -1, -1, -1)
        self.vl_hardware.setObjectName("vl_hardware")
        self.widget = QtWidgets.QWidget(self.layoutWidget)
        self.widget.setMinimumSize(QtCore.QSize(0, 90))
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setStyleSheet("QGroupBox {\n"
"    border: 2px solid gray;\n"
"    border-radius: 5px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; /* position at the top center */\n"
"    padding: 0 3px;\n"
"    \n"
"}\n"
"")
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 2, 0, 1, 1)
        self.check_tpt = QtWidgets.QCheckBox(self.groupBox)
        self.check_tpt.setChecked(True)
        self.check_tpt.setTristate(False)
        self.check_tpt.setObjectName("check_tpt")
        self.gridLayout_4.addWidget(self.check_tpt, 0, 0, 1, 2)
        self.pushButton_tpt_reset = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_tpt_reset.setObjectName("pushButton_tpt_reset")
        self.gridLayout_4.addWidget(self.pushButton_tpt_reset, 6, 0, 1, 2)
        self.pushButton_tpt_home = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_tpt_home.setObjectName("pushButton_tpt_home")
        self.gridLayout_4.addWidget(self.pushButton_tpt_home, 5, 0, 1, 2)
        self.sb_current_slot = QtWidgets.QSpinBox(self.groupBox)
        self.sb_current_slot.setWrapping(True)
        self.sb_current_slot.setAccelerated(True)
        self.sb_current_slot.setKeyboardTracking(False)
        self.sb_current_slot.setMaximum(140)
        self.sb_current_slot.setProperty("value", 1)
        self.sb_current_slot.setObjectName("sb_current_slot")
        self.gridLayout_4.addWidget(self.sb_current_slot, 2, 1, 1, 1)
        self.cb_auto_home = QtWidgets.QCheckBox(self.groupBox)
        self.cb_auto_home.setStyleSheet("font: 9pt \"Cqlineargradient(spread:pad, x1:0, y1:0, x2:1, y")
        self.cb_auto_home.setChecked(True)
        self.cb_auto_home.setTristate(False)
        self.cb_auto_home.setObjectName("cb_auto_home")
        self.gridLayout_4.addWidget(self.cb_auto_home, 1, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox, 8, 0, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setStyleSheet("QGroupBox {\n"
"    border: 2px solid gray;\n"
"    border-radius: 5px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; /* position at the top center */\n"
"    padding: 0 3px;\n"
"    \n"
"}\n"
"")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 2, 0, 1, 1)
        self.sb_settle_delay = QtWidgets.QSpinBox(self.groupBox_2)
        self.sb_settle_delay.setWrapping(True)
        self.sb_settle_delay.setAccelerated(True)
        self.sb_settle_delay.setMaximum(1000)
        self.sb_settle_delay.setProperty("value", 200)
        self.sb_settle_delay.setObjectName("sb_settle_delay")
        self.gridLayout_5.addWidget(self.sb_settle_delay, 2, 1, 1, 1)
        self.check_cam = QtWidgets.QCheckBox(self.groupBox_2)
        self.check_cam.setChecked(True)
        self.check_cam.setTristate(False)
        self.check_cam.setObjectName("check_cam")
        self.gridLayout_5.addWidget(self.check_cam, 1, 0, 1, 2)
        self.pushButton_capture = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_capture.setObjectName("pushButton_capture")
        self.gridLayout_5.addWidget(self.pushButton_capture, 3, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox_2, 9, 0, 1, 2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_3.setStyleSheet("QGroupBox {\n"
"    border: 2px solid gray;\n"
"    border-radius: 5px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; /* position at the top center */\n"
"    padding: 0 3px;\n"
"    \n"
"}\n"
"")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_6.addWidget(self.label_4, 2, 0, 1, 1)
        self.sb_intensity = QtWidgets.QSpinBox(self.groupBox_3)
        self.sb_intensity.setWrapping(True)
        self.sb_intensity.setAccelerated(True)
        self.sb_intensity.setMaximum(100)
        self.sb_intensity.setProperty("value", 100)
        self.sb_intensity.setObjectName("sb_intensity")
        self.gridLayout_6.addWidget(self.sb_intensity, 2, 1, 1, 1)
        self.pushButton_lamp = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_lamp.setCheckable(True)
        self.pushButton_lamp.setChecked(False)
        self.pushButton_lamp.setObjectName("pushButton_lamp")
        self.gridLayout_6.addWidget(self.pushButton_lamp, 4, 0, 1, 2)
        self.check_led = QtWidgets.QCheckBox(self.groupBox_3)
        self.check_led.setChecked(True)
        self.check_led.setTristate(False)
        self.check_led.setObjectName("check_led")
        self.gridLayout_6.addWidget(self.check_led, 0, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox_3, 10, 0, 1, 2)
        self.groupBox_4 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_4.setStyleSheet("QGroupBox {\n"
"    border: 2px solid gray;\n"
"    border-radius: 5px;\n"
"    margin-top: 1ex; /* leave space at the top for the title */\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center; /* position at the top center */\n"
"    padding: 0 3px;\n"
"    \n"
"}\n"
"")
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.sb_start_slot = QtWidgets.QSpinBox(self.groupBox_4)
        self.sb_start_slot.setWrapping(True)
        self.sb_start_slot.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.sb_start_slot.setAccelerated(True)
        self.sb_start_slot.setMinimum(1)
        self.sb_start_slot.setProperty("value", 1)
        self.sb_start_slot.setObjectName("sb_start_slot")
        self.gridLayout.addWidget(self.sb_start_slot, 0, 1, 1, 1)
        self.sb_end_slot = QtWidgets.QSpinBox(self.groupBox_4)
        self.sb_end_slot.setWrapping(True)
        self.sb_end_slot.setAccelerated(True)
        self.sb_end_slot.setMinimum(1)
        self.sb_end_slot.setMaximum(140)
        self.sb_end_slot.setProperty("value", 140)
        self.sb_end_slot.setObjectName("sb_end_slot")
        self.gridLayout.addWidget(self.sb_end_slot, 1, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_4, 3, 0, 1, 2)
        self.vl_hardware.addWidget(self.widget)
        self.dock_hardware.setWidget(self.dock_hardware_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dock_hardware)
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
        self.menuMechascan.setTitle(_translate("MainWindow", "&File"))
        self.menuView.setTitle(_translate("MainWindow", "&View"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit"))
        self.tb_prev.setText(_translate("MainWindow", "..."))
        self.tb_play.setText(_translate("MainWindow", "..."))
        self.tb_next.setText(_translate("MainWindow", "..."))
        self.tb_next.setShortcut(_translate("MainWindow", "N"))
        self.groupBox.setTitle(_translate("MainWindow", "Transport"))
        self.label_5.setText(_translate("MainWindow", "Goto Slot"))
        self.check_tpt.setText(_translate("MainWindow", "UEnable Transport"))
        self.pushButton_tpt_reset.setText(_translate("MainWindow", "Reset"))
        self.pushButton_tpt_home.setText(_translate("MainWindow", "Home"))
        self.cb_auto_home.setText(_translate("MainWindow", "Return to home"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Camera"))
        self.label_3.setText(_translate("MainWindow", "Delay( ms)"))
        self.check_cam.setText(_translate("MainWindow", "Use Camera "))
        self.pushButton_capture.setText(_translate("MainWindow", "&Capture"))
        self.pushButton_capture.setShortcut(_translate("MainWindow", "Shift+C"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Lamp"))
        self.label_4.setText(_translate("MainWindow", "Intensity"))
        self.pushButton_lamp.setText(_translate("MainWindow", "Lamp"))
        self.check_led.setText(_translate("MainWindow", "Use Lamp"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Scan range"))
        self.label_2.setText(_translate("MainWindow", "End"))
        self.label.setText(_translate("MainWindow", "Start"))
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

