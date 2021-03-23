#!/usr/bin/env python
# -*- coding: utf-8
from PyQt5.QtWidgets import QApplication, QWidget    #导入相应的包
from PyQt5.QtWidgets import QApplication , QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow,QApplication,QWidget,QPushButton,QLabel,QLineEdit,QTextBrowser,QGroupBox,QCheckBox)
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QThread
#字幕提取
import pandas as pd
# 爬取弹幕
import requests, re, time, csv,hashlib,urllib.request
from bs4 import BeautifulSoup as BS
from selenium import webdriver

from lxml import etree
from pprint import pprint
import json
import jieba
import numpy as np
from PIL import Image,ImageTk
from wordcloud import WordCloud as wc

from jieba import analyse
# 引入TF-IDF关键词抽取接口
tfidf = analyse.extract_tags
# 引入TextRank关键词抽取接口
textrank = analyse.textrank
# LDA
from gensim import corpora, models
import jieba.posseg as jp

from snownlp import SnowNLP
import matplotlib.pyplot as plt
import matplotlib.image as mpimg # mpimg 用于读取图片

# 爬取视频
from xml.dom.minidom import parseString
from moviepy.editor import *
import os, sys

from myVideoWidget import myVideoWidget
import datetime
#视频下载变量
thestart_time = time.time()

