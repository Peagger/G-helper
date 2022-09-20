from cv2 import namedWindow, imshow, waitKeyEx, imread,resizeWindow
import cv2
import os
import shutil
import time
import sys

leftkeys = (81, 110, 65361, 2424832)
rightkeys = (83, 109, 65363, 2555904)
# 当前脚本工作的目录路径
#root_dir = os.getcwd()
root_dir=os.path.dirname(os.path.realpath(__file__))
#print(root_dir)
# os.path.abspath()获得绝对路径
root_absdir = os.path.abspath(os.path.dirname(__file__))
#print(__file__)
#print(os.path.dirname(__file__))
#print(root_absdir)

os.chdir(root_dir)
def make_dirs2(n):
    if not os.path.exists(os.path.join(root_dir, n)):
        os.makedirs(os.path.join(root_dir, n))


def Classification_Tools(num_cls):
    #data_dir = './azur_lane/'   # 待分类数据路径
    #data_dir='./honkai_impact_3rd'
    data_dir='./genshin_impact/'
    if not os.path.exists(data_dir):#报错
        print('data_all not exists, please put data to: ', data_dir)
        time.sleep(5)
        exit()
    for i in range(1,num_cls+1):#初始化分类文件
        make_dirs2(str(i))
    image_list = os.listdir(data_dir)
    if len(image_list) == 0:
        print('no image in %s ... please put data to: %s'%(data_dir, data_dir))
        time.sleep(5)
        exit()
    #namedWindow('Classification_Tools', 0)
    i = 0
    coccus_label = None
    while True:
        assert i < len(image_list), ('no image left...')
        print('i', i)
        image_path = os.path.join(data_dir, image_list[i])
        print(image_path)
        image = imread(image_path)
        try:
            print(image.shape)
            cv2.destroyAllWindows()
            #namedWindow('Classification_Tools',cv2.WINDOW_NORMAL)
            height,width = image.shape[:2]#矩阵的shape
            if height>1000:
                proportion=1000/height
                image=cv2.resize(image,(int(proportion*width),int(1000)),interpolation=cv2.INTER_AREA)
            imshow('Classification_Tools', image)
            #cv2.resize(image,image.shape[0:2])
            key = waitKeyEx()

            if key in rightkeys:
                i =  (i + 1) % len(image_list)
                
            if key in leftkeys :
                # if not os.path.exists(os.path.join(('./' + str(coccus_label)), image_list[i-1])):
                print('leftkeys:', os.path.join(('./' + str(coccus_label)), image_list[i - 1]))
                if os.path.exists(os.path.join(('./' + str(coccus_label)), image_list[i - 1])):
                    print('ssssssssssssss', os.path.join(('./' + str(coccus_label)), image_list[i - 1]))
                    shutil.move(os.path.join(('./' + str(coccus_label)), image_list[i - 1]), data_dir)
                i -= 1
                if i < 0:
                    i = len(image_list) - 1

            if (key == ord('q')) or (key == 27):
                break

            for j in range(1,num_cls+1):
                if key & 0xFF == ord(str(j)):
                    coccus_label = str(j)
                    shutil.move(image_path, os.path.join(root_dir, str(j)))
                    i =(i + 1) % len(image_list)
                    break
        except:
            i+=1


#if __name__ == '__main__':
    # num_cls = sys.argv[1] # 传入类别数量
num_cls = 3
Classification_Tools(num_cls)

