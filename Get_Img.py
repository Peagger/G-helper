
from math import inf
import requests
import time
import random
from bs4 import BeautifulSoup
import os
import re
format_pattern=re.compile(r'(\.[a-z]+)$')
path=os.path.dirname(os.path.realpath(__file__))
#负责判断图片位置
class id():
    _list=[]
    def __init__(self,tag):
        self.tag=tag
    def getlist(self):
        isExists=os.path.exists(os.path.join(path,'id',self.tag+'.txt'))
        if isExists:
            with open(os.path.join(path,'id',self.tag+'.txt'),'r') as f:
                ls=f.read().split(',')
        else:
            with open(os.path.join(path,'id',self.tag+'.txt'),'w') as f:
                print(self.tag+'.txt文件初始化')
                ls=[]
        self._ls=ls
    #最大值
    def getmax(self):
        if(len(self._ls)>0):
            max=self._ls[0]
            for id in self._ls:
                if (id>max):
                    max=id
            return max
        else :
            return 0
    #最小值
    def getmin(self):
        if(len(self._ls)>0):
            min=self._ls[0]
            for id in self._ls:
                if (id<min and id!=''):
                    min=id
            return min
        else :
            return inf
    #写入
    def write(self,str):
        isExists=os.path.exists(os.path.join(path,'id',self.tag+'.txt'))
        if isExists:
            with open(os.path.join(path,'id',self.tag+'.txt'),'a+') as f:
                f.write(str+',')
        else:
            with open(os.path.join(path,'id',self.tag+'.txt'),'w') as f:
                print(self.tag+'.txt文件初始化')

def getURL(url,cookie='',pram={},time1=10,time2=30,referer='https://gelbooru.com/',host='gelbooru.com'):
    try:
        
        headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
            'Cookie':cookie,
            'host':host,
            'Connection':'close',
            'referer':referer,
        }
        response=requests.get(url,headers=headers,timeout=(time1,time2),params=pram)
        response.raise_for_status() #如果请求\响应\保存\解析中任何一步出了问题就会报错
        response.encoding = response.apparent_encoding #使用网站自身编码
    except Exception as e:
        print(e)
    else:
        time.sleep(2*random.random())#随机暂停0~1秒
        return response

#由图片id和图片tag保存图片
format=''
def SaveImage(id,tag):
    global format
    pram={
        'page': 'post',
        's': 'view',
        'id':id,
    }
    html=getURL('https://gelbooru.com/index.php?',host='img3.gelbooru.com',pram=pram).text
    soup=BeautifulSoup(html,'html.parser')
    url=soup.select('.fit-width')[0]['src']
    #print(url)
    format=format_pattern.findall(url)[0]
    isExist=os.path.exists(os.path.join(path,tag))
    if not isExist:
        os.makedirs(os.path.join(path,tag))
        print("创建"+tag+"目录成功")
    isExist=os.path.exists(os.path.join(path,tag,id+format))
    if not isExist:
        pic=getURL(url).content
        with open(os.path.join(path,tag,id+format),"wb") as f:
            f.write(pic)
    

#由tag得到图片id
def GetId(tag,num=500,max=0,min=100000000,mod='1'):#上限500张
    list=[]
    count=0
    urllist=['']
    while (urllist):#防止循环无法结束
        pram={
            'page': 'post',
            's': 'list',
            'tags':tag,
            'pid':str(count),
        }
        try:
            res=getURL('https://gelbooru.com/index.php?',pram=pram)
            count+=42
            soup = BeautifulSoup(res.text, 'html.parser')
            urllist=soup.find_all('article',attrs={'class':'thumbnail-preview'})
            if (mod=='1'):#新图模式，旧到新
                for url in urllist:
                    id=url.a['id'][1:]
                    if(id>max):
                        list.append(id)
                    else:
                        print('找到上次的位置,共'+str(len(list))+'张,开始爬取')
                        return list
            elif(mod=='3'):#老图模式，新到旧，一次100张
                for url in urllist:
                    id=url.a['id'][1:]
                    if(id<min):
                        #if(len(list)<100):
                        if(len(list)<500):
                            list.append(id)
                        else:
                            print('从上次的位置开始,共'+str(len(list))+'张,开始爬取')
                            return list
            elif(mod=='2'):#初始化，20张
                for url in urllist:
                    id=url.a['id'][1:]
                    if(len(list)>=20):
                        print('初始化,共'+str(len(list))+'张,开始爬取')
                        return list
                    else:
                        list.append(id)
        except Exception as e:
            print(e)
            print(str(count)+'出现错误')
    return list
def setmode(i):
    global mod
    mod=str(i)
tag='genshin_impact'#'genshin_impact'honkai_impact_3rd''azur_lane'
#mod='1'#'新图模式'
#mod='2'#'初始化'
#mod='3'#'老图模式'

mod='1'
limit=id(tag)
limit.getlist()
max,min=limit.getmax(),limit.getmin()
try:
    idlist=GetId(tag,max=max,min=min,mod=mod)
    if(mod=='1'):
        idlist.reverse()
    for id in idlist:
        try:
            SaveImage(id,tag)
            limit.write(id)
        except:
            print(id+"失败")
except:
    print(tag+'错误')
print(tag+'结束')
