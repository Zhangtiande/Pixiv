# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Pixiv_log_in.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtWidgets, QtGui
import sys, os, Pixiv_main, base64, re
import pixivpy3
from pixivpy3 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

api = ByPassSniApi()
password = ""
username = ""


class QTitleButton(QPushButton):
    """
  新建标题栏按钮类
  """

    def __init__(self, *args):
        super(QTitleButton, self).__init__(*args)
        self.setFont(QFont("Webdings"))  # 特殊字体以不借助图片实现最小化最大化和关闭按钮
        self.setFixedWidth(40)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(362, 247)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 150, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setItalic(True)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 321, 111))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 362, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pixiv_log_in"))
        self.pushButton.setText(_translate("MainWindow", "log_in"))
        self.label.setText(_translate("MainWindow", "username"))
        self.label_2.setText(_translate("MainWindow", "password"))
        self.pushButton.setStyleSheet(
            """ 
                             QPushButton
                             {text-align : center;
                             background-color : white;
                             font: bold;
                             border-color: gray;
                             border-width: 2px;
                             border-radius: 10px;
                             padding: 6px;
                             height : 14px;
                             border-style: outset;
                             font : 14px;}
                             QPushButton:pressed
                             {text-align : center;
                             background-color : light gray;
                             font: bold;
                             border-color: gray;
                             border-width: 2px;
                             border-radius: 10px;
                             padding: 6px;
                             height : 14px;
                             border-style: outset;
                             font : 14px;}
                             """
        )
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.chebox = QCheckBox("记住密码", self)
        self.chebox.move(40, 180)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = e.globalPos() - self.pos()
            e.accept()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.m_drag = False

    def mouseMoveEvent(self, e):
        if Qt.LeftButton and self.m_drag:
            self.move(e.globalPos() - self.m_DragPosition)
            e.accept()

    def setCloseButton(self, bool):
        if bool == True:
            self._CloseButton = QTitleButton(b"\xef\x81\xb2".decode("utf-8"), self)
            self._CloseButton.setObjectName("CloseButton")
            self._CloseButton.setToolTip("关闭窗口")
            self._CloseButton.setMouseTracking(True)
            self._CloseButton.clicked.connect(self.close)


class Login_ui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Login_ui, self).__init__()
        global api
        self.flag = 1
        self.api = api
        self.setupUi(self)
        self.pushButton.clicked.connect(self.log_in)
        try:
            file = open("data", "rb")
            string = "".encode("utf-8")
            lis = file.readlines()
            for i in lis:
                string += i
            file.close()
            string = str(base64.decodebytes(string))
            username = re.findall("'username': '(.*?)',", string)
            password = re.findall("'password': '(.*?)'", string)
            self.lineEdit.setText(username[0])
            self.lineEdit_2.setText(password[0])
            self.chebox.setChecked(True)
        except:
            pass

    def log_in(self):
        global username, password
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if self.chebox.isChecked():
            data = {"username": username, "password": password}
            data = str(data)
            string = base64.encodebytes(data.encode("utf-8"))
            file = open("data", "wb+")
            file.write(string)
            file.close()
        self.thread = Login_Thread(username, password)
        self.thread.success.connect(self.log_sucess)
        self.thread.start()

    def log_sucess(self, flag):
        wedge = QWidget()
        if flag == 1:
            Ui_Main.show_rank()
            QMessageBox.information(wedge, "消息", "登录成功！", QMessageBox.Yes)
            print("sucess!")
            Ui_Main.show()
            self.close()
        else:
            QMessageBox.critical(wedge, "错误", "账号或密码错误，请重新输入!")


class Login_Thread(QThread):
    success = pyqtSignal(int)

    def __init__(self, username, password):
        super(Login_Thread, self).__init__()
        self.username = username
        self.password = password

    def run(self):
        global api
        api.require_appapi_hosts(hostname="public-api.secure.pixiv.net")
        api.set_accept_language("en-us")
        try:
            # api.login(self.username, self.password)
            api.auth(refresh_token='kkz9aS-vNcpLidtgxkOxPrS4Fs_rRzWhK-OwYcmwUp4')
            self.success.emit(1)
        except pixivpy3.utils.PixivError as e:
            print(e)
            self.success.emit(0)
        self.quit()


if __name__ == "__main__":  # 如果这个文件是主程序。
    path = os.getcwd()
    origion_path = path
    try:
        os.mkdir("Pixiv")
        path = path + "\Pixiv"
        os.chdir(path)
    except:
        path = path + "\Pixiv"
        os.chdir(path)
    app = QtWidgets.QApplication(sys.argv)
    window = Login_ui()
    palette1 = QtGui.QPalette()
    palette1.setColor(palette1.Background, QtGui.QColor(147, 224, 255))
    window.setPalette(palette1)
    window.setWindowTitle("Pixiv_login")
    window.setCloseButton(True)
    window.show()
    Ui_Main = Pixiv_main.Ui_Main(api)
    sys.exit(app.exec_())
