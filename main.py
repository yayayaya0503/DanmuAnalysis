# coding=utf-8
""" 测试qss文件 """
import sys


from Danmu import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication
from myVideoWidget import myVideoWidget

class Example(QtWidgets.QMainWindow, Ui_MainWindow):
    """ 测试用例 """
    def __init__(self):
        super().__init__()
        self.loadQSS()
        self.setupUi(self)
        self.show()
        self.videoFullScreen = False   # 判断当前widget是否全屏
        self.videoFullScreenWidget = myVideoWidget()   # 创建一个全屏的widget
        self.videoFullScreenWidget.setFullScreen(1)
        self.videoFullScreenWidget.hide()               # 不用的时候隐藏起来
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.wgt_video)  # 视频播放输出的widget，就是上面定义的
        self.btn_open.clicked.connect(self.openVideoFile)   # 打开视频文件按钮
        self.btn_play.clicked.connect(self.playVideo)       # play
        self.btn_stop.clicked.connect(self.pauseVideo)       # pause
        self.player.positionChanged.connect(self.changeSlide)      # change Slide
        self.videoFullScreenWidget.doubleClickedItem.connect(self.videoDoubleClicked)  #双击响应
        self.wgt_video.doubleClickedItem.connect(self.videoDoubleClicked)   #双击响应
    def openVideoFile(self):
        try:
            self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
            self.player.play()  # 播放视频
        except Exception as e:
            QMessageBox.critical(self, "错误", "请选择flv格式的视频文件")
    def playVideo(self):
        try:
            self.player.play()
        except Exception as e:
            QMessageBox.critical(self, "错误", "请选择flv格式的视频文件")
    def pauseVideo(self):
        self.player.pause()
    def changeSlide(self,position):
        self.vidoeLength = self.player.duration()+0.1
        self.sld_video.setValue(round((position/self.vidoeLength)*100))
        self.lab_video.setText(str(round((position/self.vidoeLength)*100,2))+'%')
    def videoDoubleClicked(self,text):
        if self.player.duration() > 0:  # 开始播放后才允许进行全屏操作
            if self.videoFullScreen:
                self.player.pause()
                self.videoFullScreenWidget.hide()
                self.player.setVideoOutput(self.wgt_video)
                self.player.play()
                self.videoFullScreen = False
            else:
                self.player.pause()
                self.videoFullScreenWidget.show()
                self.player.setVideoOutput(self.videoFullScreenWidget)
                self.player.play()
                self.videoFullScreen = True


    def loadQSS(self):
        """ 加载QSS """
        #file = 'w_window.qss'
        file = 'window.qss'
        with open(file, 'rt', encoding='utf8') as f:
            styleSheet = f.read()
        self.setStyleSheet(styleSheet)
        f.close()

   
    def updateProgressBar(self):
        self.progressBar.setValue(self.horizontalSlider.value())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