danmu_model = QtGui.QStandardItemModel()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowMinimizeButtonHint)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 650)
        #self.frame_window = QWidget(self)
        #self.frame_window.setGeometry(0, 0,1052, 635)
        #self.frame_window.setObjectName('frame_window')
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.getavnumber = QtWidgets.QPushButton(self.centralwidget)
        self.getavnumber.setGeometry(QtCore.QRect(658, 32, 91, 23))
        self.getavnumber.setText("")
        self.getavnumber.setObjectName("getavnumber")
        self.getavnumber.setToolTip(u'获取弹幕视频信息')
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(300, 35, 361, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setToolTip(u'请输入B站视频av号码')
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setGeometry(QtCore.QRect(10, 80, 1031, 501))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")

        self.danmumodel = QtGui.QStandardItemModel()
        self.tableView = QtWidgets.QTableView(self.tab_8)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 1001, 451))
        self.tableView.setObjectName("tableView")
        self.tableView.setModel(self.danmumodel)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.danmumodel.setHorizontalHeaderLabels(['出现时间', '弹幕模式', '字号', '颜色', '发送时间' ,'弹幕池', '发送者id', 'rowID', '弹幕内容'])
        
        self.tabWidget_2.addTab(self.tab_8, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.graphicsciyun = QtWidgets.QGraphicsView(self.tab_3)
        self.graphicsciyun.setGeometry(QtCore.QRect(290, 10, 451, 451))
        self.graphicsciyun.setObjectName("graphicsciyun")
        self.bshowciyun = QtWidgets.QPushButton(self.tab_3)
        self.bshowciyun.setGeometry(QtCore.QRect(940, 440, 75, 23))
        self.bshowciyun.setObjectName("bshowciyun")
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.graphicsnlp = QtWidgets.QGraphicsView(self.tab_4)
        self.graphicsnlp.setGeometry(QtCore.QRect(290, 10, 451, 451))
        self.graphicsnlp.setObjectName("graphicsnlp")
        self.bshownlp = QtWidgets.QPushButton(self.tab_4)
        self.bshownlp.setGeometry(QtCore.QRect(940, 440, 75, 23))
        self.bshownlp.setObjectName("bshownlp")
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")

        self.zimumodel = QtGui.QStandardItemModel()
        self.zimumodel.setHorizontalHeaderLabels(['出现时间', '弹幕模式', '弹幕内容'])
        self.tableView = QtWidgets.QTableView(self.tab_6)
        self.tableView.setGeometry(QtCore.QRect(10, 100, 1001, 361))
        self.tableView.setObjectName("tableView_2")
        self.tableView.setModel(self.zimumodel)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        
        self.label_3 = QtWidgets.QLabel(self.tab_6)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 54, 30))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_6)
        self.label_4.setGeometry(QtCore.QRect(0, 70, 54, 30))
        self.label_4.setObjectName("label_4")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_6)
        self.textBrowser_2.setGeometry(QtCore.QRect(10, 20, 1001, 41))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.getzimu = QtWidgets.QPushButton(self.tab_6)
        self.getzimu.setGeometry(QtCore.QRect(910, 70, 101, 23))
        self.getzimu.setObjectName("getzimu")
        self.tabWidget_2.addTab(self.tab_6, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.hilghtsmodel = QtGui.QStandardItemModel()
        self.hilghtsmodel.setHorizontalHeaderLabels(['出现时间', '弹幕数量'])
        self.tableView2 = QtWidgets.QTableView(self.tab_5)
        self.tableView2.setGeometry(QtCore.QRect(10, 10, 1001, 451))
        self.tableView2.setObjectName("textBrowser_4")
        self.tableView2.setModel(self.hilghtsmodel)
        self.tableView2.horizontalHeader().setStretchLastSection(True)
        self.tabWidget_2.addTab(self.tab_5, "")

        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")

        self.timetagmodel = QtGui.QStandardItemModel()
        self.timetagmodel.setHorizontalHeaderLabels(['出现时间', '视频标签'])        
        self.textBrowser_5 = QtWidgets.QTableView(self.tab_7)
        self.textBrowser_5.setGeometry(QtCore.QRect(10, 10, 1001, 451))
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.textBrowser_5.setModel(self.timetagmodel)
        self.textBrowser_5.horizontalHeader().setStretchLastSection(True)
        
        self.tabWidget_2.addTab(self.tab_7, "")

        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.downloadvideo = QtWidgets.QPushButton(self.tab_9)
        self.downloadvideo.setGeometry(QtCore.QRect(510, 0, 75, 23))
        self.downloadvideo.setObjectName("downloadvideo")
        self.downloadvideo.setToolTip(u'下载视频')
        #self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_9)
        #self.lineEdit_2.setGeometry(QtCore.QRect(80, 3, 113, 30))
        #self.lineEdit_2.setObjectName("lineEdit_2")
        #self.lineEdit_2.setToolTip(u'请输入下载视频的清晰度(1080p:80;720p:64;480p:32;360p:15)(填写80或64或32或15)')
        self.label = QtWidgets.QLabel(self.tab_9)
        self.label.setGeometry(QtCore.QRect(0, 2, 80, 30))
        self.label.setObjectName("label")
        self.btn_open = QtWidgets.QPushButton(self.tab_9)
        self.btn_open.setGeometry(QtCore.QRect(260, 430, 91, 31))
        self.btn_open.setObjectName("btn_open")
        self.wgt_video = myVideoWidget(self.tab_9)
        self.wgt_video.setGeometry(QtCore.QRect(230, 35, 565, 361))
        self.wgt_video.setObjectName("wgt_video")
        self.btn_play = QtWidgets.QPushButton(self.tab_9)
        self.btn_play.setGeometry(QtCore.QRect(460, 430, 91, 31))
        self.btn_play.setObjectName("btn_play")
        self.lab_video = QtWidgets.QLabel(self.tab_9)
        self.lab_video.setGeometry(QtCore.QRect(650, 400, 91, 31))
        self.lab_video.setObjectName("lab_video")
        self.btn_stop = QtWidgets.QPushButton(self.tab_9)
        self.btn_stop.setGeometry(QtCore.QRect(670, 430, 91, 31))
        self.btn_stop.setObjectName("btn_stop")
        self.sld_video = QtWidgets.QSlider(self.tab_9)
        self.sld_video.setGeometry(QtCore.QRect(380, 400, 251, 31))
        self.sld_video.setMaximum(100)
        self.sld_video.setOrientation(QtCore.Qt.Horizontal)
        self.sld_video.setObjectName("sld_video")
        self.radioButton = QtWidgets.QRadioButton(self.tab_9)
        self.radioButton.setGeometry(QtCore.QRect(70, 6, 89, 23))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab_9)
        self.radioButton_2.setGeometry(QtCore.QRect(180, 6, 89, 23))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.tab_9)
        self.radioButton_3.setGeometry(QtCore.QRect(290, 6, 89, 23))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.tab_9)
        self.radioButton_4.setGeometry(QtCore.QRect(400, 6, 89, 23))
        self.radioButton_4.setObjectName("radioButton_4")
        self.tabWidget_2.addTab(self.tab_9, "")

        
        self.title_frame = QLabel(self.centralwidget)
        self.title_frame.setGeometry(0, 0, 300, 40)
        self.title_frame.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_frame.setFont(QFont("微软雅黑", 14, QFont.Bold))
        self.title_frame.setObjectName("title_frame")
        self.title_frame.setText(u" 弹幕视频信息提取系统")

        clsfont = self.font() or QFont()
        clsfont.setFamily('Webdings')
        self.button_close = QPushButton('r', self.centralwidget, font=clsfont)
        self.button_close.setGeometry(950, 0, 20, 30)
        self.button_close.setObjectName('button_close')
        self.button_close.setToolTip(u'关闭')
        self.button_close.enterEvent(self.button_close.setCursor(Qt.PointingHandCursor))
        self.button_min = QPushButton('0', self.centralwidget, font=clsfont)
        self.button_min.setGeometry(840, 0, 20, 30)
        self.button_min.setObjectName('button_min')
        self.button_min.setToolTip(u'最小化')
        self.button_min.enterEvent(self.button_min.setCursor(Qt.PointingHandCursor))

        
        #self.button_min = QtWidgets.QPushButton(self.centralwidget)
        #self.button_min.setGeometry(QtCore.QRect(910, 0, 75, 23))
        #self.button_min.setObjectName("button_min")

        
        #self.button_close = QtWidgets.QPushButton(self.centralwidget)
        #self.button_close.setGeometry(QtCore.QRect(980, 0, 75, 23))
        #self.button_close.setObjectName("button_close")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 590, 151, 30))
        self.label_2.setObjectName("label_2")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        #self.tabWidget_2.setCurrentIndex(3)
        self.getavnumber.clicked.connect(self.uploadavnumber)
        self.bshownlp.clicked.connect(self.fshownlp)
        self.bshowciyun.clicked.connect(self.fshowciyun)
        self.getzimu.clicked.connect(self.fgetzimu)
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.downloadvideo.clicked.connect(self.fdownloadvideo)

        # conexiones
        self.button_close.clicked.connect(self.close)
        self.button_min.clicked.connect(self.showMinimized)
    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)


        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.getavnumber.setText(_translate("MainWindow", "获取信息"))
        self.lineEdit.setText(_translate("MainWindow", "请输入B站视频av号码，如：52489298"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_8), _translate("MainWindow", "弹幕数据"))
        self.bshowciyun.setText(_translate("MainWindow", "查看大图"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("MainWindow", "词云"))
        self.bshownlp.setText(_translate("MainWindow", "查看大图"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "情感图"))
        self.label_3.setText(_translate("MainWindow", "关键词"))
        self.label_4.setText(_translate("MainWindow", "字幕"))
        self.getzimu.setText(_translate("MainWindow", "获取字幕"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("MainWindow", "字幕提取"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("MainWindow", "精彩时刻预测"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_7), _translate("MainWindow", "时序性标签"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_9), _translate("MainWindow", "下载视频"))
        self.label.setText(_translate("MainWindow", "视频清晰度"))
        self.radioButton.setText(_translate("MainWindow", "1080p"))
        self.radioButton_2.setText(_translate("MainWindow", "720p"))
        self.radioButton_3.setText(_translate("MainWindow", "480p"))
        self.radioButton_4.setText(_translate("MainWindow", "360p"))
        self.downloadvideo.setText(_translate("MainWindow", "下载"))
        self.btn_open.setText(_translate("MainWindow", "打开视频文件"))
        self.btn_play.setText(_translate("MainWindow", "播放"))
        self.lab_video.setText(_translate("MainWindow", "0%"))
        self.btn_stop.setText(_translate("MainWindow", "暂停"))
        #self.label_2.setText(_translate("MainWindow", "系统准备好了"))
        #self.title_frame.setText(_translate("MainWindow", "弹幕视频信息提取系统"))
        #self.button_min.setText(_translate("MainWindow", "PushButton"))
        #self.button_close.setText(_translate("MainWindow", "PushButton"))
        
    def uploadavnumber(self):
        self.label_2.setText(u"正在获取弹幕数据")
        try:
            self.label_2.setText(u"正在获取弹幕数据")
            url_num = self.lineEdit.text()

            self.label_2.setText(u"正在获取弹幕数据")
            
            b = Bili(url_num)
            b.run()
        
            getdanmustarttime = datetime.datetime.now()
            video_url = "https://www.bilibili.com/video/av{}".format(url_num)
            # video_url ='http://www.bilibili.com/video/av5038338/'
            video_html = open_url(video_url)
            danmu_id = get_danmu_id(video_html, video_url)
            all_list = []
            content = []
            if danmu_id:
                danmu_url = 'http://comment.bilibili.com/{}.xml'.format(danmu_id)
                danmu_html = open_url(url=danmu_url)
                soup = BS(danmu_html, 'lxml')
                all_d = soup.select('d')
                for d in all_d:
                    #把d标签中P的各个属性分离开
                    danmu_list = d['p'].split(',')
                    #d.get_text()是弹幕内容
                    danmu_list.append(d.get_text())
                    danmu_list[0] = sec2str(danmu_list[0])
                    danmu_list[4] = time.ctime(eval(danmu_list[4]))
                    all_list.append(danmu_list)
                    # print(d.get_text())
                    content.append(d.get_text()+'\n')
                # print(content)
                all_list.sort(key=takeFirst)
                csv_write(all_list,url_num)
                print('保存成功')
        
            url_num = self.lineEdit.text()
            fileName = "E:\\毕设\\弹幕数据\\总数据\\av{}danmu.csv".format(url_num)
            #all_list = []
            #all_list = df.query('弹幕模式 == "5"')        
            #self.textBrowser.setText(all_list)
            self.danmumodel.clear()
            self.danmumodel.setHorizontalHeaderLabels(['出现时间', '弹幕模式', '字号', '颜色', '发送时间' ,'弹幕池', '发送者id', 'rowID', '弹幕内容'])
            with open(fileName, "r", encoding="utf-8") as fileInput:
                for row in csv.reader(fileInput):    
                    items = [
                        QtGui.QStandardItem(field)
                        for field in row
                    ]
                    self.danmumodel.appendRow(items)
                
            filename = "E:\\毕设\\弹幕数据\\生活区\\av号{}danmu.jpg".format(url_num)
            img=QImage()
            img.load(filename)
            img=img.scaled(self.graphicsciyun.width(),self.graphicsciyun.height())
            scene=QGraphicsScene()
            scene.addPixmap(QPixmap().fromImage(img))
            self.graphicsciyun.setScene(scene)
        
            filenamenlp = "E:\\毕设\\弹幕数据\\生活区\\av号{}nlp.jpg".format(url_num)
            img2=QImage()
            img2.load(filenamenlp)
            img2=img2.scaled(self.graphicsnlp.width(),self.graphicsnlp.height())
            scene2=QGraphicsScene()
            scene2.addPixmap(QPixmap().fromImage(img2))
            self.graphicsnlp.setScene(scene2)

            filenamekeyword = "E:\\毕设\\弹幕数据\\生活区\\av号{}textrank_keywords.txt".format(url_num)
            filekeyword = open(filenamekeyword,'r', encoding="utf-8")
            strkey = filekeyword.read()
            filekeyword.close()
            self.textBrowser_2.setText(strkey)
            getdanmuendtime = datetime.datetime.now()
            print ("获取弹幕")
            print ((getdanmuendtime - getdanmustarttime))

            self.label_2.setText(u"系统准备好了")
        except Exception as e:
            QMessageBox.critical(self, "错误", "请输入正确的视频号码")


    def fshownlp(self):
        url_num = self.lineEdit.text()
        nlpimage = mpimg.imread("E:\\毕设\\弹幕数据\\生活区\\av号{}nlp.jpg".format(url_num)) # 读取和代码处于同一目录下的 lena.png
        # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
        nlpimage.shape #(512, 512, 3)
 
        plt.imshow(nlpimage) # 显示图片
        plt.axis('off') # 不显示坐标轴
        plt.show()

    def fshowciyun(self):
        url_num = self.lineEdit.text()
        danmuimage = mpimg.imread("E:\\毕设\\弹幕数据\\生活区\\av号{}danmu.jpg".format(url_num)) # 读取和代码处于同一目录下的 lena.png
        # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
        danmuimage.shape #(512, 512, 3)
 
        plt.imshow(danmuimage) # 显示图片
        plt.axis('off') # 不显示坐标轴
        plt.show()
               
    def fgetzimu(self):
        try:
            getdanmustarttime = datetime.datetime.now()
            # 读写csv文件
            url_num = self.lineEdit.text()
        
            df = pd.read_csv("E:\\毕设\\弹幕数据\\总数据\\av{}danmu.csv".format(url_num),usecols=[0,1,8])

            df.query('弹幕模式 == "4"').to_csv('E:/毕设/弹幕数据/总数据/av{}zimu.csv'.format(url_num),encoding='utf-8')

        
        
            self.zimumodel.clear()
            fileName = "E:\\毕设\\弹幕数据\\总数据\\av{}zimu.csv".format(url_num)
            self.zimumodel.setHorizontalHeaderLabels(['出现时间', '弹幕模式', '弹幕内容'])
            with open(fileName, "r", encoding="utf-8") as fileInput:
                for row in csv.reader(fileInput):    
                    items = [
                        QtGui.QStandardItem(field)
                        for field in row
                    ]
                    self.zimumodel.appendRow(items)
            getdanmuendtime = datetime.datetime.now()
            print ("zimu")
            print ((getdanmuendtime - getdanmustarttime))
            self.highlights()
            self.timetag()
        except Exception as e:
            QMessageBox.critical(self, "错误", "请先点击主界面按钮获取弹幕数据")

    def highlights(self):
        getdanmustarttime = datetime.datetime.now()
        # 读写csv文件
        url_num = self.lineEdit.text()
        fileName = " all_data/av{}hlights.csv".format(url_num)
        df = pd.read_csv("all_data/av{}danmu.csv".format(url_num))
        df['出现时间'].value_counts().to_csv('all_data/av{}hlights.csv'.format(url_num),encoding='utf-8')
        #print(df['出现时间'].value_counts())
        self.hilghtsmodel.clear()
        self.hilghtsmodel.setHorizontalHeaderLabels(['出现时间', '弹幕数量'])
        with open(fileName, "r", encoding="utf-8") as fileInput:
            for row in csv.reader(fileInput):    
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.hilghtsmodel.appendRow(items)
        getdanmuendtime = datetime.datetime.now()
        print ("highlights")
        print ((getdanmuendtime - getdanmustarttime))


    def timetag(self):
        getdanmustarttime = datetime.datetime.now()
        # 读写csv文件
        url_num = self.lineEdit.text()
        df = pd.read_csv("all_data/av{}danmu.csv".format(url_num),usecols=[0,8])
        tagsdata = df.groupby(by='出现时间')['弹幕内容'].sum()
        n = 0
        for datai in tagsdata:
            text=str(datai)
            # 基于TextRank算法进行关键词抽取
            datai = textrank(text)
            tagsdata[n] = datai
            n = n + 1
            #print(datai)
        print(tagsdata)
        tagsdata.to_csv('all_data/av{}timetag.csv'.format(url_num),encoding='utf-8')
        self.timetagmodel.clear()
        self.timetagmodel.setHorizontalHeaderLabels(['出现时间', '视频标签'])
        with open('all_data/av{}timetag.csv'.format(url_num), "r", encoding="utf-8") as fileInput:
            for row in csv.reader(fileInput):    
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.timetagmodel.appendRow(items)
        getdanmuendtime = datetime.datetime.now()
        print ("timetag")
        print ((getdanmuendtime - getdanmustarttime))


    def fdownloadvideo(self):
        #用户输入av号或者视频链接地址
        #print('*'*30 + 'B站视频下载小助手' + '*'*30)
        #start = input('请输入您要下载的B站av号或者视频链接地址:')
        #if start.isdigit() == True: #如果输入的是av号
            #start_url = 'https://www.bilibili.com/video/av' + start
        #else:
            #start_url = start

        start_url = 'https://www.bilibili.com/video/av' + self.lineEdit.text()
        start_url = 'https://www.bilibili.com/video/' + self.lineEdit.text()

        #视频质量
        # <accept_format><![CDATA[flv,flv720,flv480,flv360]]></accept_format>
        # <accept_description><![CDATA[高清 1080P,高清 720P,清晰 480P,流畅 360P]]></accept_description>
        # <accept_quality><![CDATA[80,64,32,15]]></accept_quality>
        #quality = input('请输入您要下载视频的清晰度(1080p:80;720p:64;480p:32;360p:15)(填写80或64或32或15):')
        try:
            #quality = self.lineEdit_2.text()
            if self.radioButton.isChecked():
                quality = 80
            elif self.radioButton_2.isChecked():
                quality = 64
            elif self.radioButton_3.isChecked():
                quality = 32
            elif self.radioButton_4.isChecked():
                quality = 15

            #获取视频的cid,title
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            }
            html = requests.get(start_url,headers=headers).text
            cid = re.search(r'cid=(\d+)&',html).group(1)
            title = re.search(r'<h1 title="(.*?)" class="video-title"',html).group(1)
            print('[下载视频的cid]:' +cid)
            print('[下载视频的标题]:' + title)
            # 清洗一下标题名称(不能有\ / : * ? " < > |)
            title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的

            #访问API地址
            entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
            appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
            params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
            chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
            url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
            headers = {
                'Referer':start_url,  #注意加上referer
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
            }
            # print(url_api)
            html = requests.get(url_api,headers=headers).json()
            # print(json.dumps(html))
            video_list = [html['durl'][0]['url']]
            # print(video_list)

            #下载视频
            '''
            urllib.urlretrieve 的回调函数：
            def callbackfunc(blocknum, blocksize, totalsize):
                @blocknum:  已经下载的数据块
                @blocksize: 数据块的大小
                @totalsize: 远程文件的大小
            '''


            print('[正在下载,请稍等...]:' + title)
            currentVideoPath = os.path.join(sys.path[0],'bilibili_video',title)  #当前目录作为下载目录
            num = 1
            for i in video_list:
                opener = urllib.request.build_opener()
                # 请求头
                opener.addheaders = [
                    # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
                    ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
                    ('Accept', '*/*'),
                    ('Accept-Language', 'en-US,en;q=0.5'),
                    ('Accept-Encoding', 'gzip, deflate, br'),
                    ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
                    ('Referer', start_url),  #注意修改referer,必须要加的!
                    ('Origin', 'https://www.bilibili.com'),
                    ('Connection', 'keep-alive'),
                ]
                urllib.request.install_opener(opener)
                #创建文件夹存放下载的视频
                if not os.path.exists(currentVideoPath):
                    os.makedirs(currentVideoPath)
                #开始下载
                thestart_time = time.time()
                urllib.request.urlretrieve(url=i,filename=os.path.join(currentVideoPath,r'{}-{}.flv'.format(title,num)), reporthook=Schedule_cmd)  #写成mp4也行  title + '-' + num + '.flv'
                num +=1

            #合并视频
            if len(video_list) >= 2:
                #视频大于一段才要合并
                print('[下载完成,正在合并视频]')
                # 定义一个数组
                L = []
                # 访问 video 文件夹 (假设视频都放在这里面)
                root_dir = currentVideoPath
                # 遍历所有文件
                for file in sorted(os.listdir(root_dir), key=lambda x: int(x[x.rindex("-")+1:x.rindex(".")])):
                    # 如果后缀名为 .mp4/.flv
                    if os.path.splitext(file)[1] == '.flv':
                         # 拼接成完整路径
                         filePath = os.path.join(root_dir, file)
                         # 载入视频
                         video = VideoFileClip(filePath)
                         # 添加到数组
                         L.append(video)
                # 拼接视频
                final_clip = concatenate_videoclips(L)
                # 生成目标视频文件
                final_clip.to_videofile(os.path.join(root_dir,r'{}.mp4'.format(title)), fps=24, remove_temp=False)
                print('[视频合并完成]')

            else:
                #视频只有一段则直接打印下载完成
                print('[下载完成]:' + title)
            #拓展:分P视频:url相同,只是cid不同,通过url?p=1,2..分别找出每个分P的cid,带入请求得到下载地址
            #如果是windows系统，下载完成后打开下载目录
            if(sys.platform.startswith('win')):
                os.startfile(currentVideoPath)
        except Exception as e:
            QMessageBox.critical(self, "错误", "请选择视频清晰度")

        
# 爬取视频
def Schedule_cmd(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - thestart_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # 设置下载进度条
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    # time.sleep(0.1)
    f.write('\r')


def Schedule(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - thestart_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # 设置下载进度条
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    print(percent_str.ljust(6, ' ') + '-'+ speed_str)
    f.flush()
    time.sleep(2)
    # print('\r')

# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % (G)
        else:
            return "%.3fM" % (M)
    else:
        return "%.3fK" % (kb)
# 爬虫        

#打开网页函数
def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    return html
#获取弹幕url中的数字id号

#当requests行不通时，采用selenium的方法。
def sele_get(url):
    SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
    driver = webdriver.PhantomJS(service_args = SERVICE_ARGS)
    driver.get(url)
    time.sleep(2)
    danmu_id = re.findall(r'cid=(\d+)&', driver.page_source)[0]

    return danmu_id


def get_danmu_id(html, url):
    try:
        soup = BS(html, 'lxml')
        #视频名
        title = soup.select('title[data-vue-meta="true"]')[0].get_text()
        #投稿人
        author = soup.select('meta[name="author"]')[0]['content']
        #弹幕的网站代码
        try:

            danmu_id = re.findall(r'cid=(\d+)&', html)[0]
            #danmu_id = re.findall(r'/(\d+)-1-64', html)[0]
            #print(danmu_id)
        except:
            danmu_id = sele_get(url)
        print(title, author)
        return danmu_id
    except:
        print('视频不见了哟')
        return False
#秒转换成时间
def sec2str(seconds):
    seconds = eval(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    time = "%02d:%02d:%02d" % (h, m, s)
    return time

#csv保存函数
def csv_write(tablelist,url_num):
    tableheader = ['出现时间', '弹幕模式', '字号', '颜色', '发送时间' ,'弹幕池', '发送者id', 'rowID', '弹幕内容']
    with open('all_data/av{}danmu.csv'.format(url_num), 'w', newline='', errors='ignore',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(tableheader)
        for row in tablelist:
            writer.writerow(row)
            
#列表排序方法
def takeSecond(elem):
    return elem[1]            
def takeFirst(elem):
    return elem[0]


class Bili(object):
    def __init__(self,url_num):
        self.name = "av号"+str(url_num)
        self.url = "https://www.bilibili.com/video/av{}".format(url_num)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

    def parse(self, url):
        response = requests.get(url,headers=self.headers)
        res = response.content.decode()
        return res

    def get_content(self,res):
        html = etree.HTML(res)
        item = {}
        item["title"] = html.xpath("//div[@id='viewbox_report']/h1/@title")[0] if len(html.xpath("//div[@id='viewbox_report']/h1/@title"))>0 else None
        if item["title"]:
            item["cid"] = re.findall(r"cid=([\d]+)&",res)[0]
        else:
            return None
        print(item)
        return item

    def get_url(self, item):
        cid = item["cid"]
        danmu_url = "https://comment.bilibili.com/{}.xml".format(cid)
        print(danmu_url)
        # 延时操作，防止太快爬取
        time.sleep(2)
        return danmu_url

    def get_danmu(self, res, item):
        # pprint(res)
        html = etree.HTML(res.encode())
        item = html.xpath('//d/text()')
        # pprint(item)
        return item

    def save(self, name, content):
        with open("all_data/{}.json".format(name),"a",encoding="utf-8")as f:
            f.write(json.dumps(content,ensure_ascii=False,indent=4))
            print("保存成功")
        with open("all_data/{}.txt".format(name),"a",encoding="utf-8")as f:
            f.write(json.dumps(content,ensure_ascii=False,indent=4))
            print("保存成功")
        
    # 弹幕去重
    def remove_double_barrage(self):
        '''
        double_arrage:所有重复弹幕的集合
        results:去重后的弹幕
        barrage:每种弹幕内容都存储一遍
        '''
        item = {}
        # 1 获取url
        # 2 发送请求，获取相应
        res = self.parse(self.url)
        # 3 提取cid和标题
        item = self.get_content(res)
        if item==None:
            print("vid号不正确，请重新输入。")
            return
        # 4 组合弹幕url
        danmu_url = self.get_url(item)
        # 5 发送请求获取相应
        res_danmu = self.parse(danmu_url)
        # 6 提取
        end = self.get_danmu(res_danmu, item)
        # pprint(end)
        double_barrage=[]
        results=[]
        barrage=set()
        for result in end:
            # pprint(result)
            if result not in results:
                results.append(result)
                
            else:
                double_barrage.append(result)
                barrage.add(result)
        
        return double_barrage,results,barrage
        
    # 创建停用词list  
    def stopwordslist(self,filepath):  
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  
        return stopwords 
    # 弹幕重复计算和词云的制作
    def make_wordCould(self):

        getdanmustarttime = datetime.datetime.now()
        
        double_barrages,results,barrages=self.remove_double_barrage()
        # 重词计数
        with open('all_data/{}danmubarrages.txt'.format(self.name),'w',encoding='utf-8') as f:
            for barrage in barrages:
                amount=double_barrages.count(barrage)
                f.write(barrage+':'+str(amount+1)+'\n')

        # 设置停用词
        stop_words=['【','】',',','.','?','!','。','哈哈','哈哈哈','哈哈哈哈']
        stopwords = self.stopwordslist('stopwords/CNENstopwords.txt')  # 这里加载停用词的路径
        words=''
        
        results = jieba.cut(str(results),cut_all=False)
        print(results)
        #if results:
            #for result in results:
                #for stop in stop_words:
                    #result=''.join(result.split(stop))
                #words.append(result)
            # 列表拼接成字符串
            #words=''.join(words)
            #print(words)
            #words=jieba.cut(words)
            #print(words)
            #words=''.join(words)
          
        for word in results:
            if word not in stopwords:
                if word != '\t':
                    words +=word
                    words +=" "
        
        luo=np.array(Image.open('洛天依.jpg'))
        w=wc(font_path='‪C:/Windows/Fonts/SIMYOU.TTF',background_color='white',width=1600,height=1600,max_words=2000,mask=luo)
        w.generate(words)
        w.to_file('all_data/{}danmu.jpg'.format(self.name))

        getdanmuendtime = datetime.datetime.now()
        print ("wordcloud")
        print ((getdanmuendtime - getdanmustarttime))

            
    
    def tfidf_keywords(self,text):
        # 原始文本
        text=str(text)

        # 基于TF-IDF算法进行关键词抽取
        keywords = tfidf(text)
        print("保存tfidf关键词")
        # 输出抽取出的关键词
        with open('all_data/{}tfidf_keywords.txt'.format(self.name),'w',encoding='utf-8') as f:
            for keyword in keywords:
                f.write(keyword + "/")
        #branch = tk.Tk()
        #branch.title("textrank关键词提取")
            # branch.geometry('200x100')                 #是x 不是*
            # branch.resizable(width=False, height=True) #宽不可变, 高可变,默认为True
            #t = tk.Text(branch)
            #t.pack()
            #t.insert("insert", content)
        #theLabel = tk.Label(root, text="tfidf关键词", width=15).grid(row=4, column=0)
        #text = tk.Text(root, font=('微软雅黑', 10),height=2)
        #text.grid(row=4, column=1)
        #text.insert("insert", keywords)
        #branch.mainloop()   
    def textrank_keywords(self,text):

        getdanmustarttime = datetime.datetime.now()
        
        # 原始文本
        text=str(text)

        print("保存textrank关键词")
        # 基于TextRank算法进行关键词抽取
        keywords = textrank(text)
        # 输出抽取出的关键词
        with open('all_data/{}textrank_keywords.txt'.format(self.name),'w',encoding='utf-8') as f:
            for keyword in keywords:
                f.write(keyword + "/")
        #branch = tk.Tk()
        #branch.title("textrank关键词提取")
            # branch.geometry('200x100')                 #是x 不是*
            # branch.resizable(width=False, height=True) #宽不可变, 高可变,默认为True
            #t = tk.Text(branch)
            #t.pack()
            #t.insert("insert", content)
        #theLabel = tk.Label(root, text="textrank关键词", width=15).grid(row=5, column=0)
        #text = tk.Text(root, font=('微软雅黑', 10),height=2)
        #text.grid(row=5, column=1)
        #text.insert("insert", keywords)
        #branch.mainloop()

        getdanmuendtime = datetime.datetime.now()
        print ("textrank")
        print ((getdanmuendtime - getdanmustarttime))
        
    def gensimLDA(self,content):

        getdanmustarttime = datetime.datetime.now()

        # 文本集
        texts = content
        # 分词过滤条件
        jieba.add_word('仿妆')
        flags = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd')  # 词性
        stopwords = ('666','不','这么')  # 停词
        stopwords = self.stopwordslist('stopwords\CNENstopwords.txt')  # 这里加载停用词的路径
        # 分词
        words_ls = []
        for text in texts:
            
            words = [word.word for word in jp.cut(text) if word.flag in flags and word.word not in stopwords]
            # words = jieba.cut(text)
            words_ls.append(words)
            # print(text)
        
        # print(texts)
        # 构造词典
        dictionary = corpora.Dictionary(words_ls)
        # 打印词典
        # print(words_ls)
        # 基于词典，使【词】→【稀疏向量】，并将向量放入列表，形成【稀疏向量集】
        corpus = [dictionary.doc2bow(words) for words in words_ls]
        # lda模型，num_topics设置主题的个数
        lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)
        # 打印所有主题，每个主题显示10个词
        for topic in lda.print_topics(num_topics = 10,num_words=10):
            print(topic)
            with open('all_data/{}LDAtopic.txt'.format(self.name),'w',encoding='utf-8') as f:
                f.write(str(topic)+'\n')
        # 主题推断
        print(lda.inference(corpus))

        getdanmuendtime = datetime.datetime.now()
        print ("lda")
        print ((getdanmuendtime - getdanmustarttime))
        
    def contentnlp(self,content):

        getdanmustarttime = datetime.datetime.now()

        list = content
        sentimentslist = []
        for i in list:
            s = SnowNLP(i)
            # print s.sentiments
            sentimentslist.append(s.sentiments)
        plt.hist(sentimentslist, bins = np.arange(0, 1, 0.01), facecolor = 'blue')
        plt.xlabel('Sentiments Probability')
        plt.ylabel('Quantity')
        plt.title('Analysis of Sentiments')
        plt.savefig('all_data/{}nlp.jpg'.format(self.name))
        #plt.show()
        #branch = tk.Tk()
        #im=Image.open('E:\毕设\弹幕数据\生活区\{}nlp.jpg'.format(self.name))
        #img=ImageTk.PhotoImage(im)
        #imLabel=tk.Label(branch,image=img)
        # imLabel.grid(row=6, column=0, sticky='w', padx=10, pady=5)
        #branch.mainloop()

        getdanmuendtime = datetime.datetime.now()
        print ("nlp")
        print ((getdanmuendtime - getdanmustarttime))
    
    def run(self):
        item = {}
        # 1 获取url
        # 2 发送请求，获取相应
        res = self.parse(self.url)
        # 3 提取cid和标题
        item = self.get_content(res)
        if item==None:
            print("vid号不正确，请重新输入。")
            return
        # 4 组合弹幕url
        danmu_url = self.get_url(item)
        # 5 发送请求获取相应
        res_danmu = self.parse(danmu_url)
        # 6 提取
        end = self.get_danmu(res_danmu, item)
        # 7 保存
        self.save(self.name,end)
        # 8 制作词云
        self.make_wordCould()
        # 9 tfidf关键词提取
        self.tfidf_keywords(end)
        # 10 textrank关键词提取
        self.textrank_keywords(end)
        # 11 LDA
        self.gensimLDA(end)
        # 12 nlp
        self.contentnlp(end)
        
        print("程序结束")


