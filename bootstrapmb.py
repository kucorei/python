# -*- coding:utf-8 -*-
# Author :SHL
# Date   : 0:08
# File   :bootstrapmb.py
import requests, json, re, os
from bs4 import BeautifulSoup


class get_html():
    def __init__(self, get_turl):
        self.get_turl = get_turl
        #设置cookie值
        self.cookie = ''
        self.headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '1388',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': self.cookie,
            'DNT': '1',
            'Host': 'www.bootstrapmb.com',
            'Origin': 'http://www.bootstrapmb.com',
            'Referer': 'http://www.bootstrapmb.com/item/9226',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.headers1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'v.bootstrapmb.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        }
        self.headers2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Cookie': self.cookie,
            'DNT': '1',
            'Host': 'www.bootstrapmb.com',
            'Origin': 'http://www.bootstrapmb.com',
            'Referer': 'http://www.bootstrapmb.com/muban?page=3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0',
            'X-Requested-With': 'XMLHttpRequest',
        }

        self.data = {
            'oper': 'getTree',
            'view': ''
        }
        self.l = []
        self.k = []
        self.h = {}
        self.t = {}
        self.os_path = r'C:\Users\admin\Desktop'
        self.url = 'http://v.bootstrapmb.com/'
        self.get_item()
        self.get_request()
        self.processing()
        self.gui(self.x)
        for g in self.l:
            self.k.append(g)
        self.os_get()
        # 文档路径
        self.os_chdir(self.os_path)

        self.get_content()
        print('共下载%s个文件' % len(self.k))

    # 第一次请求，获取view参数和设置data数据
    def get_item(self):
        g = requests.get(self.get_turl, headers=self.headers2)
        g = BeautifulSoup(g.text, 'html.parser')
        r = g.find(id='view')
        u = re.findall('value="(.*?)"', str(r), re.S)[0]
        self.data['view'] = u
        self.url = self.url + '/' + u
        j = re.sub('bootstrap模板', "", g.title.text)
        self.path = re.sub(' _Bootstrap模板库', "", j)
        os.chdir(self.os_path)
        self.os_path = self.os_path + '/' + self.path
        if not os.path.exists(self.os_path):
            os.makedirs(self.path)

    # 根据内容来下载文件
    def get_content(self):
        for get in self.t:
            gett = self.t[get]
            try:
                content = requests.get(gett, headers=self.headers1)
                with open(get, 'wb') as f:
                    f.write(content.content)
                    f.close()
                print('下载成功:%s' % gett)
            except Exception as e:
                print('下载失败')

    # 获取目录
    def get_request(self):
        h = requests.post('http://www.bootstrapmb.com/_Ajax/Opt', headers=self.headers, data=self.data)
        self.content = h.text

    def processing(self):
        w = self.content
        soup = BeautifulSoup(w, 'html.parser')
        self.x = soup.div.ul

    # 递归处理所有的文件夹里面的内容
    # http://v.bootstrapmb.com/2020/11/mjiyy9226/cart.html
    def rui(self, w, text):
        for i in w.ul:
            txt = w.span.text
            x = text + '/' + str(txt) + '/' + str(i.span.text)
            if '.' in x:
                self.k.append(x)
            else:
                # 去除汉字文件夹
                if not re.search('[\u4E00-\u9FFF]', x, re.S):
                    try:
                        self.rui(i, text + '/' + str(txt))
                    except Exception as e:
                        pass

    # 取外层的html
    def gui(self, x):
        for i in x:
            # print(i.ul)
            # print(i.span.text)
            x = i.span.text
            if '.' in x:
                self.l.append(('/' + x))
            else:
                self.rui(i, '')

    # 取文件路径
    def os_get(self):
        for xx in self.k:
            i = re.findall('.*?\/', xx, re.S)
            q = ''
            for f in i:
                q = q + f
            self.h[q[1:-1]] = q[1:-1]

    # 创建文件夹
    def os_chdir(self, txt):
        os.chdir(txt)
        for i in self.h:
            t = i
            try:
                if not os.path.exists(t):
                    os.makedirs(t)
            except Exception as e:
                pass
        for pah in self.k:
            rr = txt + pah
            self.t[rr] = self.url + pah


get_html('http://www.bootstrapmb.com/item/8726')
