from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtGui import QImage, QPixmap

import os,sys,cv2

inputPath = ""
outputPath = ""
picList = []
cacheList = []
selectCache = {}
selectChoices = ["Class1","Class2","Class3","Class4"]

CacheCapacity = 5

debug = 1

def init():
	global scene
	scene = QtWidgets.QGraphicsScene()
	scene.setSceneRect(0, 0, 460, 800)

	global inputPath,outputPath,picList
	
	if debug == 0:
		inputPath = input("inputPath")
		outputPath = input("outputPath")
	else:
		inputPath = "./input"
		outputPath = "./output"

	if os.path.exists(inputPath) == False:
		os.mkdir(inputPath)
	if os.path.exists(outputPath) == False:
		os.mkdir(outputPath)
	
	fileList = os.listdir(inputPath)
	picList = []
	for fileName in fileList:
		if fileName.find(".png") != -1:
			picList.append(fileName)
	for dirname in selectChoices:
		if os.path.exists(outputPath+"/"+dirname) == False:
			os.mkdir(outputPath+"/"+dirname)
	showCache()
	showImageAll()

def showCache():
	ui.bar_CacheCount.setValue(len(cacheList))
	ui.textBrowser_CacheCount.append(str(len(cacheList))+"/"+str(CacheCapacity)+" Cached")
	
def showImageAll():
	ui.imageInf.append("--------------------")
	ui.imageInf.append("imageFilename:"+picList[0])
	image = cv2.imread(inputPath+"/"+picList[0])
	ui.imageInf.append("size:"+str(image.shape[1])+" * "+str(image.shape[0]))
	showImage(image)

def showImage(image):
	scene.clear()
	image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	qimage = QImage(image_RGB.data, image_RGB.shape[1], image_RGB.shape[0], image_RGB.shape[1]*3, QImage.Format_RGB888)
	zoomChange = min(ui.graphicsView_image.width()/image.shape[1], ui.graphicsView_image.height()/image.shape[0])
	imw, imh = int(image.shape[1]*zoomChange), int(image.shape[0]*zoomChange)
	pix = QPixmap(qimage).scaled(imw,imh)
	scene.addPixmap(pix)
	ui.graphicsView_image.setScene(scene)

def writeCache(picName):
	select = selectCache.pop(picName)
	os.replace(inputPath+"/"+picName,outputPath+"/"+selectChoices[select]+"/"+picName)

def writeAllCache():
	global cacheList
	for picName in cacheList:
		writeCache(picName)
	cacheList = []
	showCache()

def nextPic():
	global picList,cacheList,image_now
	if len(cacheList) < CacheCapacity:
		cacheList.append(picList.pop(0))
	else:
		writeCache(cacheList.pop(0))
		cacheList.append(picList.pop(0))
	if len(picList) > 0:
		showCache()
		showImageAll()

def events_select(select):
	global selectCache
	if len(picList) > 0:
		selectCache[picList[0]] = select
		nextPic()
	else:
		ui.imageInf.append("--------------------")
		ui.imageInf.append("All Picture Done")

def event_Class1():
	events_select(0)
def event_Class2():
	events_select(1)
def event_Class3():
	events_select(2)
def event_Class4():
	events_select(3)

def event_Back():
	if len(cacheList) > 0:
		picList.insert(0,cacheList.pop())
		showCache()
		showImageAll()

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(894, 880)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.button_Back = QtWidgets.QPushButton(self.centralwidget)
		self.button_Back.setGeometry(QtCore.QRect(520, 510, 101, 81))
		self.button_Back.setObjectName("button_Back")
		self.Select = QtWidgets.QGroupBox(self.centralwidget)
		self.Select.setGeometry(QtCore.QRect(500, 600, 381, 221))
		self.Select.setObjectName("Select")
		self.pushButton_Class1 = QtWidgets.QPushButton(self.Select)
		self.pushButton_Class1.setGeometry(QtCore.QRect(20, 20, 101, 81))
		self.pushButton_Class1.setObjectName("pushButton_Class1")
		self.pushButton_Class2 = QtWidgets.QPushButton(self.Select)
		self.pushButton_Class2.setGeometry(QtCore.QRect(20, 120, 101, 81))
		self.pushButton_Class2.setObjectName("pushButton_Class2")
		self.pushButton_Class3 = QtWidgets.QPushButton(self.Select)
		self.pushButton_Class3.setGeometry(QtCore.QRect(140, 120, 101, 81))
		self.pushButton_Class3.setObjectName("pushButton_Class3")
		self.pushButton_Class4 = QtWidgets.QPushButton(self.Select)
		self.pushButton_Class4.setGeometry(QtCore.QRect(260, 120, 101, 81))
		self.pushButton_Class4.setObjectName("pushButton_Class4")
		self.graphicsView_image = QtWidgets.QGraphicsView(self.centralwidget)
		self.graphicsView_image.setGeometry(QtCore.QRect(10, 10, 471, 811))
		self.graphicsView_image.setObjectName("graphicsView_image")
		self.imageInf = QtWidgets.QTextBrowser(self.centralwidget)
		self.imageInf.setGeometry(QtCore.QRect(520, 10, 341, 481))
		self.imageInf.setObjectName("imageInf")
		self.Button_WriteCache = QtWidgets.QPushButton(self.centralwidget)
		self.Button_WriteCache.setGeometry(QtCore.QRect(790, 510, 75, 23))
		self.Button_WriteCache.setObjectName("Button_WriteCache")
		self.bar_CacheCount = QtWidgets.QProgressBar(self.centralwidget)
		self.bar_CacheCount.setGeometry(QtCore.QRect(640, 570, 221, 23))
		self.bar_CacheCount.setProperty("value", 0)
		self.bar_CacheCount.setObjectName("bar_CacheCount")
		self.textBrowser_CacheCount = QtWidgets.QTextBrowser(self.centralwidget)
		self.textBrowser_CacheCount.setGeometry(QtCore.QRect(640, 530, 131, 31))
		self.textBrowser_CacheCount.setObjectName("textBrowser_CacheCount")
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 894, 23))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)


		self.pushButton_Class1.clicked.connect(event_Class1)
		self.pushButton_Class2.clicked.connect(event_Class2)
		self.pushButton_Class3.clicked.connect(event_Class3)
		self.pushButton_Class4.clicked.connect(event_Class4)
		self.bar_CacheCount.setRange(0,CacheCapacity)
		self.button_Back.clicked.connect(event_Back)
		self.Button_WriteCache.clicked.connect(writeAllCache)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.button_Back.setText(_translate("MainWindow", "Back"))
		self.Select.setTitle(_translate("MainWindow", "GroupBox"))
		self.pushButton_Class1.setText(_translate("MainWindow", "Class1"))
		self.pushButton_Class2.setText(_translate("MainWindow", "Class2"))
		self.pushButton_Class3.setText(_translate("MainWindow", "Class3"))
		self.pushButton_Class4.setText(_translate("MainWindow", "Class4"))
		self.Button_WriteCache.setText(_translate("MainWindow", "WriteCache"))	


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	init()
	sys.exit(app.exec_())
