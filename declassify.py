from logging import root
import os
import shutil
root_path=os.path.dirname(os.path.realpath(__file__))
def moveback(path,target):
    for dir in os.listdir(path):
        picdir=os.path.join(root_path,path,dir)
        print(picdir)
        for pic in os.listdir(picdir):
            picpath=os.path.join(picdir,pic)
            print(picpath)
            try:
                shutil.move(picpath,target)
            except:
                print('{}已存在'.format(pic))
                os.remove(picpath)

moveback('pic/1','classified/1')