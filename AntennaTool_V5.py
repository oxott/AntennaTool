# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from tkinter import filedialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.interpolate import make_interp_spline, BSpline
from mpldatacursor import datacursor
from matplotlib import style
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from bisect import bisect_left
from scipy import interpolate
import math
import matplotlib.pyplot as plt
import matplotlib
import tkinter as tk
import pandas as pd
import glob
import numpy as np
import matplotlib.pylab as pylab
from scipy.optimize import root_scalar


params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

matplotlib.use('Qt5Agg')
style.use("ggplot")

def dBm2W(dBm):
    return 10**(dBm/10)




def graficoBunito(x, y, points):
    xnew = np.linspace(x.min(), x.max(), int(points))
    spl = make_interp_spline(x, y, k=3) #BSpline object
    ynew = spl(xnew)
    return xnew, ynew, spl


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setObjectName("tabWidget")
        self.diagRad = QtWidgets.QWidget()
        self.diagRad.setObjectName("diagRad")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.diagRad)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.diagRad)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.diagRad)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.folderPath = QtWidgets.QLineEdit(self.diagRad)
        self.folderPath.setEnabled(True)
        self.folderPath.setReadOnly(True)
        self.folderPath.setObjectName("folderPath")
        self.verticalLayout_2.addWidget(self.folderPath)
        self.folderPath_4 = QtWidgets.QLineEdit(self.diagRad)
        self.folderPath_4.setReadOnly(True)
        self.folderPath_4.setClearButtonEnabled(False)
        self.folderPath_4.setObjectName("folderPath_4")
        self.verticalLayout_2.addWidget(self.folderPath_4)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.browseFolder = QtWidgets.QPushButton(self.diagRad)
        self.browseFolder.setObjectName("browseFolder")
        self.verticalLayout_7.addWidget(self.browseFolder)
        self.browseFolder_4 = QtWidgets.QPushButton(self.diagRad)
        self.browseFolder_4.setObjectName("browseFolder_4")
        self.verticalLayout_7.addWidget(self.browseFolder_4)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_freq = QtWidgets.QLabel(self.diagRad)
        self.label_freq.setObjectName("label_freq")
        self.horizontalLayout_2.addWidget(self.label_freq)
        self.cb_frequency_4 = QtWidgets.QComboBox(self.diagRad)
        self.cb_frequency_4.setObjectName("cb_frequency_4")
        self.horizontalLayout_2.addWidget(self.cb_frequency_4)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_what_plot = QtWidgets.QLabel(self.diagRad)
        self.label_what_plot.setObjectName("label_what_plot")
        self.horizontalLayout_3.addWidget(self.label_what_plot)
        self.cb_what_plot = QtWidgets.QComboBox(self.diagRad)
        self.cb_what_plot.setObjectName("cb_what_plot")
        self.horizontalLayout_3.addWidget(self.cb_what_plot)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.saveCsv = QtWidgets.QPushButton(self.diagRad)
        self.saveCsv.setObjectName("saveCsv")
        self.horizontalLayout_4.addWidget(self.saveCsv)
        self.verticalLayout_8.addLayout(self.horizontalLayout_4)
        self.gridLayout_2.addLayout(self.verticalLayout_8, 0, 0, 1, 1)
        
        '''
        self.graphicsView = QtWidgets.QGraphicsView(self.diagRad)
        self.graphicsView.setObjectName("graphicsView")
        '''
        
        self.canvas = FigureCanvas(Figure(figsize=(7, 7)))
        self.ax = self.canvas.figure.add_subplot(111, polar=True)
        self.ax.set_theta_zero_location("N")
        self.ax.autoscale(enable = False)
        self.ax.set_rmax(-15)
        self.ax.set_rmin(-45)
        
        
        self.gridLayout_2.addWidget(self.canvas, 1, 0, 1, 1)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.gridLayout_2.addWidget(self.toolbar, 2, 0, 1, 1)
        
        
        self.splitter = QtWidgets.QSplitter(self.diagRad)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.normalize = QtWidgets.QCheckBox(self.splitter)
        self.normalize.setObjectName("normalize")
        self.hold = QtWidgets.QCheckBox(self.splitter)
        self.hold.setObjectName("hold")
        self.clearBtn_2 = QtWidgets.QPushButton(self.splitter)
        self.clearBtn_2.setObjectName("clearBtn_2")
        self.gridLayout_2.addWidget(self.splitter, 3, 0, 1, 1)
        self.tabWidget.addTab(self.diagRad, "")
        
        self.dist = QtWidgets.QWidget()
        self.dist.setObjectName("dist")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.dist)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_13 = QtWidgets.QLabel(self.dist)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_26.addWidget(self.label_13)
        self.folderPath_2 = QtWidgets.QLineEdit(self.dist)
        self.folderPath_2.setObjectName("folderPath_2")
        self.folderPath_2.setReadOnly(True)
        self.horizontalLayout_26.addWidget(self.folderPath_2)
        self.horizontalLayout_25.addLayout(self.horizontalLayout_26)
        self.browseFolder_2 = QtWidgets.QPushButton(self.dist)
        self.browseFolder_2.setObjectName("browseFolder_2")
        self.horizontalLayout_25.addWidget(self.browseFolder_2)
        self.gridLayout_4.addLayout(self.horizontalLayout_25, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_14 = QtWidgets.QLabel(self.dist)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_27.addWidget(self.label_14)
        self.cb_frequency_2 = QtWidgets.QComboBox(self.dist)
        self.cb_frequency_2.setObjectName("cb_frequency_2")
        self.horizontalLayout_27.addWidget(self.cb_frequency_2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_27)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_15 = QtWidgets.QLabel(self.dist)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_28.addWidget(self.label_15)
        self.cb_what_plot_2 = QtWidgets.QComboBox(self.dist)
        self.cb_what_plot_2.setObjectName("cb_what_plot_2")
        self.horizontalLayout_28.addWidget(self.cb_what_plot_2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_28)
        self.saveCsv_2 = QtWidgets.QPushButton(self.dist)
        self.saveCsv_2.setObjectName("saveCsv_2")
        self.horizontalLayout_5.addWidget(self.saveCsv_2)
        self.gridLayout_4.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        
        self.canvas_2 = FigureCanvas(Figure(figsize=(7, 7)))
        self.ax_2 = self.canvas_2.figure.add_subplot(111)
        self.gridLayout_4.addWidget(self.canvas_2, 2, 0, 1, 1)
        self.toolbar_2 = NavigationToolbar(self.canvas_2, self)
        self.gridLayout_4.addWidget(self.toolbar_2, 3, 0, 1 ,1)
        
        self.splitter_4 = QtWidgets.QSplitter(self.dist)
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.normalize_2 = QtWidgets.QCheckBox(self.splitter_4)
        self.normalize_2.setObjectName("normalize_2")
        self.hold_2 = QtWidgets.QCheckBox(self.splitter_4)
        self.hold_2.setObjectName("hold_2")
        self.clearBtn_3 = QtWidgets.QPushButton(self.splitter_4)
        self.clearBtn_3.setObjectName("clearBtn_3")
        self.gridLayout_4.addWidget(self.splitter_4, 4, 0, 1, 1)
        self.tabWidget.addTab(self.dist, "")
        self.perdas = QtWidgets.QWidget()
        self.perdas.setObjectName("perdas")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.perdas)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.label_16 = QtWidgets.QLabel(self.perdas)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_32.addWidget(self.label_16)
        self.folderPath_3 = QtWidgets.QLineEdit(self.perdas)
        self.folderPath_3.setObjectName("folderPath_3")
        self.folderPath_3.setReadOnly(True)
        self.horizontalLayout_32.addWidget(self.folderPath_3)
        self.horizontalLayout_31.addLayout(self.horizontalLayout_32)
        self.browseFolder_3 = QtWidgets.QPushButton(self.perdas)
        self.browseFolder_3.setObjectName("browseFolder_3")
        self.horizontalLayout_31.addWidget(self.browseFolder_3)
        self.verticalLayout_17.addLayout(self.horizontalLayout_31)
        self.verticalLayout_16.addLayout(self.verticalLayout_17)
        
        self.canvas_3 = FigureCanvas(Figure(figsize=(7, 7)))
        self.ax_3 = self.canvas_3.figure.add_subplot(111)
        self.verticalLayout_16.addWidget(self.canvas_3)
        
        self.toolbar_3 = NavigationToolbar(self.canvas_3, self)
        self.verticalLayout_16.addWidget(self.toolbar_3)
        
        
        
        self.verticalLayout_15.addLayout(self.verticalLayout_16)
        self.splitter_5 = QtWidgets.QSplitter(self.perdas)
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName("splitter_5")
        self.verticalLayout_15.addWidget(self.splitter_5)
        self.gridLayout_5.addLayout(self.verticalLayout_15, 0, 0, 1, 1)
        self.tabWidget.addTab(self.perdas, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setEnabled(True)
        self.tab.setObjectName("tab")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.splitter_2 = QtWidgets.QSplitter(self.tab)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.label_freq_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_freq_2.setObjectName("label_freq_2")
        self.verticalLayout_4.addWidget(self.label_freq_2)
        self.horizontalLayout_8.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.folderPath_5 = QtWidgets.QLineEdit(self.layoutWidget)
        self.folderPath_5.setMinimumSize(QtCore.QSize(81, 0))
        self.folderPath_5.setObjectName("folderPath_5")
        self.folderPath_5.setReadOnly(True)
        self.verticalLayout_5.addWidget(self.folderPath_5)
        self.folderPath_6 = QtWidgets.QLineEdit(self.layoutWidget)
        self.folderPath_6.setMinimumSize(QtCore.QSize(81, 20))
        self.folderPath_6.setObjectName("folderPath_6")
        self.folderPath_6.setReadOnly(True)
        self.verticalLayout_5.addWidget(self.folderPath_6)
        self.cb_frequency_3 = QtWidgets.QComboBox(self.layoutWidget)
        self.cb_frequency_3.setMinimumSize(QtCore.QSize(81, 20))
        self.cb_frequency_3.setObjectName("cb_frequency_3")
        self.verticalLayout_5.addWidget(self.cb_frequency_3)
        self.horizontalLayout_8.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.browseFolder_6 = QtWidgets.QPushButton(self.layoutWidget)
        self.browseFolder_6.setObjectName("browseFolder_6")
        self.verticalLayout_6.addWidget(self.browseFolder_6)
        self.browseFolder_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.browseFolder_5.setObjectName("browseFolder_5")
        self.verticalLayout_6.addWidget(self.browseFolder_5)
        self.saveCsv_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.saveCsv_3.setObjectName("saveCsv_3")
        self.verticalLayout_6.addWidget(self.saveCsv_3)
        self.horizontalLayout_8.addLayout(self.verticalLayout_6)
        self.line = QtWidgets.QFrame(self.splitter_2)
        self.line.setMaximumSize(QtCore.QSize(3, 16777215))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.widget = QtWidgets.QWidget(self.splitter_2)
        self.widget.setObjectName("widget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.GainCheckBox = QtWidgets.QCheckBox(self.widget)
        self.GainCheckBox.setObjectName("GainCheckBox")
        self.verticalLayout_12.addWidget(self.GainCheckBox)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.cb_Gain_1 = QtWidgets.QComboBox(self.widget)
        self.cb_Gain_1.setMinimumSize(QtCore.QSize(81, 20))
        self.cb_Gain_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cb_Gain_1.setObjectName("cb_Gain_1")
        self.horizontalLayout_7.addWidget(self.cb_Gain_1)
        self.verticalLayout_12.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.cb_Gain_2 = QtWidgets.QComboBox(self.widget)
        self.cb_Gain_2.setMinimumSize(QtCore.QSize(81, 20))
        self.cb_Gain_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cb_Gain_2.setObjectName("cb_Gain_2")
        self.horizontalLayout_6.addWidget(self.cb_Gain_2)
        self.verticalLayout_12.addLayout(self.horizontalLayout_6)
        self.gridLayout_6.addLayout(self.verticalLayout_12, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_3.addWidget(self.label_10)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.line_Gain_Output = QtWidgets.QLineEdit(self.widget)
        self.line_Gain_Output.setMinimumSize(QtCore.QSize(81, 20))
        self.line_Gain_Output.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.line_Gain_Output.setObjectName("line_Gain_Output")
        self.line_Gain_Output.setReadOnly(True)
        self.verticalLayout_3.addWidget(self.line_Gain_Output)
        self.gridLayout_6.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.gridLayout_7.addWidget(self.splitter_2, 0, 0, 1, 1)
        
        
        self.canvas_4 = FigureCanvas(Figure(figsize=(7, 7)))
        self.ax_4 = self.canvas_4.figure.add_subplot(111)
        self.gridLayout_7.addWidget(self.canvas_4, 1, 0, 1, 1)
        self.toolbar_4 = NavigationToolbar(self.canvas_4, self)
        self.gridLayout_7.addWidget(self.toolbar_4, 2, 0, 1, 1)
        
        
        
        
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.normalize_3 = QtWidgets.QCheckBox(self.tab)
        self.normalize_3.setObjectName("normalize_3")
        self.gridLayout.addWidget(self.normalize_3, 3, 0, 1, 1)
        self.hold_3 = QtWidgets.QCheckBox(self.tab)
        self.hold_3.setObjectName("hold_3")
        self.gridLayout.addWidget(self.hold_3, 3, 1, 1, 1)
        self.clearBtn_4 = QtWidgets.QPushButton(self.tab)
        self.clearBtn_4.setObjectName("clearBtn_4")
        self.gridLayout.addWidget(self.clearBtn_4, 3, 2, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout, 3, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setMaximumSize(QtCore.QSize(52, 16))
        self.label_8.setObjectName("label_8")
        self.verticalLayout_9.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setMaximumSize(QtCore.QSize(52, 16))
        self.label_9.setObjectName("label_9")
        self.verticalLayout_9.addWidget(self.label_9)
        self.horizontalLayout_9.addLayout(self.verticalLayout_9)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.line_med1 = QtWidgets.QLineEdit(self.tab_2)
        self.line_med1.setObjectName("line_med1")
        self.line_med1.setReadOnly(True)
        self.verticalLayout_10.addWidget(self.line_med1)
        self.line_med2 = QtWidgets.QLineEdit(self.tab_2)
        self.line_med2.setObjectName("line_med2")
        self.line_med2.setReadOnly(True)
        self.verticalLayout_10.addWidget(self.line_med2)
        self.horizontalLayout_9.addLayout(self.verticalLayout_10)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.estimate_gain_1_btn = QtWidgets.QPushButton(self.tab_2)
        self.estimate_gain_1_btn.setMaximumSize(QtCore.QSize(75, 20))
        self.estimate_gain_1_btn.setObjectName("estimate_gain_1_btn")
        self.verticalLayout_11.addWidget(self.estimate_gain_1_btn)
        self.estimate_gain_2_btn = QtWidgets.QPushButton(self.tab_2)
        self.estimate_gain_2_btn.setMaximumSize(QtCore.QSize(75, 20))
        self.estimate_gain_2_btn.setObjectName("estimate_gain_2_btn")
        self.verticalLayout_11.addWidget(self.estimate_gain_2_btn)
        self.horizontalLayout_9.addLayout(self.verticalLayout_11)
        self.gridLayout_8.addLayout(self.horizontalLayout_9, 0, 0, 1, 1)
        
        self.canvas_5 = FigureCanvas(Figure(figsize=(7,7)))
        self.ax_5 = self.canvas_5.figure.add_subplot(111)
        self.gridLayout_8.addWidget(self.canvas_5, 1, 0, 1, 1)
        self.toolbar_5 = NavigationToolbar(self.canvas_4, self)
        self.gridLayout_8.addWidget(self.toolbar_5, 2, 0, 1, 1)
        
        
        self.gridLayout_9.addLayout(self.gridLayout_8, 3, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.tabWidget, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.browseFolder.clicked.connect(self.load_csv)        
        self.browseFolder_2.clicked.connect(self.load_csv_2)    
        self.browseFolder_3.clicked.connect(self.load_csv_file)    
        self.browseFolder_4.clicked.connect(self.load_csv_file_3)    
        self.browseFolder_5.clicked.connect(self.load_csv_file_2)        
        self.browseFolder_6.clicked.connect(self.load_csv_3)    
        self.clearBtn_2.clicked.connect(self.clear_plot)
        self.clearBtn_3.clicked.connect(self.clear_plot_3)    
        self.clearBtn_4.clicked.connect(self.clear_plot_2)    
        self.saveCsv.clicked.connect(self.save_csv)    
        self.saveCsv_2.clicked.connect(self.save_csv_2)    
        self.saveCsv_3.clicked.connect(self.save_csv_3)    
        self.cb_frequency_4.activated.connect(self.update_plot)    
        self.cb_frequency_2.activated.connect(self.update_plot_2)    
        self.cb_frequency_3.activated.connect(self.update_plot_3)    
        self.cb_what_plot.activated.connect(self.what_plot)    
        self.cb_what_plot_2.activated.connect(self.what_plot_2)
        
        self.GainCheckBox.stateChanged.connect(self.GainEstimateEnabled)
        self.cb_Gain_1.activated.connect(self.GainEstimate)
        self.cb_Gain_2.activated.connect(self.GainEstimate)
        self.GainEstimateEnabled = False
        
        self.folderLoaded = False
        self.folderLoaded_2 = False
        self.lossLoaded = False
        self.lossLoaded_perda = False
        
    def GainEstimateEnabled(self, state):
        if state == Qt.Checked:
            self.GainEstimateEnabled = True
            print(self.GainEstimateEnabled)
        else:
            self.GainEstimateEnabled = False
            print(self.GainEstimateEnabled)
        self.scat = 0
    def GainEstimate(self):
        if self.folderLoaded == False:
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Open Folder"),
                                                  QtWidgets.qApp.tr("Arquivos de Distância não carregados!"),
                                                  QtWidgets.QMessageBox.Ok)
        elif self.lossLoaded == False:
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Open Folder"),
                                                  QtWidgets.qApp.tr("Arquivo de Perdas não carregado!"),
                                                  QtWidgets.QMessageBox.Ok)
        elif self.GainEstimateEnabled:
            def func(k):
                return G1dB*(1 - math.exp(-k*float(D2))) - G2dB*(1 - math.exp(-k*float(D1)))
            
            def Alfredo(k, gain, x):
                return gain*(1 - np.exp(-k*x))
                        
            D1 = self.cb_Gain_1.currentText()
            D2 = self.cb_Gain_2.currentText()
            desFreq = round(float(self.cb_frequency_3.currentText())*1e9)
            S21 = self.df_5[self.df_5.Frequency == float(desFreq)]
            D1S21 = S21[S21.Distancia == float(D1)].S21.values[0]
            D2S21 = S21[S21.Distancia == float(D2)].S21.values[0]
            D1 = float(D1)/100
            D2 = float(D2)/100
            perda = self.funcao_perda(desFreq/1e9)
           
            
            D1S21W = dBm2W(D1S21 - perda)
            D2S21W = dBm2W(D2S21 - perda)
            
            lmbda = 3e8/desFreq
            G1 = np.sqrt(D1S21W)*(4*np.pi*float(D1))/lmbda
            G2 = np.sqrt(D2S21W)*(4*np.pi*float(D2))/lmbda
            
            
            if float(D1) != 0.0 and float(D2) != 0.0 and D1 != D2:
                G1dB = 10*np.log10(G1)
                G2dB = 10*np.log10(G2)
                if self.scat:
                    print('Tem Scat', self.scat)
                    self.scat.remove()
                    self.approx.pop(0).remove()
                    self.canvas_4.draw_idle()
                self.scat = self.ax_4.scatter([float(D1)*100, float(D2)*100], [G1dB, G2dB])
                print(self.scat)
                self.canvas_4.draw_idle()
                #print(f'\nOrigi = {D1S21}, perda = {perda}, S21 = {D1S21 - perda}, S21W = {D1S21W}, dist = {D1}, ganho = {G1dB}')
                #print(f'Origi = {D2S21}, perda = {perda},S21 = {D2S21 - perda}, S21W = {D2S21W}, dist = {D2}, ganho = {G2dB}')
                kmax = [0.1, 1000]
                try:
                    sol = root_scalar(func, method='toms748', bracket = kmax)
                    k = sol.root
                    Gcd = G1dB/(1-math.exp(-k*float(D1)))
                    print(f'k = {k}, Gcd = {Gcd}')
                    x2 = np.arange(self.dists_3[0]/100, self.dists_3[-1]/100, 0.10)
                    self.approx = self.ax_4.plot(x2*100, Alfredo(k, Gcd, x2), label='Alfredo')
                    self.line_Gain_Output.setText(f'{round(Gcd, 2)} dB')
                except:
                    pass
                    QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Estimativa Erro"),
                                              QtWidgets.qApp.tr("Não foi possível achar uma solução para k = [0.1, 1000]"),
                                              QtWidgets.QMessageBox.Ok)
                

        
    def empty_plot(self):
        self.ax.cla()
        self.ax.set_theta_zero_location("N")
        self.ax.autoscale(enable = False)
        self.ax.set_rmax(-15)
        self.ax.set_rmin(-45)
        #print('zerei')

    def clear_plot(self):
        self.empty_plot()
        #print('to tentando limpar')
        self.canvas.draw_idle()

    def clear_plot_2(self):
        self.ax_2.cla()
        self.canvas_2.draw_idle()

    def clear_plot_3(self):
        self.ax_4.cla()
        self.canvas_4.draw_idle()

    def what_plot(self):
        self.whatPlot = str(self.cb_what_plot.currentText())

    def what_plot_2(self):
        self.clear_plot_2()
        self.whatPlot2 = str(self.cb_what_plot_2.currentText())
        if self.whatPlot2 == 'Distância':
            self.cb_frequency_2.clear()
            self.cb_frequency_2.addItems([str(dist) for dist in self.dists])
        elif self.whatPlot2 == 'Frequência':
            self.cb_frequency_2.clear()
            self.cb_frequency_2.addItems([str(freq) for freq in self.freqs])

    def update_plot(self):
        if self.folderLoaded_2 == False:
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Open Folder"),
                                                  QtWidgets.qApp.tr("Arquivos do Diagrama de Radiação não carregados!"),
                                                  QtWidgets.QMessageBox.Ok)
        else:
            self.whatPlot = str(self.cb_what_plot.currentText())
            desFreq = round(float(self.cb_frequency_4.currentText())*1e9)
            theta = np.deg2rad(self.df[self.df.Frequency == float(desFreq)].Angle)
            r1 = self.df.loc[self.df['Frequency'] == float(desFreq)]
            if self.lossLoaded_perda:
                aux = self.df_perda[self.df_perda['Frequency'] == float(desFreq)]
                aux = aux.iat[0,1]
                r1 = r1-aux
            r = r1[self.whatPlot].clip(lower = self.ax.get_rmin())

            if not self.hold.isChecked():
                #//pass
                self.empty_plot()

            if self.normalize.isChecked():
                try:
                    self.ax.autoscale(enable=False)
                    rMax = max(r)
                    r = r - rMax
                    rMin = min(r)
                    self.ax.set_rmax(0)
                    self.ax.set_rmin(rMin)
                except:
                    pass
            else:
                self.ax.autoscale(enable = False)
                self.ax.set_rmax(-15)
                self.ax.set_rmin(-45)

            #//mpl#datacursor.remove()
            line_1, = self.ax.plot(theta, r, label = (str(desFreq/1e9) + ' GHz' + f' - {"%.2f" % max(r)}dB'))
            self.ax.set_xticks(np.pi/180. * np.linspace(0,  360, 24, endpoint=False))
            self.ax.set_thetalim(0, 2*np.pi)
            #self.ax.set_xticks(np.pi/180. * np.linspace(180,  -180, 24, endpoint=False))

            self.ax.set_title(self.folderTitle)
            legenda = self.ax.legend(bbox_to_anchor=(0, 1.02, 1, .102), borderaxespad=0, loc="right")
            legenda.set_draggable(True)
            #datacursor(line_1, formatter='x: {x:.2f}\ny: {y:.2f}'.format)
            self.canvas.draw_idle()

    def update_plot_2(self):
        self.whatPlot2 = str(self.cb_what_plot_2.currentText())
        if self.whatPlot2 == 'Distância':
            Y = self.df_2[self.df_2.Distancia == float(self.cb_frequency_2.currentText())].S21
            #self.ax_2.set_xlabel('Distância')
            xlabel = 'Frequência [GHz]'
            var = 'd'
            unit = 'cm'
            X = self.freqs
        elif self.whatPlot2 == 'Frequência':
            desFreq = round(float(self.cb_frequency_2.currentText())*1e9)
            tempY = self.df_2[self.df_2.Frequency == float(desFreq)].S21.tolist()
            tempX = self.dists
            var = 'f'
            unit = 'GHz'
            xlabel = 'Distância [cm]'
            X, Y, func = graficoBunito(tempX, tempY, tempX.size*3)
            #X = self.dists
            #Y = self.df_2[self.df_2.Frequency == float(self.desFreq)].S21.tolist()
            #print(X, len(X), Y, len(Y))
            #print(tempX.size)


        if not self.hold_2.isChecked():
            self.ax_2.cla()

        self.ax_2.set_ylabel('|S21| [dB]')
        self.ax_2.set_xlabel(xlabel)
        line_ax2_1, = self.ax_2.plot(X, Y, label = f'{self.cb_frequency_2.currentText()} {unit}')
        legenda_2 = self.ax_2.legend(bbox_to_anchor=(0, 1.02, 1, .102), borderaxespad=0, loc="best")
        legenda_2.set_draggable(True)
        self.canvas_2.draw_idle()

    def update_plot_3(self):
        if self.folderLoaded == False:
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Open Folder"),
                                                  QtWidgets.qApp.tr("Arquivos de Distância não carregados!"),
                                                  QtWidgets.QMessageBox.Ok)
        elif self.lossLoaded == False:
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Open Folder"),
                                                  QtWidgets.qApp.tr("Arquivo de Perdas não carregado!"),
                                                  QtWidgets.QMessageBox.Ok)
        else:
            if not self.hold_3.isChecked():
                #//pass
                self.ax_4.cla()
            desFreq = round(float(self.cb_frequency_3.currentText())*1e9)
            tempsY = self.df_5[self.df_5.Frequency == float(desFreq)].S21.tolist()
            #print(self.df_5[self.df_5.Frequency == float(desFreq)])
            perda = self.funcao_perda(desFreq/1e9)
            ganho = []
            #print(tempsY, f'Perda = {perda}', self.dists_3, desFreq)

            for tempY, dist in zip(tempsY[1:], self.dists_3[1:]):
                aux1 = tempY - perda
                P = 10**((aux1)/10)
                lmda = 3e8/(desFreq)
                fim = math.sqrt(P) * (4*math.pi*(dist/100))/lmda
                fim = 10*math.log(fim, 10)
                ganho.append(fim)
                #print(f'Origin = {tempY} perda = {perda}, S21 = {aux1}, S21W = {P}, dist = {dist} , ganho = {fim}')

            #print(ganho)

            #self.ax_4.plot(self.dists_3, tempY)
            self.ax_4.set_ylabel('Ganho [dB]')
            self.ax_4.set_xlabel('Distância [cm]')
            xnew, ynew, _ = graficoBunito(self.dists_3[1:], ganho, self.dists_3[1:].size*3)
            self.ax_4.plot(xnew, ynew, label = f'{desFreq/1e9} GHz')
            #self.ax_4.plot(self.dists_3[1:], ganho, label = f'{desFreq/1e9} GHz')
            legenda_4 = self.ax_4.legend(bbox_to_anchor=(0, 1.02, 1, .102), borderaxespad=0, loc="right")
            legenda_4.set_draggable(True)

            self.canvas_4.draw_idle()

    def load_csv(self):
        root = tk.Tk()
        root.withdraw()
        self.folder = filedialog.askdirectory()
        try:
            self.folderTitle = self.folder.split('/')[-1]
            self.folderPath.setText(self.folder)
            files = glob.glob(self.folder + '//*.CSV')
            if files[-1].replace(self.folder + '\\','').replace('.CSV', '')[-3:] == '360':
                complete = True
            else:
                complete = False
            #//print(complete)
            self.df= pd.DataFrame()
            self.folderLoaded_2 = True
            for file in files:
                tempFile = pd.read_csv(file, header=2, engine='python')
                angle = file.replace(self.folder + '\\','').replace('.CSV', '')[-3:]
                if angle.isdigit():
                    tempFile['Angle'] = float(angle)
                    self.df = self.df.append(tempFile, ignore_index=True, sort=False)
                if angle == '000' and not complete:
                    aux3 = tempFile.copy(deep = True)
                    aux3.Angle = 360.0
                    self.df = self.df.append(aux3, ignore_index = True, sort=False)

            #//print(self.df['Angle'].unique())
            self.df.rename(columns = {self.df.columns[1]: 'S21', self.df.columns[2]: 'Phase'}, inplace = True)
            self.df.sort_values(['Frequency', 'Angle'], inplace = True)
            self.df.reset_index(drop=True, inplace=True)
            self.df= self.df[['Frequency', 'Angle', 'S21', 'Phase']]
            freqs = self.df.Frequency.unique()/1e9
            #//print(self.df['Angle'].unique())

            self.cb_frequency_4.clear()
            self.cb_frequency_4.addItems([str(freq) for freq in freqs])

            self.cb_what_plot.clear()
            self.cb_what_plot.addItems(self.df.columns[2:])

            #//self.clear_plot()
        except:
            pass
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Open Folder"),
                                              QtWidgets.qApp.tr("Erro ao abrir Arquivos!"),
                                              QtWidgets.QMessageBox.Ok)

    def load_csv_2(self):
        root = tk.Tk()
        root.withdraw()
        self.folder_2 = filedialog.askdirectory()
        try:
            self.folderTitle_2 = self.folder_2.split('/')[-1]
            self.folderPath_2.setText(self.folder_2)
            files_2 = glob.glob(self.folder_2 + '//*.CSV')
            #print(files_2)
            self.df_2= pd.DataFrame()
            for file in files_2:
                tempFile = pd.read_csv(file, header=2, engine='python')
                dist = file.replace(self.folder_2 + '\\','').replace('.CSV', '')[-3:]
                #print(dist)
                if dist.isdigit():
                    tempFile['Distancia'] = float(dist)
                    self.df_2 = self.df_2.append(tempFile, ignore_index=True, sort=False)

            self.df_2.rename(columns = {self.df_2.columns[1]: 'S21', self.df_2.columns[2]: 'Phase'}, inplace = True)
            self.df_2.sort_values(['Frequency', 'Distancia'], inplace = True)
            self.df_2.reset_index(drop=True, inplace=True)
            self.df_2= self.df_2[['Frequency', 'S21', 'Distancia', 'Phase']]
            self.freqs = self.df_2.Frequency.unique()/1e9
            self.dists = self.df_2.iloc[:, 2].unique()
            self.cb_what_plot_2.clear()
            self.cb_what_plot_2.addItems(['Frequência', 'Distância'])

            self.cb_frequency_2.clear()
            self.cb_frequency_2.addItems([str(freq) for freq in self.freqs])
        except:
            pass
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Open Folder"),
                                              QtWidgets.qApp.tr("Erro ao abrir Arquivos!"),
                                              QtWidgets.QMessageBox.Ok)

    def load_csv_3(self):
        root = tk.Tk()
        root.withdraw()
        self.folder_3 = filedialog.askdirectory()
        try:
            self.folderTitle_3 = self.folder_3.split('/')[-1]
            self.folderPath_5.setText(self.folder_3)
            files_3 = glob.glob(self.folder_3 + '//*.CSV')
            #print(files_2)
            self.df_5= pd.DataFrame()
            for file in files_3:
                tempFile = pd.read_csv(file, header=2, engine='python')
                dist = file.replace(self.folder_3 + '\\','').replace('.CSV', '')[-3:]
                #print(dist)
                if dist.isdigit():
                    tempFile['Distancia'] = float(dist)
                    self.df_5 = self.df_5.append(tempFile, ignore_index=True, sort=False)

            self.df_5.rename(columns = {self.df_5.columns[1]: 'S21', self.df_5.columns[2]: 'Phase'}, inplace = True)
            self.df_5.sort_values(['Frequency', 'Distancia'], inplace = True)
            self.df_5.reset_index(drop=True, inplace=True)
            self.df_5= self.df_5[['Frequency', 'S21', 'Distancia', 'Phase']]
            self.freqs_3 = self.df_5.Frequency.unique()/1e9
            self.dists_3 = self.df_5.iloc[:, 2].unique()

            self.cb_frequency_3.clear()
            self.cb_frequency_3.addItems([str(freq) for freq in self.freqs_3])
            
            self.cb_Gain_1.clear()
            self.cb_Gain_1.addItems([str(freq) for freq in self.dists_3])
            
            self.cb_Gain_2.clear()
            self.cb_Gain_2.addItems([str(freq) for freq in self.dists_3])
            #print(self.dists_3)
            #print(self.freqs_3)

            self.folderLoaded = True
        except:
            pass
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Open Folder"),
                                              QtWidgets.qApp.tr("Erro ao abrir Arquivos!"),
                                              QtWidgets.QMessageBox.Ok)

    def save_csv(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","",".xlsx", options=options)
        if fileName:
            writer = pd.ExcelWriter(fileName + '.xlsx')
            self.df.to_excel(writer, sheet_name='All', columns = self.df.columns.tolist())
            writer.save()
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Save XLSX"),
                                              QtWidgets.qApp.tr("File Saved"),
                                              QtWidgets.QMessageBox.Ok)

    def save_csv_2(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","",".xlsx", options=options)
        if fileName:
            writer = pd.ExcelWriter(fileName + '.xlsx')
            self.df_2.to_excel(writer, sheet_name='All', columns = self.df_2.columns.tolist())
            writer.save()
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Save XLSX"),
                                              QtWidgets.qApp.tr("File Saved"),
                                              QtWidgets.QMessageBox.Ok)

    def save_csv_3(self):
        '''
        for freq in self.freqs_3:
            temps = self.df_5[self.df_5.Frequency == float(desFreq)].S21.tolist()
            for temp, dist in zip(self.temps, self.dists_3[1:]):
                aux1 = tempY - perda
                P = 10**((aux1)/10)
                lmda = 3e8/(desFreq)
                fim = math.sqrt(P) * (4*math.pi*(dist/100))/lmda
                fim = 10*math.log(fim, 10)
                ganho.append(fim)
                #print(tempY, perda, desFreq, dist, fim)
                '''
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","",".xlsx", options=options)
        if fileName:
            writer = pd.ExcelWriter(fileName + '.xlsx')
            self.df_5.to_excel(writer, sheet_name='All', columns = self.df_5.columns.tolist())
            writer.save()
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Save XLSX"),
                                              QtWidgets.qApp.tr("File Saved"),
                                              QtWidgets.QMessageBox.Ok)

    def load_csv_file(self):
        root = tk.Tk()
        root.withdraw()
        self.fileName_3 = filedialog.askopenfile()
        self.folderPath_3.setText(self.fileName_3.name)
        self.df_3= pd.read_csv(self.fileName_3, header=2, engine='python')
        #print(self.df_3.head())
        freq_3 = self.df_3.iloc[:,0]/1e9
        loss = self.df_3.iloc[:,1]

        x, y, funcao = graficoBunito(freq_3, loss, freq_3.size*3)

        self.ax_3.cla()

        line3, = self.ax_3.plot(freq_3, loss, label = 'Perdas nos cabos e adaptadores')
        #line5, = self.ax_3.plot(x, y, label = 'Interpolação')
        self.ax_3.autoscale(enable = True)
        self.ax_3.set_xlabel('Frequência [GHz]')
        self.ax_3.set_ylabel('|S21| [dB]')
        legenda_3 = self.ax_3.legend(bbox_to_anchor=(0, 1.02, 1, .102), borderaxespad=0, loc="right")
        legenda_3.set_draggable(True)

        #datacursor(line3, formatter='x: {x:.0f}\ny: {y:.0f}'.format)

        self.canvas_3.draw_idle()

    def load_csv_file_2(self):
        root = tk.Tk()
        root.withdraw()
        self.fileName_4 = filedialog.askopenfile()
        try:
            self.df_4= pd.read_csv(self.fileName_4, header=2, engine='python')
            self.folderPath_6.setText(self.fileName_4.name)
            #print(self.fileName_4)
            self.freq_loss = self.df_4.iloc[:,0]/1e9
            self.loss = self.df_4.iloc[:,1]

            nada, fon, self.funcao_perda = graficoBunito(self.freq_loss, self.loss, self.freq_loss.size*3)

            self.lossLoaded = True
        except:
            pass
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Open Folder"),
                                              QtWidgets.qApp.tr("Erro ao abrir Arquivos!"),
                                              QtWidgets.QMessageBox.Ok)

    def load_csv_file_3(self):
        root = tk.Tk()
        root.withdraw()
        self.fileName_perda = filedialog.askopenfile()
        try:
            self.df_perda= pd.read_csv(self.fileName_perda, header=2, engine='python')
            self.folderPath_4.setText(self.fileName_perda.name)
            #print(self.fileName_4)
            self.freq_loss_perda = self.df_perda.iloc[:,0]/1e9
            self.loss_perda = self.df_perda.iloc[:,1]

            self.lossLoaded_perda = True

        except:
            pass
            QtWidgets.QMessageBox.information(None, QtWidgets.qApp.tr("Open Folder"),
                                             QtWidgets.qApp.tr("Erro ao abrir Arquivo!"),
                                             QtWidgets.QMessageBox.Ok)
  
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FrequencyPlotter"))
        self.label.setText(_translate("MainWindow", "Medições de Distância:"))
        self.label_2.setText(_translate("MainWindow", "Medições de Perda:"))
        self.browseFolder.setText(_translate("MainWindow", "Browse"))
        self.browseFolder_4.setText(_translate("MainWindow", "Browse"))
        self.label_freq.setText(_translate("MainWindow", "Frequências [GHz]:"))
        self.label_what_plot.setText(_translate("MainWindow", "Parâmetro:"))
        self.saveCsv.setText(_translate("MainWindow", "Salvar CSV"))
        self.normalize.setText(_translate("MainWindow", "Normalizar"))
        self.hold.setText(_translate("MainWindow", "Hold"))
        self.clearBtn_2.setText(_translate("MainWindow", "Limpar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.diagRad), _translate("MainWindow", "Diagrama de Radiação"))
        self.label_13.setText(_translate("MainWindow", "Medição de Distância:"))
        self.browseFolder_2.setText(_translate("MainWindow", "Browse"))
        self.label_14.setText(_translate("MainWindow", "Frequências [GHz]:"))
        self.label_15.setText(_translate("MainWindow", "Available Values:"))
        self.saveCsv_2.setText(_translate("MainWindow", "Salvar CSV"))
        self.normalize_2.setText(_translate("MainWindow", "Normalize"))
        self.hold_2.setText(_translate("MainWindow", "Hold"))
        self.clearBtn_3.setText(_translate("MainWindow", "Limpar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dist), _translate("MainWindow", "Distância"))
        self.label_16.setText(_translate("MainWindow", "File:"))
        self.browseFolder_3.setText(_translate("MainWindow", "Browse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.perdas), _translate("MainWindow", "Perdas"))
        self.label_3.setText(_translate("MainWindow", "Medições de Distância:"))
        self.label_4.setText(_translate("MainWindow", "Medições de Perda:"))
        self.label_freq_2.setText(_translate("MainWindow", "Frequências [GHz]:"))
        self.browseFolder_6.setText(_translate("MainWindow", "Browse"))
        self.browseFolder_5.setText(_translate("MainWindow", "Browse"))
        self.saveCsv_3.setText(_translate("MainWindow", "Salvar CSV"))
        self.GainCheckBox.setText(_translate("MainWindow", "Estimar Ganho"))
        self.label_5.setText(_translate("MainWindow", "Medição 1:"))
        self.label_6.setText(_translate("MainWindow", "Medição 2:"))
        self.label_7.setText(_translate("MainWindow", "Ganho Estimado:"))
        self.normalize_3.setText(_translate("MainWindow", "Normalizar"))
        self.hold_3.setText(_translate("MainWindow", "Hold"))
        self.clearBtn_4.setText(_translate("MainWindow", "Limpar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Ganho"))
        self.label_8.setText(_translate("MainWindow", "Medição 1"))
        self.label_9.setText(_translate("MainWindow", "Medição 2:"))
        self.estimate_gain_1_btn.setText(_translate("MainWindow", "Browse"))
        self.estimate_gain_2_btn.setText(_translate("MainWindow", "Browse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Estimativa de Ganho"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
       
