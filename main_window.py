# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './qt-mechascan/mainwindow.ui'
#
# Created: Tue Feb  3 22:54:32 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(647, 577)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.dock_hardware = QtWidgets.QDockWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_hardware.sizePolicy().hasHeightForWidth())
        self.dock_hardware.setSizePolicy(sizePolicy)
        self.dock_hardware.setMinimumSize(QtCore.QSize(152, 400))
        self.dock_hardware.setMaximumSize(QtCore.QSize(152, 524287))
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
        self.vl_hardware.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.vl_hardware.setObjectName("vl_hardware")
        self.cb_use_cam = QtWidgets.QCheckBox(self.dock_hardware_2)
        self.cb_use_cam.setChecked(True)
        self.cb_use_cam.setObjectName("cb_use_cam")
        self.vl_hardware.addWidget(self.cb_use_cam)
        self.cb_use_led = QtWidgets.QCheckBox(self.dock_hardware_2)
        self.cb_use_led.setChecked(True)
        self.cb_use_led.setObjectName("cb_use_led")
        self.vl_hardware.addWidget(self.cb_use_led)
        self.cb_autohome = QtWidgets.QCheckBox(self.dock_hardware_2)
        self.cb_autohome.setChecked(True)
        self.cb_autohome.setObjectName("cb_autohome")
        self.vl_hardware.addWidget(self.cb_autohome)
        self.cb_use_tpt = QtWidgets.QCheckBox(self.dock_hardware_2)
        self.cb_use_tpt.setChecked(True)
        self.cb_use_tpt.setObjectName("cb_use_tpt")
        self.vl_hardware.addWidget(self.cb_use_tpt)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vl_hardware.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.vl_hardware)
        self.dock_hardware.setWidget(self.dock_hardware_2)
        self.gridLayout.addWidget(self.dock_hardware, 0, 0, 1, 1)
        self.dock_control = QtWidgets.QDockWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_control.sizePolicy().hasHeightForWidth())
        self.dock_control.setSizePolicy(sizePolicy)
        self.dock_control.setMinimumSize(QtCore.QSize(170, 80))
        self.dock_control.setMaximumSize(QtCore.QSize(200, 100))
        self.dock_control.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dock_control.setObjectName("dock_control")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.dockWidgetContents_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.tb_play_3 = QtWidgets.QToolButton(self.dockWidgetContents_3)
        self.tb_play_3.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/ic_navigate_before_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_play_3.setIcon(icon)
        self.tb_play_3.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.tb_play_3.setObjectName("tb_play_3")
        self.horizontalLayout_5.addWidget(self.tb_play_3)
        self.toolButton_7 = QtWidgets.QToolButton(self.dockWidgetContents_3)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/resources/ic_play_arrow_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icons/resources/ic_pause_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.toolButton_7.setIcon(icon1)
        self.toolButton_7.setObjectName("toolButton_7")
        self.horizontalLayout_5.addWidget(self.toolButton_7)
        self.tb_stop_3 = QtWidgets.QToolButton(self.dockWidgetContents_3)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tb_stop_3.setFont(font)
        self.tb_stop_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/resources/ic_stop_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_stop_3.setIcon(icon2)
        self.tb_stop_3.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.tb_stop_3.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.tb_stop_3.setObjectName("tb_stop_3")
        self.horizontalLayout_5.addWidget(self.tb_stop_3)
        self.toolButton_8 = QtWidgets.QToolButton(self.dockWidgetContents_3)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/resources/ic_navigate_next_48px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_8.setIcon(icon3)
        self.toolButton_8.setObjectName("toolButton_8")
        self.horizontalLayout_5.addWidget(self.toolButton_8)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_5)
        self.dock_control.setWidget(self.dockWidgetContents_3)
        self.gridLayout.addWidget(self.dock_control, 1, 0, 1, 1)
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
        self.gridLayout.addWidget(self.dockWidget, 0, 1, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 647, 27))
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
        self.cb_use_cam.setText(_translate("MainWindow", "Camera "))
        self.cb_use_led.setText(_translate("MainWindow", "Lighting"))
        self.cb_autohome.setText(_translate("MainWindow", "Return to home"))
        self.cb_use_tpt.setText(_translate("MainWindow", "Use Transport"))
        self.tb_play_3.setText(_translate("MainWindow", "..."))
        self.toolButton_7.setText(_translate("MainWindow", "..."))
        self.toolButton_8.setText(_translate("MainWindow", "..."))
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

import qt_resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

