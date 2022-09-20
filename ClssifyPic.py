
from importlib.resources import path
import os
import shutil
import cv2
import os.path as op



root_dir=os.path.dirname(os.path.realpath(__file__))
filenames=['selected','r18g','discard']
class ClassifyPic():
    def __init__(self,path='pic',kind=3):
        self.hight=1600/3
        self.width=2560/3
        self.image_list=os.listdir(op.join(root_dir,path))
        self.path=path
        self.savedir='classified'
        self.kind=len(filenames)
        self.filenames=filenames
        self.record=[]#记录执行的操作
        self.movedpic=[]

    
    def makeDir(self,filename,path=''):
        if not os.path.exists(os.path.join(root_dir,path,filename)):
            os.makedirs(os.path.join(root_dir,path,filename))
    def makeResultDirs(self):
        for i in range(0,self.kind):
            self.makeDir(path=self.savedir,filename=filenames[i])
    
    def showimage(self):
        '''显示'''
        leftkeys = (81, 110, 65361, 2424832)
        rightkeys = (83, 109, 65363, 2555904)
        i=0
        length=len(self.image_list)#图片数量
        if(length==0):print('请在{}文件夹下放入图片'.format(self.path));return
        while True:
            print('第{}张'.format(i+1))
            i=i%len(self.image_list)
            if (i in self.movedpic):
                if (len(self.movedpic)!=length):
                    i=i+1;continue
                else:
                    print('好耶,分类完毕!')
            #读取图片
            image_path=op.join(root_dir,self.path,self.image_list[i])
            image=cv2.imread(image_path)
            cv2.destroyAllWindows()
            #缩放图片比例
            hight,width = image.shape[:2]
            ratioOfHight=self.hight/hight
            ratioOfwidth=self.width/width
            if ratioOfHight<1:      ratio=ratioOfHight
            if ratioOfwidth<ratio:  ratio=ratioOfHight
            if ratio:
                image=cv2.resize(image,(int(width*ratio),int(hight*ratio)),interpolation=cv2.INTER_AREA)
            #窗口设置
            cv2.imshow(self.image_list[i], image)
            pressedKey=cv2.waitKeyEx()
            print('当前输入: ',pressedKey,pressedKey&0xff)

            if (pressedKey==-1)or(pressedKey&0xff==27):break
            if (pressedKey in leftkeys):
                if(len(self.record)>0):
                    act=self.record.pop()
                    i=(i-1+length)%length
                    if(act[0]==-1):
                        continue
                    else:
                        self.movedpic.remove(act[0])
                        shutil.move(act[1],act[2])
                        continue
                else:
                    i=(i-1+length)%length
                    continue
            if (pressedKey in rightkeys):
                i+=1
                self.record.append([-1])
                continue
            for j in range(self.kind):
                if(pressedKey&0xff==ord(str(j+1))):
                    shutil.move(image_path,op.join(root_dir,self.savedir,self.filenames[j]))
                    self.movedpic.append(i)
                    self.record.append([i,op.join(root_dir,self.savedir,self.filenames[j],self.image_list[i]),op.join(root_dir,self.path)])
                    continue



if __name__=='__main__':
    classify=ClassifyPic()
    classify.makeResultDirs()
    classify.showimage()
    #print(classify.image_list)
    print('程序结束')


        