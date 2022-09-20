import os
import shutil
root_dir=os.path.dirname(__file__)
dict={}

def Create_Dict():
    with open(os.path.join(root_dir,'对照表.csv'),'r',encoding='utf-8-sig') as f:
        dicts=f.read().split('\n')
        for elem in dicts:
            #print(elem.split(','))
            if(len(elem.split(','))>=3):
                dict[elem.split(',')[2]]=elem.split(',')[1]
    return dict

#Create_Dict()

Create_Dict()
