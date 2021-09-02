#! /usr/bin/env python

import os
import sys
import glob
import rospy
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from datetime import date

class RightLayout(QWidget):
    def __init__(self, parent):        
        super(RightLayout, self).__init__(parent)
        x_pos, y_pos = 405, 6
        w_pix, h_pix = 230, 440
        self.today = date.today().strftime("%d-%m-%Y")
        self.container_1 = QWidget(self)
        self.container_1.setContentsMargins(0, 0, 0, 0)
        self.container_1.setFixedSize(w_pix, h_pix)
        self.container_1.move(x_pos, y_pos)
        self.container_1.setStyleSheet("background-color:#dedddc;")
        self.container_1.showMaximized()
        self.basicSet()
        self.vbox = None
        self.awbModeVal = False


        self.container_2 = QWidget(self)
        self.container_2.setContentsMargins(0, 0, 0, 0)
        self.container_2.setFixedSize(w_pix, h_pix)
        self.container_2.move(x_pos, y_pos)
        self.container_2.setStyleSheet("background-color:#dedddc;")
        self.container_2.showMaximized()
        self.container_2.setVisible(False)
        self.motorSet() 

        self.container_3 = QWidget(self)
        self.container_3.setContentsMargins(0, 0, 0, 0)
        self.container_3.setFixedSize(w_pix, h_pix)
        self.container_3.move(x_pos, y_pos)
        self.container_3.setStyleSheet("background-color:#dedddc;")
        self.container_3.showMaximized()
        self.container_3.setVisible(False)
        self.focuserWidget()
        
    def scrollBarWidget(self,name,vMin,vMax,current):
        #label
        label = QLabel()
        label.setText(name)

        #val
        val = QLabel()
        val.setText(str(current))

        #slider
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.NoFocus)
        slider.setMinimum(vMin)
        slider.setMaximum(vMax)
        slider.setValue(current)
        slider.valueChanged[int].connect(val.setNum)


        return [label,slider,val]

    def focuserWidget(self):
        # creating a QWebEngineView
        self.browser = QWebEngineView(self.container_3)
        # setting default browser url as google
        self.browser.setUrl(QUrl("http://192.168.0.203:5000/video_feed"))
        # adding action when url get changed
        self.browser.urlChanged.connect(self.update_urlbar)
        # adding action when loading is finished
        self.browser.loadFinished.connect(self.update_title)
        # set this browser as central widget or main window
        self.setCentralWidget(self.browser)
        # creating QToolBar for navigation
        navtb = QToolBar("Navigation")
        # adding this tool bar tot he main window
        self.addToolBar(navtb)
        # similarly for home action
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
        # adding a separator in the tool bar
        navtb.addSeparator()
        # creating a line edit for the url
        self.urlbar = QLineEdit()
        # adding action when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        # adding this to the tool bar
        navtb.addWidget(self.urlbar)


    #motor settings:
    def motorSet(self):
        #Menu container
        vMotorbox = QVBoxLayout(self.container_2)
        vMotorbox.setContentsMargins(10, 10, 10, 50)
        

        #preview button
        previewButton = QPushButton('Preview')
        previewButton.setStyleSheet("background-color : #4B8BBE")
        previewButton.clicked.connect(self.onClickPreview)
        vMotorbox.addWidget(previewButton)

        #close preview button
        closePreviewButton = QPushButton('Close Preview')
        closePreviewButton.setStyleSheet("background-color : #4B8BBE")
        closePreviewButton.clicked.connect(self.onClickClosePreview)
        vMotorbox.addWidget(closePreviewButton)

        #Altitude control motor - manual slider bar
        self.altSlider = self.scrollBarWidget('Altitude Speed',0,1000,0)
        #update alt information
        self.updateAltSpeed = QPushButton('Update Alt Speed')
        self.updateAltSpeed.setStyleSheet('background-color: #4B8BBE')
        self.updateAltSpeed.clicked.connect(self.altButton)
        
        #Az control motor - manual slider bar
        self.azSlider = self.scrollBarWidget('Azimuth Speed',0,1000,0)
        self.updateAzSpeed = QPushButton('Update Az Speed')
        self.updateAzSpeed.setStyleSheet('background-color: #4B8BBE')
        self.updateAzSpeed.clicked.connect(self.azButton)
        
        self.altTopBottom = QCheckBox()
        self.altTopBottom.setStyleSheet('''
            QCheckBox::indicator:unchecked {
            image: url(icons/top.png);
            }
            QCheckBox::indicator:checked {
            image: url(icons/bottom.png);
            }
        ''')


        for i in range(0,3):
             vMotorbox.addWidget(self.altSlider[i])
        altHorizontalLayer = QHBoxLayout()
        altHorizontalLayer.addWidget(self.updateAltSpeed)
        altHorizontalLayer.addWidget(self.altTopBottom)
        
        vMotorbox.addLayout(altHorizontalLayer)
        
        
       
        for i in range(0,3):
             vMotorbox.addWidget(self.azSlider[i])

        self.azRightLeft = QCheckBox()
        self.azRightLeft.setStyleSheet('''
            QCheckBox::indicator:unchecked {
            image: url(icons/right.png);
            }
            QCheckBox::indicator:checked {
            image: url(icons/left.png);
            }
        ''')
        self.previewTracking = QPushButton('Preview Tracking')
        self.previewTracking.setStyleSheet('background-color: #4B8BBE')
        
        self.tracking = QPushButton('Tracking')
        self.tracking.setIcon(QIcon('icons/target.png'))
        self.tracking.setStyleSheet('background-color: #4B8BBE')
       
        azHorizontalLayer = QHBoxLayout()
        azHorizontalLayer.addWidget(self.updateAzSpeed)
        azHorizontalLayer.addWidget(self.azRightLeft)
        vMotorbox.addLayout(azHorizontalLayer)
        vMotorbox.addWidget(self.previewTracking)
        vMotorbox.addWidget(self.tracking)


        


    #cam settings
    def basicSet(self):
        #Menu container
        vbox = QVBoxLayout(self.container_1)
        vbox.setContentsMargins(10, 10, 10, 50)
        # vbox.addStretch(2)


        #preview button
        previewButton = QPushButton('Preview')
        previewButton.setStyleSheet("background-color : #4B8BBE")
        previewButton.clicked.connect(self.onClickPreview)
        vbox.addWidget(previewButton)

        #close preview button
        closePreviewButton = QPushButton('Close Preview')
        closePreviewButton.setStyleSheet("background-color : #4B8BBE")
        closePreviewButton.clicked.connect(self.onClickClosePreview)
        vbox.addWidget(closePreviewButton)


        #scroller : ISO value
        self.isoValGroup = self.scrollBarWidget("ISO",100,800,100)
        #Shutter speed Value
        self.shutterSpeedGroup = self.scrollBarWidget('Shutter Speed',1,1000,1)
        #Number of Images for long shot
        self.numberImageGroup = self.scrollBarWidget('Number of Images for Long Shot',1,100,1)

        #number of frame slider
        self.numberFrameGroup = self.scrollBarWidget('Number of Frames',1,24,1)
        #Analog Gain
        self.analogGainGroup = self.scrollBarWidget('Analog Gain',0,12,0)
        
        #awb (auto white balance)
        self.awbToggle = QCheckBox("awb mode")
        self.awbToggle.setStyleSheet('''
            QCheckBox::indicator:unchecked {
            image: url(icons/off.png);
            }
            QCheckBox::indicator:checked {
            image: url(icons/on.png);
            }
        ''')
        self.awbToggle.clicked.connect(self.awbMode)
        
        #awb_gain if awb mode is off only
        self.awbGainGroup = self.scrollBarWidget('awb gain',0,8,0)


        #mainTab and other 2 tabs
        self.mainTab = QTabWidget()
        self.basicPanelTab = QWidget()
        self.advanceTab = QWidget()

        #tabs name
        self.mainTab.addTab(self.basicPanelTab, 'Basic')
        self.mainTab.addTab(self.advanceTab,'Advance')

        self.basicPanelTab.layout = QVBoxLayout()
        for each in range(0,3):
            self.basicPanelTab.layout.addWidget(self.isoValGroup[each])
        for each in range(0,3):
            self.basicPanelTab.layout.addWidget(self.shutterSpeedGroup[each])
        
        for each in range(0,3):
            self.basicPanelTab.layout.addWidget(self.numberImageGroup[each])
        self.basicPanelTab.setLayout(self.basicPanelTab.layout)

        #advance tab
        self.advanceTab.layout = QVBoxLayout()
        for each in range(0,3):
            self.advanceTab.layout.addWidget(self.numberFrameGroup[each])
    
        for each in range(0,3):
            self.advanceTab.layout.addWidget(self.analogGainGroup[each]) 

        self.advanceTab.layout.addWidget(self.awbToggle)
        for each in range(0,3):
            self.advanceTab.layout.addWidget(self.awbGainGroup[each])
        
        self.advanceTab.setLayout(self.advanceTab.layout)
        
        #gallery 
        galleryButton = QPushButton()
        galleryButton.setIcon(QIcon('icons/gallery.png'))
        galleryButton.clicked.connect(self.openImage)

        #qv4l2 seetinga button
        qvDetailButton = QPushButton('qv4l2')
        qvDetailButton.setStyleSheet("QPushButton {background-color : #606060; color : white}")
        qvDetailButton.clicked.connect(self.onClickqv)

        #update all parameter
        updateParamButton = QPushButton('Update Param')
        updateParamButton.clicked.connect(self.updateAllParam)


        horizontalLayer = QHBoxLayout()
        horizontalLayer.addWidget(galleryButton)
        horizontalLayer.addWidget(qvDetailButton)
        horizontalLayer.addWidget(updateParamButton)

        #Single Shot button
        singleShotButton = QPushButton('Single Shot')
        singleShotButton.setStyleSheet("QPushButton {background-color : #4B8BBE; color : black}")
        singleShotButton.clicked.connect(self.onClickSingleShot)

        #longshot button
        longShotButton = QPushButton('Long Shot')
        longShotButton.setStyleSheet("QPushButton {background-color : #4B8BBE; color : black}")
        longShotButton.clicked.connect(self.onClickLongShot)


        #video recording
        videoRecButton = QPushButton('Video Recording')
        videoRecButton.setStyleSheet("QPushButton {background-color : #4B8BBE; color : black}")
        videoRecButton.clicked.connect(self.onClickVideo)

        vbox.addLayout(horizontalLayer)
        vbox.addWidget(self.mainTab)

        vbox.addWidget(singleShotButton)
        vbox.addWidget(longShotButton)
        vbox.addWidget(videoRecButton)

    def awbMode(self):
        self.awbModeVal = bool(not self.awbModeVal)
 
    def openImage(self):
        allFiles = glob.glob('images/'+self.today+'/*') 
        latestImage = max(allFiles, key=os.path.getctime)
        os.system('gpicview '+latestImage)
       

    def updateAllParam(self):
        os.system('rostopic pub -1 /cam_control std_msgs/String cam-control_'+ \
        str(self.isoValGroup[1].value())+'_'+ \
        str(self.shutterSpeedGroup[1].value())+'_'+ \
        str(self.numberFrameGroup[1].value())+'_'+ \
        str(self.analogGainGroup[1].value())+'_'+ \
        str(self.awbModeVal)+'_'+ \
        str(self.awbGainGroup[1].value())
        )
        
    def onClickLongShot(self):
        os.system('rostopic pub -1 /cam_control std_msgs/String capture_s102_img:'+str(self.numberImageGroup[1].value())+  \
            '_name:test')
    def onClickVideo(self):
        os.system('rostopic pub -1 /cam_control std_msgs/String capture_s103_img')
    def onClickqv(self):
        os.system('qv4l2')    
    def onClickSingleShot(self):
        os.system('rostopic pub -1 /cam_control std_msgs/String capture_s101')
    def onClickPreview(self):
        os.system('rostopic pub -1 /cam_control std_msgs/String cap_p100')
    def onClickClosePreview(self):
        os.system('rostopic pub -1 /cam_control std_msgs/String cap_p400')

    def altButton(self):
        rospy.loginfo('rostopic pub -1 /motor_control std_msgs/String altmotor_'+str(self.altSlider[1].value())+'_'+str(self.altTopBottom.isChecked())+" -1")
        os.system('rostopic pub -1 /motor_control std_msgs/String altmotor_'+str(self.altSlider[1].value())+'_'+str(self.altTopBottom.isChecked())+" -1")

    def azButton(self):
        os.system('rostopic pub -1 /motor_control std_msgs/String hrmotor_'+str(self.azSlider[1].value())+'_'+str(self.azRightLeft.isChecked())+" -1")


