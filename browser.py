import os
import sys
try:
    from PyQt5.uic import loadUi
    from PyQt5 import QtWidgets, QtCore, QtGui
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView, QWebEnginePage as QWebPage
except ImportError as e:
    with open(os.getcwd()+"/log.txt", "w") as file:
        file.write(os.popen(f"pip install -r {os.getcwd()}/requirements.txt").read())
    try:
        from PyQt5.uic import loadUi
        from PyQt5 import QtWidgets, QtCore
        from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView, QWebEnginePage as QWebPage
    except ImportError as e:
        print("[EXCEPTION] Something has gone wrong. Please provide requirements.txt before running again.")
        exit

class window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        loadUi(os.getcwd()+"\\sample.ui", self)
    
        self.tabs = []
        self.webViews = []

        self.insertTab()
        self.updateUrl()
        
        self.tabWidget.currentChanged.connect(self.updateUrl)
        self.webViews[self.tabWidget.currentIndex()].urlChanged.connect(self.updateUrl)
        self.webViews[self.tabWidget.currentIndex()].loadFinished.connect(self.updateUrl)
        
        self.btBack.clicked.connect(self.back)
        self.btForward.clicked.connect(self.forward)
        self.btReload.clicked.connect(self.reload)
        self.btHome.clicked.connect(self.home)

        self.txUrl.returnPressed.connect(self.goUrl)
        self.btGoUrl.clicked.connect(self.goUrl)
        self.btInsert.clicked.connect(self.insertTab)
        self.btDelete.clicked.connect(self.deleteTab)

    def home(self):
        self.webViews[self.tabWidget.currentIndex()].setUrl(QtCore.QUrl("https://www.google.com"))
        self.updateUrl()
    def reload(self):
        self.webViews[self.tabWidget.currentIndex()].reload()
        self.updateUrl()
    def forward(self):
        self.webViews[self.tabWidget.currentIndex()].forward()
    def back(self):
        self.webViews[self.tabWidget.currentIndex()].back()

    def goUrl(self):
        url = str(self.txUrl.text())
        # print(url.startswith("https://"))
        
        if url.count(".") == 0:
            url = "https://www.google.com/search?q=" + url
        if url.startswith("https://") is not True: url = "https://" + url
        self.webViews[self.tabWidget.currentIndex()].setUrl(QtCore.QUrl(url))

    def updateUrl(self):
        print(self.tabWidget.currentIndex())

        url = self.webViews[self.tabWidget.currentIndex()].url().toString()
        self.txUrl.setText(url)
        name = self.webViews[self.tabWidget.currentIndex()].title()
        if name=="":
            name = "Loading..."
        self.tabWidget.setTabText(self.tabWidget.currentIndex(), name)
    
    def insertTab(self):
        self.tabs.append(QtWidgets.QWidget())
        self.webViews.append(QWebView(self.tabs[-1]))
        self.webViews[-1].setGeometry(QtWidgets.QDesktopWidget().screenGeometry())
        self.webViews[-1].setUrl(QtCore.QUrl("https://www.google.com/"))
        self.tabWidget.addTab(self.tabs[-1], "www.google.com")
        
        self.arangeGeometry()
        self.btDelete.setText(str(len(self.tabs)))
        self.tabWidget.setCurrentIndex(len(self.tabs) - 1)
    
    def deleteTab(self):
        if len(self.tabs) > 1:
            self.tabs.pop(self.tabWidget.currentIndex())
            self.webViews.pop(self.tabWidget.currentIndex())
            self.tabWidget.removeTab(self.tabWidget.currentIndex())
            
            self.btDelete.setText(str(len(self.tabs)))
        else:
            self.btDelete.setText("!")

    def arangeGeometry(self):
        size = self.size()
        # print(size)
        for i in range(len(self.webViews)):
            self.webViews[i].resize(size)
            
    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.arangeGeometry()
    
def app():
    app=QtWidgets.QApplication(sys.argv)
    win=window()
    win.show()
    sys.exit(app.exec_())
app()