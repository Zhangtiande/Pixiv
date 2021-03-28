# -*- coding: utf-8 -*-
# @Time    : 2021/3/27 16:27
# @Author  : kjleo
# @Software: PyCharm
# @E-mail  ：2491461491@qq.com
import re
import time
from concurrent.futures.thread import *
from PyQt5.QtCore import *
import PyQt5.QtCore
import requests

results = []
length = 0

class Down(QThread):
    process = pyqtSignal(int, int, float)
    success = pyqtSignal(str)


    def __init__(self, Id, row, url = None, sigle_url=False,Name=None):
        super().__init__()
        if sigle_url:
            self.url = url.replace("i.pximg.net","i.pixiv.cat")
        else:
            self.url = "https://pixiv.cat/82939788.png".replace("82939788", str(Id))
        self.Id = str(Id)
        self.FileObj = None
        self.row = row
        self.le = requests.get(self.url, stream=True).headers["Content-Length"]
        if Name:
            self.FileObj = open(Name, "wb")
        else:
            self.prepare()




    def run(self):
        global length
        start = time.time()
        if float(self.le) < 0.5 * 2024 * 1024:
            resp = requests.get(self.url)
            self.FileObj.write(resp.content)
            self.FileObj.close()
        else:
            l = 0
            DownSplit(self.url)
            for i in results:
                data = i.result()
                string = data[0]
                data = data[1]
                p = "bytes (.*?)-"
                t = int(re.findall(p, string=string)[0])
                self.FileObj.seek(t, 0)
                self.FileObj.write(data)
            self.FileObj.close()
        end = time.time()
        s = "id:" + self.Id + "  下载成功,是否打开文件夹"
        self.process.emit(100, self.row, int(length/(end-start)/1024))
        self.success.emit(s)

    def prepare(self):
        try:
            des = requests.get(self.url, stream=True).headers["Content-Disposition"]
        except:
            print(self.url)
            print(requests.get(self.url, stream=True).headers)
        p = 'filename="(.*?)"'
        res = re.findall(p,des)
        if len(res) != 0:
            self.FileObj = open(res[0],"wb")



def down(downStart, length, no, url):
    global resps
    data = b''
    headers = {
        'Range': 'bytes=%s-%s' % (downStart, downStart + length),
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.43'
                     '89.90 Safari/537.36 Edg/89.0.774.63',
        'Host':'pixiv.cat'
    }
    response = requests.get(url, headers=headers)
    data=response.content
    return response.headers["Content-Range"], data




def DownSplit(url):
    global results,length
    length = int(requests.get(url,stream=True).headers['Content-Length'])
    part = int(length/12)

    with ThreadPoolExecutor(max_workers=8) as pool:
        for i in range(12):
            results.append(pool.submit(lambda p: down(*p),[i*part,part,i,url]))

    pool.shutdown()








