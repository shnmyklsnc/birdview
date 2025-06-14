# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/birdview.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(425, 200)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icons/mainlogo_sm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.mainStackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.mainStackedWidget.setAutoFillBackground(False)
        self.mainStackedWidget.setObjectName("mainStackedWidget")
        self.navigationPage = QtWidgets.QWidget()
        self.navigationPage.setObjectName("navigationPage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.navigationPage)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cameraConnectionWidget = ClickableWidget(self.navigationPage)
        self.cameraConnectionWidget.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.cameraConnectionWidget.setMouseTracking(False)
        self.cameraConnectionWidget.setObjectName("cameraConnectionWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.cameraConnectionWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.cameraConnectionIcon = QtWidgets.QLabel(self.cameraConnectionWidget)
        self.cameraConnectionIcon.setText("")
        self.cameraConnectionIcon.setPixmap(QtGui.QPixmap(":/icon/icons/video-camera-alt.png"))
        self.cameraConnectionIcon.setScaledContents(True)
        self.cameraConnectionIcon.setIndent(0)
        self.cameraConnectionIcon.setObjectName("cameraConnectionIcon")
        self.verticalLayout.addWidget(self.cameraConnectionIcon)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.cameraStatusLabel = QtWidgets.QLabel(self.cameraConnectionWidget)
        self.cameraStatusLabel.setObjectName("cameraStatusLabel")
        self.horizontalLayout.addWidget(self.cameraStatusLabel)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout_2.addWidget(self.cameraConnectionWidget, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 0, 1, 1, 1)
        self.liveMonitoringWidget = ClickableWidget(self.navigationPage)
        self.liveMonitoringWidget.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.liveMonitoringWidget.setObjectName("liveMonitoringWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.liveMonitoringWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.liveMonitoringIcon = QtWidgets.QLabel(self.liveMonitoringWidget)
        self.liveMonitoringIcon.setText("")
        self.liveMonitoringIcon.setPixmap(QtGui.QPixmap(":/icon/icons/eye.png"))
        self.liveMonitoringIcon.setScaledContents(True)
        self.liveMonitoringIcon.setIndent(0)
        self.liveMonitoringIcon.setObjectName("liveMonitoringIcon")
        self.verticalLayout_3.addWidget(self.liveMonitoringIcon)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem6)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        spacerItem7 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.liveMonitoringLabel = QtWidgets.QLabel(self.liveMonitoringWidget)
        self.liveMonitoringLabel.setObjectName("liveMonitoringLabel")
        self.horizontalLayout_3.addWidget(self.liveMonitoringLabel)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.gridLayout_2.addWidget(self.liveMonitoringWidget, 0, 2, 1, 1)
        self.floorPlanSetupWidget = ClickableWidget(self.navigationPage)
        self.floorPlanSetupWidget.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.floorPlanSetupWidget.setObjectName("floorPlanSetupWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.floorPlanSetupWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem9)
        self.floorPlanSetupIcon = QtWidgets.QLabel(self.floorPlanSetupWidget)
        self.floorPlanSetupIcon.setText("")
        self.floorPlanSetupIcon.setPixmap(QtGui.QPixmap(":/icon/icons/map.png"))
        self.floorPlanSetupIcon.setScaledContents(True)
        self.floorPlanSetupIcon.setIndent(0)
        self.floorPlanSetupIcon.setObjectName("floorPlanSetupIcon")
        self.verticalLayout_2.addWidget(self.floorPlanSetupIcon)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem10)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem11 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem11)
        self.floorPlanSetupLabel = QtWidgets.QLabel(self.floorPlanSetupWidget)
        self.floorPlanSetupLabel.setObjectName("floorPlanSetupLabel")
        self.horizontalLayout_2.addWidget(self.floorPlanSetupLabel)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem12)
        self.gridLayout_2.addWidget(self.floorPlanSetupWidget, 1, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem13, 1, 1, 1, 1)
        self.selectModelWidget = ClickableWidget(self.navigationPage)
        self.selectModelWidget.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.selectModelWidget.setObjectName("selectModelWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.selectModelWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem14)
        self.selectModelIcon = QtWidgets.QLabel(self.selectModelWidget)
        self.selectModelIcon.setText("")
        self.selectModelIcon.setPixmap(QtGui.QPixmap(":/icon/icons/head-side-thinking.png"))
        self.selectModelIcon.setScaledContents(True)
        self.selectModelIcon.setIndent(0)
        self.selectModelIcon.setObjectName("selectModelIcon")
        self.verticalLayout_4.addWidget(self.selectModelIcon)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem15)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        spacerItem16 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem16)
        self.selectModelLabel = QtWidgets.QLabel(self.selectModelWidget)
        self.selectModelLabel.setObjectName("selectModelLabel")
        self.horizontalLayout_4.addWidget(self.selectModelLabel)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem17)
        self.gridLayout_2.addWidget(self.selectModelWidget, 1, 2, 1, 1)
        self.mainStackedWidget.addWidget(self.navigationPage)
        self.cameraStatusPage = QtWidgets.QWidget()
        self.cameraStatusPage.setObjectName("cameraStatusPage")
        self.line = QtWidgets.QFrame(self.cameraStatusPage)
        self.line.setGeometry(QtCore.QRect(20, 40, 391, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget = QtWidgets.QWidget(self.cameraStatusPage)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 60, 391, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.currentCameraLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.currentCameraLabel.setFont(font)
        self.currentCameraLabel.setObjectName("currentCameraLabel")
        self.horizontalLayout_6.addWidget(self.currentCameraLabel)
        spacerItem18 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem18)
        self.currentCameraValue = QtWidgets.QLabel(self.layoutWidget)
        self.currentCameraValue.setMinimumSize(QtCore.QSize(200, 0))
        self.currentCameraValue.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.currentCameraValue.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.currentCameraValue.setText("")
        self.currentCameraValue.setObjectName("currentCameraValue")
        self.horizontalLayout_6.addWidget(self.currentCameraValue)
        self.layoutWidget1 = QtWidgets.QWidget(self.cameraStatusPage)
        self.layoutWidget1.setGeometry(QtCore.QRect(290, 120, 119, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.testCameraBtn = QtWidgets.QPushButton(self.layoutWidget1)
        self.testCameraBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.testCameraBtn.setObjectName("testCameraBtn")
        self.verticalLayout_5.addWidget(self.testCameraBtn)
        spacerItem19 = QtWidgets.QSpacerItem(0, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_5.addItem(spacerItem19)
        self.cameraSetupSaveChangesBtn = QtWidgets.QPushButton(self.layoutWidget1)
        self.cameraSetupSaveChangesBtn.setEnabled(False)
        self.cameraSetupSaveChangesBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.cameraSetupSaveChangesBtn.setObjectName("cameraSetupSaveChangesBtn")
        self.verticalLayout_5.addWidget(self.cameraSetupSaveChangesBtn)
        self.layoutWidget2 = QtWidgets.QWidget(self.cameraStatusPage)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 120, 201, 71))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.cameraSelectionCombobox = QtWidgets.QComboBox(self.layoutWidget2)
        self.cameraSelectionCombobox.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.cameraSelectionCombobox.setEditable(False)
        self.cameraSelectionCombobox.setObjectName("cameraSelectionCombobox")
        self.cameraSelectionCombobox.addItem("")
        self.gridLayout_3.addWidget(self.cameraSelectionCombobox, 0, 0, 2, 2)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem20, 0, 2, 2, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.RSTPBtn = QtWidgets.QPushButton(self.layoutWidget2)
        self.RSTPBtn.setEnabled(False)
        self.RSTPBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.RSTPBtn.setObjectName("RSTPBtn")
        self.horizontalLayout_5.addWidget(self.RSTPBtn)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem21)
        self.useRSTPCheckbox = QtWidgets.QCheckBox(self.layoutWidget2)
        self.useRSTPCheckbox.setObjectName("useRSTPCheckbox")
        self.horizontalLayout_5.addWidget(self.useRSTPCheckbox)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 2, 0, 1, 3)
        self.layoutWidget3 = QtWidgets.QWidget(self.cameraStatusPage)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 10, 201, 30))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.cameraStatusPageBackBtn = QtWidgets.QPushButton(self.layoutWidget3)
        self.cameraStatusPageBackBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.cameraStatusPageBackBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/icons/direction.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.cameraStatusPageBackBtn.setIcon(icon1)
        self.cameraStatusPageBackBtn.setCheckable(False)
        self.cameraStatusPageBackBtn.setAutoExclusive(True)
        self.cameraStatusPageBackBtn.setFlat(True)
        self.cameraStatusPageBackBtn.setObjectName("cameraStatusPageBackBtn")
        self.horizontalLayout_7.addWidget(self.cameraStatusPageBackBtn)
        spacerItem22 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem22)
        self.cameraStatusPageLabel = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.cameraStatusPageLabel.setFont(font)
        self.cameraStatusPageLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.cameraStatusPageLabel.setObjectName("cameraStatusPageLabel")
        self.horizontalLayout_7.addWidget(self.cameraStatusPageLabel)
        self.mainStackedWidget.addWidget(self.cameraStatusPage)
        self.floorPlanSetupPage = QtWidgets.QWidget()
        self.floorPlanSetupPage.setObjectName("floorPlanSetupPage")
        self.gridLayout = QtWidgets.QGridLayout(self.floorPlanSetupPage)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.floorPlanSetupPageBackBtn = QtWidgets.QPushButton(self.floorPlanSetupPage)
        self.floorPlanSetupPageBackBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.floorPlanSetupPageBackBtn.setText("")
        self.floorPlanSetupPageBackBtn.setIcon(icon1)
        self.floorPlanSetupPageBackBtn.setCheckable(False)
        self.floorPlanSetupPageBackBtn.setAutoExclusive(True)
        self.floorPlanSetupPageBackBtn.setFlat(True)
        self.floorPlanSetupPageBackBtn.setObjectName("floorPlanSetupPageBackBtn")
        self.horizontalLayout_8.addWidget(self.floorPlanSetupPageBackBtn)
        spacerItem23 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem23)
        self.floorPlanSetupPageLabel = QtWidgets.QLabel(self.floorPlanSetupPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.floorPlanSetupPageLabel.sizePolicy().hasHeightForWidth())
        self.floorPlanSetupPageLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.floorPlanSetupPageLabel.setFont(font)
        self.floorPlanSetupPageLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.floorPlanSetupPageLabel.setObjectName("floorPlanSetupPageLabel")
        self.horizontalLayout_8.addWidget(self.floorPlanSetupPageLabel)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_8)
        spacerItem24 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem24)
        self.gridLayout.addLayout(self.horizontalLayout_10, 0, 0, 1, 1)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.floorPlanImageBox = QtWidgets.QLabel(self.floorPlanSetupPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.floorPlanImageBox.sizePolicy().hasHeightForWidth())
        self.floorPlanImageBox.setSizePolicy(sizePolicy)
        self.floorPlanImageBox.setMinimumSize(QtCore.QSize(0, 0))
        self.floorPlanImageBox.setBaseSize(QtCore.QSize(0, 0))
        self.floorPlanImageBox.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.floorPlanImageBox.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.floorPlanImageBox.setText("")
        self.floorPlanImageBox.setObjectName("floorPlanImageBox")
        self.verticalLayout_7.addWidget(self.floorPlanImageBox)
        spacerItem25 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem25)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.floorPlanSetupSaveChangesBtn = QtWidgets.QPushButton(self.floorPlanSetupPage)
        self.floorPlanSetupSaveChangesBtn.setEnabled(False)
        self.floorPlanSetupSaveChangesBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.floorPlanSetupSaveChangesBtn.setObjectName("floorPlanSetupSaveChangesBtn")
        self.horizontalLayout_9.addWidget(self.floorPlanSetupSaveChangesBtn)
        spacerItem26 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem26)
        self.previewFloorPlanImageBtn = QtWidgets.QPushButton(self.floorPlanSetupPage)
        self.previewFloorPlanImageBtn.setEnabled(False)
        self.previewFloorPlanImageBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.previewFloorPlanImageBtn.setObjectName("previewFloorPlanImageBtn")
        self.horizontalLayout_9.addWidget(self.previewFloorPlanImageBtn)
        spacerItem27 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem27)
        self.uploadFloorPlanImageBtn = QtWidgets.QPushButton(self.floorPlanSetupPage)
        self.uploadFloorPlanImageBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.uploadFloorPlanImageBtn.setObjectName("uploadFloorPlanImageBtn")
        self.horizontalLayout_9.addWidget(self.uploadFloorPlanImageBtn)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.gridLayout.addLayout(self.verticalLayout_7, 2, 0, 1, 1)
        spacerItem28 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout.addItem(spacerItem28, 1, 0, 1, 1)
        self.mainStackedWidget.addWidget(self.floorPlanSetupPage)
        self.aiModelPage = QtWidgets.QWidget()
        self.aiModelPage.setObjectName("aiModelPage")
        self.layoutWidget_2 = QtWidgets.QWidget(self.aiModelPage)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 10, 238, 30))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.aiModelPageBackBtn = QtWidgets.QPushButton(self.layoutWidget_2)
        self.aiModelPageBackBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.aiModelPageBackBtn.setText("")
        self.aiModelPageBackBtn.setIcon(icon1)
        self.aiModelPageBackBtn.setCheckable(False)
        self.aiModelPageBackBtn.setAutoExclusive(True)
        self.aiModelPageBackBtn.setFlat(True)
        self.aiModelPageBackBtn.setObjectName("aiModelPageBackBtn")
        self.horizontalLayout_11.addWidget(self.aiModelPageBackBtn)
        spacerItem29 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem29)
        self.aiModelPageLabel = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.aiModelPageLabel.setFont(font)
        self.aiModelPageLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.aiModelPageLabel.setObjectName("aiModelPageLabel")
        self.horizontalLayout_11.addWidget(self.aiModelPageLabel)
        self.selectedAIModelValue = QtWidgets.QLabel(self.aiModelPage)
        self.selectedAIModelValue.setGeometry(QtCore.QRect(10, 90, 401, 31))
        self.selectedAIModelValue.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.selectedAIModelValue.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.selectedAIModelValue.setText("")
        self.selectedAIModelValue.setObjectName("selectedAIModelValue")
        self.selectedAIModelLabel = QtWidgets.QLabel(self.aiModelPage)
        self.selectedAIModelLabel.setGeometry(QtCore.QRect(10, 60, 141, 19))
        self.selectedAIModelLabel.setObjectName("selectedAIModelLabel")
        self.line_2 = QtWidgets.QFrame(self.aiModelPage)
        self.line_2.setGeometry(QtCore.QRect(10, 40, 401, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.aiModelChooseBtn = QtWidgets.QPushButton(self.aiModelPage)
        self.aiModelChooseBtn.setGeometry(QtCore.QRect(320, 130, 88, 27))
        self.aiModelChooseBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.aiModelChooseBtn.setObjectName("aiModelChooseBtn")
        self.aiModelSaveChangesBtn = QtWidgets.QPushButton(self.aiModelPage)
        self.aiModelSaveChangesBtn.setEnabled(False)
        self.aiModelSaveChangesBtn.setGeometry(QtCore.QRect(10, 130, 121, 27))
        self.aiModelSaveChangesBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.aiModelSaveChangesBtn.setObjectName("aiModelSaveChangesBtn")
        self.mainStackedWidget.addWidget(self.aiModelPage)
        self.monitoringPage = QtWidgets.QWidget()
        self.monitoringPage.setObjectName("monitoringPage")
        self.layoutWidget_3 = QtWidgets.QWidget(self.monitoringPage)
        self.layoutWidget_3.setGeometry(QtCore.QRect(10, 10, 181, 30))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.monitoringPageBackBtn = QtWidgets.QPushButton(self.layoutWidget_3)
        self.monitoringPageBackBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.monitoringPageBackBtn.setText("")
        self.monitoringPageBackBtn.setIcon(icon1)
        self.monitoringPageBackBtn.setCheckable(False)
        self.monitoringPageBackBtn.setAutoExclusive(True)
        self.monitoringPageBackBtn.setFlat(True)
        self.monitoringPageBackBtn.setObjectName("monitoringPageBackBtn")
        self.horizontalLayout_12.addWidget(self.monitoringPageBackBtn)
        spacerItem30 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem30)
        self.monitoringPageLabel = QtWidgets.QLabel(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.monitoringPageLabel.setFont(font)
        self.monitoringPageLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.monitoringPageLabel.setObjectName("monitoringPageLabel")
        self.horizontalLayout_12.addWidget(self.monitoringPageLabel)
        self.monitoringCameraStatusLabel = QtWidgets.QLabel(self.monitoringPage)
        self.monitoringCameraStatusLabel.setGeometry(QtCore.QRect(10, 70, 121, 19))
        self.monitoringCameraStatusLabel.setObjectName("monitoringCameraStatusLabel")
        self.monitoringCameraStatusValue = QtWidgets.QLabel(self.monitoringPage)
        self.monitoringCameraStatusValue.setGeometry(QtCore.QRect(10, 100, 271, 31))
        self.monitoringCameraStatusValue.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.monitoringCameraStatusValue.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.monitoringCameraStatusValue.setText("")
        self.monitoringCameraStatusValue.setObjectName("monitoringCameraStatusValue")
        self.line_3 = QtWidgets.QFrame(self.monitoringPage)
        self.line_3.setGeometry(QtCore.QRect(10, 40, 571, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.monitoringFloorPlanStatusLabel = QtWidgets.QLabel(self.monitoringPage)
        self.monitoringFloorPlanStatusLabel.setGeometry(QtCore.QRect(300, 70, 131, 19))
        self.monitoringFloorPlanStatusLabel.setObjectName("monitoringFloorPlanStatusLabel")
        self.monitoringFloorPlanStatusValue = QtWidgets.QLabel(self.monitoringPage)
        self.monitoringFloorPlanStatusValue.setGeometry(QtCore.QRect(300, 100, 281, 31))
        self.monitoringFloorPlanStatusValue.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.monitoringFloorPlanStatusValue.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.monitoringFloorPlanStatusValue.setText("")
        self.monitoringFloorPlanStatusValue.setObjectName("monitoringFloorPlanStatusValue")
        self.worldPointsBtn = QtWidgets.QPushButton(self.monitoringPage)
        self.worldPointsBtn.setGeometry(QtCore.QRect(300, 150, 131, 27))
        self.worldPointsBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.worldPointsBtn.setObjectName("worldPointsBtn")
        self.cameraPointsBtn = QtWidgets.QPushButton(self.monitoringPage)
        self.cameraPointsBtn.setGeometry(QtCore.QRect(10, 150, 151, 27))
        self.cameraPointsBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.cameraPointsBtn.setObjectName("cameraPointsBtn")
        self.cameraPointsValue = QtWidgets.QLabel(self.monitoringPage)
        self.cameraPointsValue.setGeometry(QtCore.QRect(10, 190, 281, 19))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        self.cameraPointsValue.setFont(font)
        self.cameraPointsValue.setObjectName("cameraPointsValue")
        self.worldPointsValue = QtWidgets.QLabel(self.monitoringPage)
        self.worldPointsValue.setGeometry(QtCore.QRect(300, 190, 281, 19))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(8)
        self.worldPointsValue.setFont(font)
        self.worldPointsValue.setObjectName("worldPointsValue")
        self.startMonitoringBtn = QtWidgets.QPushButton(self.monitoringPage)
        self.startMonitoringBtn.setGeometry(QtCore.QRect(220, 230, 151, 27))
        self.startMonitoringBtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.startMonitoringBtn.setObjectName("startMonitoringBtn")
        self.mainStackedWidget.addWidget(self.monitoringPage)
        self.verticalLayout_6.addWidget(self.mainStackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.mainStackedWidget.setCurrentIndex(4)
        self.cameraSelectionCombobox.setCurrentIndex(0)
        self.useRSTPCheckbox.clicked['bool'].connect(self.RSTPBtn.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Birdview"))
        self.cameraStatusLabel.setText(_translate("MainWindow", "Camera Setup"))
        self.liveMonitoringLabel.setText(_translate("MainWindow", "Monitoring"))
        self.floorPlanSetupLabel.setText(_translate("MainWindow", "Floor Plan Setup"))
        self.selectModelLabel.setText(_translate("MainWindow", "AI Model"))
        self.currentCameraLabel.setText(_translate("MainWindow", "Current Camera:"))
        self.testCameraBtn.setText(_translate("MainWindow", "Test Camera"))
        self.cameraSetupSaveChangesBtn.setText(_translate("MainWindow", "Save Changes"))
        self.cameraSelectionCombobox.setCurrentText(_translate("MainWindow", "Select Camera"))
        self.cameraSelectionCombobox.setPlaceholderText(_translate("MainWindow", "Select Camera"))
        self.cameraSelectionCombobox.setItemText(0, _translate("MainWindow", "Select Camera"))
        self.RSTPBtn.setText(_translate("MainWindow", "RTSP"))
        self.useRSTPCheckbox.setText(_translate("MainWindow", "Use RTSP?"))
        self.cameraStatusPageLabel.setText(_translate("MainWindow", "Camera Setup"))
        self.floorPlanSetupPageLabel.setText(_translate("MainWindow", "Floor Plan Setup"))
        self.floorPlanSetupSaveChangesBtn.setText(_translate("MainWindow", "Save Changes"))
        self.previewFloorPlanImageBtn.setText(_translate("MainWindow", "Preview"))
        self.uploadFloorPlanImageBtn.setText(_translate("MainWindow", "Upload"))
        self.aiModelPageLabel.setText(_translate("MainWindow", "AI Model Selection"))
        self.selectedAIModelLabel.setText(_translate("MainWindow", "Selected AI Model"))
        self.aiModelChooseBtn.setText(_translate("MainWindow", "Choose"))
        self.aiModelSaveChangesBtn.setText(_translate("MainWindow", "Save Changes"))
        self.monitoringPageLabel.setText(_translate("MainWindow", "Monitoring"))
        self.monitoringCameraStatusLabel.setText(_translate("MainWindow", "Camera Status"))
        self.monitoringFloorPlanStatusLabel.setText(_translate("MainWindow", "Floor Plan Status"))
        self.worldPointsBtn.setText(_translate("MainWindow", "Set World Points"))
        self.cameraPointsBtn.setText(_translate("MainWindow", "Set Camera Points"))
        self.cameraPointsValue.setText(_translate("MainWindow", "[(1000, 1000), (1000, 1000), (1000, 1000), (1000, 1000)]"))
        self.worldPointsValue.setText(_translate("MainWindow", "[(1000, 1000), (1000, 1000), (1000, 1000), (1000, 1000)]"))
        self.startMonitoringBtn.setText(_translate("MainWindow", "Start Monitoring"))
from ui.custom_widgets import ClickableWidget
import ui.resource_rc
