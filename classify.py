import os
import time
import random
import shutil
import requests
from bs4 import BeautifulSoup
from Get_Dict import *
root_dir=os.path.dirname(__file__)
#print(root_dir)

def make_dirs(str):#创建文件夹
    if not os.path.exists(os.path.join(root_dir,'pic',str)):
        os.makedirs(os.path.join(root_dir,'pic',str))

def getURL(url='https://gelbooru.com/index.php?',cookie='',pram={},time1=10,time2=30,referer='https://gelbooru.com/',host='gelbooru.com'):
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
        time.sleep(random.randint(0,1)/2)#随机暂停0~0.5秒
        return response

def gettags(filename):#由文件名得到角色标签
    tags=[]
    id=filename.split('.')[0]
    pram={
        'page': 'post',
        's': 'view',
        'id':id,
    }
    html=getURL(pram=pram).text
    soup=BeautifulSoup(html,'html.parser')
    taglist=soup.select('.tag-type-character a')
    for tag in taglist:
        #print(tag.text)
        if (tag.text!='?'):
            tags.append(tag.text)
    #print(tags)
    return tags

def classify(str):
    #global dict
    exc=['manjuu_(azur_lane)']
    for file in os.listdir(os.path.join(root_dir,str)):
        tags=gettags(file)
        #print(tags)
        if(len(tags)<=3 and len(tags)>0):
            for tag in tags:
                if(tag not in exc):
                    if(dict.get(tag.replace(' ','_'))):
                        make_dirs(os.path.join(str,dict[tag.replace(' ','_')]))
                        if not os.path.exists(os.path.join(root_dir,'pic',str,dict[tag.replace(' ','_')],file)):
                            shutil.move(os.path.join(root_dir,str,file),os.path.join(root_dir,'pic',str,dict[tag.replace(' ','_')]))
                        else:
                            os.remove(os.path.join(root_dir,str,file))

                    else:
                        make_dirs(os.path.join(str,tag.replace(' ','_')))
                        if not os.path.exists(os.path.join(root_dir,'pic',str,tag.replace(' ','_'),file)):
                            shutil.move(os.path.join(root_dir,str,file),os.path.join(root_dir,'pic',str,tag.replace(' ','_')))
                        else:
                            os.remove(os.path.join(root_dir,str,file))
                    break
        else:
            make_dirs(os.path.join(str,'multi'))
            if not os.path.exists(os.path.join(root_dir,'pic',str,'multi',file)):
                shutil.move(os.path.join(root_dir,str,file),os.path.join(root_dir,'pic',str,'multi'))
            else:
                os.remove(os.path.join(root_dir,str,file))


#filename='7496131.xxx's
#gettags(filename)
#make_dirs(gettags(filename))
classify('1')
print('图片1分类完成')
classify('2')
print('图片2分类完成')
print('任务结束')