class RpiStudio(QMainWindow):

    def __init__(self):
        super(QMainWindow,self).__init__()
        self.title = 'Telescope Control'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.form_widget = RightLayout(self) 
        self.setCentralWidget(self.form_widget)
        self.showMaximized()

    def teleMenuBar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Log')
        menubar = self.menuBar()
        
        # settings
        settingsMenu = menubar.addMenu('Settings')
        self.camSettings = QAction("Camera", self,checkable= True)
        self.camSettings.triggered.connect(self.camMenuSettings)
        self.motorSettings = QAction("Motor", self,checkable=True)
        self.motorSettings.triggered.connect(self.motorMenuSettings)
        self.camSettings.setChecked(True)
        settingsMenu.addAction(self.camSettings)
        settingsMenu.addAction(self.motorSettings)
        
        #window
        viewMenu = menubar.addMenu('Window')
        viewStatAct = QAction('Log Details', self,checkable=True)
        viewStatAct.setStatusTip('Log Detail')
        viewStatAct.triggered.connect(self.toggleMenu)
        viewMenu.addAction(viewStatAct)

        viewFull = QAction('Full Screen', self, checkable=True)
        viewFull.setStatusTip('Full Screen Mode')
        viewFull.triggered.connect(self.toggleScreen)
        viewMenu.addAction(viewFull)
        
    def camMenuSettings(self):
        self.form_widget.container_1.setVisible(True)
        self.form_widget.container_2.setVisible(False)
        self.camSettings.setChecked(True)
        self.motorSettings.setChecked(False)
    def motorMenuSettings(self):
        self.form_widget.container_1.setVisible(False)
        self.form_widget.container_2.setVisible(True)
        self.camSettings.setChecked(False)
        self.motorSettings.setChecked(True)

    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

    def toggleScreen(self,state):
        if state:
            self.showMaximized()
        else:
            self.showNormal()
        
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.teleMenuBar()
        self.show()



if __name__ == '__main__':
    rospy.init_node('widget_gui')
    try:
        defaultfont = QFont('Arial', 8)
        defaultfont.setPixelSize(8)
        QApplication.setStyle("fusion")
        QApplication.setFont(defaultfont)
        app = QApplication(sys.argv)
        ex = RpiStudio()
        sys.exit(app.exec_())
    except rospy.ROSInterruptException: pass
    