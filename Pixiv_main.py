# -*- coding: utf-8 -*-
# @Time    : 2020/7/29 14:28
# @Author  : kjleo
# @Software: PyCharm
# @E-mail  ：2491461491@qq.com

import sys, multiprocessing.dummy, random, string, tkinter, os

from Pixiv_main_ui import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PIL import Image
from PyQt5 import QtWidgets
from PictureDownload import Down

class Ui_Main(QtWidgets.QMainWindow, Ui_MainWindow):
    bar_count = 0

    def __init__(self, api):
        super(Ui_Main, self).__init__()
        self.mode = {1: "square_medium", 2: "medium", 3: "large", 4: "large"}
        self.setupUi(self)
        self.type2 = 1
        self.api = api
        self.pushButton.clicked.connect(self.show_rank)
        self.model = QStandardItemModel(30, 5)
        self.model.setHorizontalHeaderLabels(["插画名称", "插画id", "插画张数", "下载进度", "速度kb/s"])
        self.tableView.setModel(self.model)
        self.pushButton_2.clicked.connect(self.next)
        self.next_url = ""
        self.comboBox.addItem("日榜_R18")
        self.comboBox.addItem("周榜_R18")
        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.generatemenu)
        self.comboBox_2.currentIndexChanged.connect(self.set_type)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.doubleClicked.connect(self.show_pic)
        palette = QPalette()
        pix = QPixmap(":pic/back.jpg")
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)
        self.setWindowIcon(QIcon(":pic/Roi.ico"))
        screen = tkinter.Tk()
        self.screen_x = screen.winfo_screenwidth()
        self.screen_y = screen.winfo_screenheight()
        self.type = 1
        self.showimgs = []
        self.pushButton_3.clicked.connect(self.recommened)
        self.pushButton_4.clicked.connect(self.search)
        self.id = 0
        self.comboBox.currentTextChanged.connect(self.change)

    def change(self):
        self.id = self.comboBox.currentIndex()
        print(self.id)

    def search(self):
        text = self.plainTextEdit.toPlainText()
        self.thread4 = FindThread(self.api, text)
        self.thread4.dic.connect(self.show_search)
        self.thread4.start()

    def show_search(self, rank):
        self.type2 = 2
        self.tableView.clearSpans()
        self.next_url = rank["next_url"]
        self.illusts = rank["illusts"]
        self.model = QStandardItemModel(len(self.illusts), 5)
        self.model.setHorizontalHeaderLabels(["插画名称", "插画id", "插画张数", "下载进度", "速度kb/s"])
        self.tableView.setModel(self.model)
        for row in range(len(self.illusts)):
            column = 0
            item = QStandardItem(self.illusts[row]["title"])
            self.model.setItem(row, column, item)
            column += 1
            item = QStandardItem(str(self.illusts[row]["id"]))
            self.model.setItem(row, column, item)
            column += 1
            item = QStandardItem(str(self.illusts[row]["page_count"]))
            self.model.setItem(row, column, item)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def recommened(self):
        self.thread3 = RecommendedThread(self.api)
        self.thread3.dic.connect(self.set_re)
        self.thread3.start()

    def set_re(self, rank):
        self.type2 = 3
        self.tableView.clearSpans()
        self.next_url = rank["next_url"]
        self.illusts = rank["illusts"]
        self.model = QStandardItemModel(len(self.illusts), 5)
        self.model.setHorizontalHeaderLabels(["插画名称", "插画id", "插画张数", "下载进度", "速度kb/s"])
        self.tableView.setModel(self.model)
        for row in range(len(self.illusts)):
            column = 0
            item = QStandardItem(self.illusts[row]["title"])
            self.model.setItem(row, column, item)
            column += 1
            item = QStandardItem(str(self.illusts[row]["id"]))
            self.model.setItem(row, column, item)
            column += 1
            item = QStandardItem(str(self.illusts[row]["page_count"]))
            self.model.setItem(row, column, item)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_pic(self):
        row = self.tableView.currentIndex().row()
        url = self.illusts[row]["meta_pages"]
        id = self.illusts[row]["id"]
        if not url:
            url = self.illusts[row]["image_urls"][self.mode[self.type]]
        else:
            url = url[0]["image_urls"][self.mode[self.type]]
        self.showthred = ShowThread(id, url)
        self.showthred.success.connect(self.show_img)
        self.showthred.start()

    def show_img(self, image_path):
        self.showimgs.append(image_path)
        img = Image.open(image_path)
        imgSize = img.size  # 图片的长和宽
        len = imgSize[0]  # 图片的长边
        high = imgSize[1]  # 图片的短边
        while 1:
            len *= 0.99
            high *= 0.99
            if len < self.screen_x and high < self.screen_y:
                break
        size = QSize(int(len), int(high))
        img = QImage(image_path)
        pixImg = QPixmap.fromImage(img.scaled(size, Qt.IgnoreAspectRatio))
        self.label = QLabel()
        self.label.setScaledContents(True)
        self.label.move(300, 300)
        self.label.setPixmap(pixImg)
        self.label.show()

    def set_type(self):
        self.type = int(self.comboBox_2.currentText())

    def generatemenu(self, pos):
        for i in self.tableView.selectionModel().selection().indexes():  # 设置选中的单元格索引
            c = i.column()
            if c == 1:
                menu = QMenu()
                n1 = menu.addAction("下载")

                # 设置菜单显示的坐标位置为相对于单元格的位置
                screenpos = self.tableView.mapToGlobal(pos)
                a = menu.exec_(screenpos)
                id = self.tableView.currentIndex().data()
                index = self.tableView.currentIndex()
                row = self.tableView.currentIndex().row()
                index = index.sibling(row, 3)
                if a == n1:
                    urls = self.illusts[i.row()]["meta_pages"]
                    if not urls:
                        self.p_bar = QProgressBar(self)
                        self.tableView.setIndexWidget(index, self.p_bar)
                        self.lcd = QLCDNumber(self)
                        self.lcd.setSmallDecimalPoint(True)
                        self.lcd.setDigitCount(8)
                        index = index.sibling(row, 4)
                        self.tableView.setIndexWidget(index, self.lcd)
                        urls = self.illusts[i.row()]["image_urls"][self.mode[self.type]]
                        if self.type == 4:
                            urls = self.illusts[i.row()]["meta_single_page"]
                            urls = urls["original_image_url"]
                        self.thread2 = Down(int(id),row)
                        self.thread2.process.connect(self.set_process)
                        self.thread2.success.connect(self.success)
                        self.thread2.start()
                    else:
                        self.down = Down_Thread(self.api, urls, id, self.type)
                        self.down.success.connect(self.success)
                        self.down.start()
                else:
                    return

    def set_process(self, process, row, speed):
        index = self.tableView.currentIndex()
        index = index.sibling(row, 3)
        bar = self.tableView.indexWidget(index)
        bar.setValue(process)
        index = index.sibling(row, 4)
        lcd = self.tableView.indexWidget(index)
        lcd.display(speed)

    def success(self, s):
        wedge = QWidget()
        reply = QMessageBox.information(wedge, "消息", s, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == 16384:
            path = os.getcwd()
            os.system("start explorer " + str(path))

    def show_rank(self):
        mode = {0: "day", 1: "week", 2: "month", 3: "day_r18", 4: "week_r18"}
        self.thread = Rank_Thread(self.api, mode[self.id], 1)
        self.thread.success1.connect(self.set_table)
        self.thread.start()

    def next(self):
        if self.next_url == "":
            return
        next_qs = self.api.parse_qs(self.next_url)
        self.thread = Rank_Thread(self.api, next_qs, self.type2)
        self.thread.success1.connect(self.set_table)
        self.thread.success2.connect(self.show_search)
        self.thread.success3.connect(self.set_re)
        self.thread.start()

    def set_table(self, rank):
        self.type2 = 1
        self.tableView.clearSpans()
        self.next_url = rank["next_url"]
        self.illusts = rank["illusts"]
        self.model = QStandardItemModel(len(self.illusts), 5)
        self.model.setHorizontalHeaderLabels(["插画名称", "插画id", "插画张数", "下载进度", "速度kb/s"])
        self.tableView.setModel(self.model)
        for row in range(len(self.illusts)):
            column = 0
            item = QStandardItem(self.illusts[row]["title"])
            self.model.setItem(row, column, item)
            column += 1
            item = QStandardItem(str(self.illusts[row]["id"]))
            self.model.setItem(row, column, item)
            column += 1
            item = QStandardItem(str(self.illusts[row]["page_count"]))
            self.model.setItem(row, column, item)
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def closeEvent(self, event):
        for each in self.showimgs:
            os.remove(each)
        event.accept()


class Rank_Thread(QThread):
    success1 = pyqtSignal(dict)
    success2 = pyqtSignal(dict)
    success3 = pyqtSignal(dict)

    def __init__(self, api, url, type):
        super(Rank_Thread, self).__init__()
        self.url = url
        self.api = api
        self.type = type

    def run(self):
        if type(self.url) == str:
            rank = self.api.illust_ranking(mode=self.url)
            self.success1.emit(rank)
        elif self.type == 1:
            rank = self.api.illust_ranking(**self.url)
            self.success1.emit(rank)
        elif self.type == 2:
            rank = self.api.search_illust(**self.url)
            self.success2.emit(rank)
        elif self.type == 3:
            rank = self.api.illust_recommended(**self.url)
            self.success3.emit(rank)


class Down_Thread(QThread):
    success = pyqtSignal(str)

    def __init__(self, api, urls, id, type=3):
        super(Down_Thread, self).__init__()
        self.urls = urls
        self.api = api
        self.id = id
        mode = {1: "square_medium", 2: "medium", 3: "large", 4: "original", 5: "single"}
        self.type = mode[type]
        self.pool = multiprocessing.dummy.Pool()

    def run(self):
        i = 0
        if self.type == "single":
            url = self.urls["original_image_url"]
            self.thread2 = Down(self.id,row=0,url=url,sigle_url=True)
            self.thread2.start()
            self.thread2.join()
            i += 1
        else:
            ids = []
            for each in self.urls:
                s = self.id + '-' + str(i+1)
                ids.append(s)
                i += 1
            for Id in ids:
                self.thread2 = Down(Id, row=0)
                self.thread2.start()
            # self.pool.map(self.down, ids)
            # self.pool.close()
            # self.pool.join()
        s = "id:" + str(self.id) + "  下载成功" + str(i) + "张,是否打开文件夹"
        self.success.emit(s)

    def down(self, Id):
        self.thread2 = Down(Id,row=0)
        self.thread2.start()


class ShowThread(QThread):
    success = pyqtSignal(str)

    def __init__(self, id, url):
        super(ShowThread, self).__init__()
        self.id = id
        self.url = url

    def run(self):
        self.filename = (
                "".join(random.sample(string.ascii_letters + string.digits, 5)) + ".png"
        )
        self.thread2 = Down(self.id, row=0, url=self.url, sigle_url=True,Name=self.filename)
        self.thread2.start()
        self.thread2.success.connect(self.fun)


    def fun(self,s):
        self.success.emit(self.filename)


class RecommendedThread(QThread):
    dic = pyqtSignal(dict)

    def __init__(self, api):
        super(RecommendedThread, self).__init__()
        self.api = api

    def run(self):
        json_result = self.api.illust_recommended()
        self.dic.emit(json_result)


class FindThread(QThread):
    dic = pyqtSignal(dict)

    def __init__(self, api, text):
        super(FindThread, self).__init__()
        self.api = api
        self.text = text

    def run(self):
        json_result = self.api.search_illust(word=self.text)
        self.dic.emit(json_result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    api = ""
    window = Ui_Main(api)
    window.show()
    sys.exit(app.exec_())
