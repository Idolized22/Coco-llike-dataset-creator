#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Idolized22

This file pressents 
A class to create 3 Set of cocolike dataset : 
    - train 
    - test 
    - val 
The  Inputs are the output of the labelme  tool which is avilable in github, mentioned 
uder credits. 

This file is written in order to create train  a custum cocolike dataset on:
    the  https://github.com/facebookresearch/maskrcnn-benchmark/ mask-rcnn network. 
    
    
I have used this github exemple file : labelme2coco and fixed few bugs 
In addition, This File automatilcaly creates 3 sets , with used defined ratio
@parm :  DataDistrabutionTrainTestVal  
         - user defined ratio of Train: Test : Val ,
         must be  dict of integer with the following keys : 
        train , test , val . the defualt values are 60 20 20 respectively. 
@param: Name : string , the name of the dataset 

@param: pathes :  a dictionary  of pates with the following keys: 
                labels , input , output          
   TODO: 
    1. add annotations field BoundingBox 
    2. convert to work with iscrowded =0 , aka polygons dots 
    3. add support to appending exsiting dataset (MUST Backup   Previous version to dir\old+timeframe )   
    4. re-enble parsersupport 
    5. solve directory in directory bug for list of json files gathering 
    
    BUGS 
    solved :append empty masks to annotation 
    finds json files works only for directory inside directory 
Credits: 

https://github.com/wkentaro/labelme#anaconda 
https://github.com/waspinator/pycococreator         
        
"""

import argparse
import datetime
import glob
import json
import os
import os.path as osp
import sys
import numpy as np
import PIL.Image

import labelme

try:
    import pycocotools.mask
except ImportError:
    print('Please install pycocotools:\n\n    pip install pycocotools\n')
    sys.exit(1)

import string

from ModfiyImagesSizes import * 
from matplotlib import pyplot as plt 
from GetPolygon import *

###ver9 imports: 
#from pycococreatortools import *
########

######function add on verison 9 : 




######
class Del: # remove string names 
  def __init__(self, keep=string.digits):
    self.comp = dict((ord(c),c) for c in keep)
  def __getitem__(self, k):
    return self.comp.get(k)


def ListImages_andAnnotationFiles(args ):
    print("In Constraction\nCome Back Later Aligator")
    
def DetermineRandomSubset(InputFiles, coeff=dict(train=60,test=20,val=20)): 
    # coeef is to be passed as dict with keys : 'test' , 'train', 'val'
    # and it's values are the ratio of test : train : val
    SubSetAssosiation=[]
    RandomNumers= np.random.randint(0,coeff['train']+coeff['test']+coeff['val'],
                                    size=len(InputFiles))
    
    for integer,file in  zip(RandomNumers,InputFiles): 
        if integer in range (0, coeff['train']):
            SubSetAssosiation.append(dict(dist='train', 
                                     path = os.path.split(file)[0],
                                     name = os.path.split(file)[1]))
        elif integer in range(coeff['train'], coeff['train']+coeff['test']):
            SubSetAssosiation.append(dict(dist='test',
                                     path = os.path.split(file)[0],
                                     name = os.path.split(file)[1]))
        elif integer in range (coeff['train']+coeff['test'],
                               coeff['train']+coeff['test']+coeff['val']):
            SubSetAssosiation.append(dict(dist='val',
                                     path = os.path.split(file)[0],
                                     name = os.path.split(file)[1]))
            
    return SubSetAssosiation

def FilesInDir(path,*filetypes ):
    #return list of all files of specific file type 
    print ('Makeing list of files from the following types', *filetypes 
           ,'\nIn the following directory',path)        
    
    #files_lists= {a:[] for a   in filetypes}
    label_files = []
    #for filetype in files_lists :
    for root , directories, files in os.walk(path):
        for directory in directories:
            label_files= label_files+ glob.glob(osp.join(path,directory,'*.json'))
    return label_files

class CocoEnteryDataFormat: 
    def __init__ (self,Set_Name= '' ,data=None ): 
        #TODO add option to path to this function info and lisence 
        now = datetime.datetime.now()
        if (data==None): 
            data = dict(
            info=dict( 
                description=''+str(Set_Name),
                url='',
                version='',
                year=now.year,
                contributor="",
                date_created=now.strftime('%Y-%m-%d %H:%M:%S.%f'),
            ),
            licenses=[dict(
                url='',
                id=1,
                name="",
            )],
            images=[
                # license, url, file_name, height, width, date_captured, id
            ],
            type='instances',
            annotations=[
                # segmentation, area, iscrowd, image_id, bbox, category_id, id
            ],
            categories=[
                # supercategory, id, name
            ],
                    )
            
        
        else: 
            print ('TODO:\n ', 
               'read data fields from exsisting files')
        self.data=data




class COCO_DATASET :
    # Input Arguments : 
    #
    #dist_cofficeients_ is a dict of cofficent for the test train val distrabutaions  
    #
    #pathes : args pathes to inputs labels and images   ; 
    #         labels file (required only to create a new data_Set) ;
    #         output directory 
    # Name is the Name of the data set 
    def exsistance(self): 
        #check if dataset with the given pathes exsists 
        # if it's not exsist a new one is created 
        # TODO : if it's exsist append exsisting one 
        if osp.exists(self.args.output_dir):
            isappendable= True
            print('Output directory already exists:', self.args.output_dir)
            print('TODO: back up exsiting dataset')
            print('TODO: append exsiting dataset')
            self.index=dict (train=1 , test=1 , val =1 )
            #sys.exit(1)
        else:# create a fresh new dataset : 
            #os.makedirs(args.output_dir)
            #os.makedirs(osp.join(self.args.output_dir, 'JPEGImages'))# ToRemove in 
            os.makedirs(osp.join(self.args.output_dir,'train'))
            os.makedirs(osp.join(self.args.output_dir,'test'))
            os.makedirs(osp.join(self.args.output_dir,'val'))
            os.makedirs(osp.join(self.args.output_dir,'annotations'))
            print('Creating dataset:', self.args.output_dir)
            isappendable=False
        return isappendable

    def Load_Categories_from_LabelFile(self ): 
        # relevent for creating a new dataset 
        class_name_to_id = {}
        '''Ido: I dont need Categories -1 and 0 '''
        ## create a function for reading labels 
        for i, line in enumerate(open(self.args.labels).readlines()):
            class_id = i+1#19feb19 all countings starts from 1  #- 1  # starts with -1
            class_name = line.strip()
            class_name=class_name.lower() # make sure that all classes has the same name
            #if class_id == -1:
                #assert class_name == '__ignore__'
                #continue
            #elif class_id == 0:
                #assert class_name == '_background_'
            class_name_to_id[class_name] = class_id
            for key in self.data:
                self.data[key]['categories'].append(dict( # might be data[key, categories]
                    supercategory='Obj', #'None,
                    id=class_id,
                    name=class_name,
                ))
        return class_name_to_id

    def RemoveImgsWithNoanottations(self , ImgToRemove): 
        
        print('removing Images with ban anottations from datasets images field')
        
        for SubSetkey in ImgToRemove: 
            #loop over train test and val 
            for ImgName in ImgToRemove[SubSetkey]:
                #loop over all images to remove in the set 
                    for element in self.data[SubSetkey]['images']:
                        #check if the image name of the current list element maches
                        #current element to be removed: 
                        if element['file_name']==ImgName+'.jpg':
                            self.data[SubSetkey]['images'].remove(element)
                            print(ImgName, ' has been removed')
                            continue

    
    
    def AppendAnottation(self):
        print('add annotations to output directories')
        
        imgToRemoveTrain=dict(test=dict(),train=dict(),val=dict()) #ver10d4d3 :Remove Imgs with Corrapted mask from dataset
        
        
        out_ann_file = dict (  train = osp.join(self.args.output_dir,'annotations','train_annotations.json')
        ,test= osp.join(self.args.output_dir,'annotations','test_annotations.json')
        ,val = osp.join(self.args.output_dir,'annotations','val_annotations.json'))
        DD = Del()
        for file in self.subsetDistanation:
            print('Generating dataset from:',file['name'] ,
                  'appending ' ,file['dist'], ' subset')
            with open(osp.join(file['path'],file['name'])) as f:
                label_data = json.load(f)
            SinglePolygon=Get_PolygonsGEN(label_data) # version 9.5 segmentation path
            base=osp.splitext(file['name'])[0]
            out_img_file = osp.join(
            os.getcwd(),self.args.output_dir, file['dist'], base + '.jpg')
            img_file = osp.join(file['path'],label_data['imagePath'])
            
            #reduce ImageSize
            smallerImg ,NewSize  = resize_image(PIL.Image.open(img_file))    
            
            #img = np.asarray(PIL.Image.open(img_file))
            img = np.asarray(smallerImg)

            PIL.Image.fromarray(img).save(out_img_file)
            self.data[file['dist']]['images'].append(dict(
                    license=1,
                    url='',#TODO Add url for deseasedcardinmountofolives
                    file_name= base + '.jpg',
                    height=img.shape[0],
                    width=img.shape[1],
                    
                    date_captured=
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                    #I will use the number in the Image name as id 
                    id=int(base.translate(DD))#image_id+1,#start from 1
                    ))

            masks = {}
            for shape in label_data['shapes']:
                points = shape['points']
                label = shape['label'].lower()
                shape_type = shape.get('shape_type', None)
                mask = labelme.utils.shape_to_mask(
                    img.shape[:2], points, shape_type
                )
        
                mask = np.asfortranarray(mask.astype(np.uint8))
                '''# trying to avoid masks concatination 
                if label in masks:
                    masks[label] = masks[label] | mask
                else:
                    masks[label] = mask
                '''
                #index=1 # index is now a global variable  # Todo add condition in case of appending exsiting dataset        
            
            
                #for label, mask in masks.items():
                cls_name = label.split('-')[0]
                if cls_name not in self.class_name_to_id:
                    continue
                cls_id = self.class_name_to_id[cls_name]
                #23feb19 imshow mask #test that mask is not currapted 
                
                print(label,'Origonal Mask of : ', file['name'])
                
                #plt.imshow(mask)
                #plt.title(str(str(self.index)+' ' +label+' original Size Mask '+ file['name']))
                #plt.show()
                
                #resize Mask : 
                print(label,'Resizing Binary mask of img : ', file['name'])
                mask= resize_binary_mask(mask,NewSize) 
                
                
                #from matplotlib import pyplot as plt 
                #print('Resized Mask of: ', file['name'])
                #plt.imshow(mask)
                #plt.title(str(str(self.index)+' '+label+' ' +file['name']+ ' Resized Mask' ))
                #plt.show()
                
                segmentation = pycocotools.mask.encode(np.asfortranarray(mask.astype(np.uint8)))
                segmentation['counts'] = segmentation['counts'].decode()
                area = float(pycocotools.mask.area(segmentation)) #consider to remove float
                bounding_box =pycocotools.mask.toBbox(segmentation)#ver9 added bbox under debug  
                
                
                #if area and bbox is not None append datasets 
                if (area>0 ): 
                    self.data[file['dist']]['annotations'].append(dict(
                        #segmentation=segmentation,
                        segmentation = [next(SinglePolygon)], # ver9.5 patch
                        height=img.shape[0],
                        width=img.shape[1],
                        area=area,
                        iscrowd=0, #use RLE ,#None,
                        image_id=int(base.translate(DD)), # just as im above under field images 
                        bbox=bounding_box.tolist(),
                        category_id=cls_id
                        ,id=self.index[file['dist']],))##TODO? add BoundingBox , convert to polygons ?
                    self.index[file['dist']]=self.index[file['dist']]+1 
                    print (str(str(self.index)+' ' +label+'  '+ file['name'])
                    ,'\n has been appended succefuly' )
                else :
                    print('skipped ', label , file['name'], ' index is not promoted ' , self.index)
                    imgToRemoveTrain[file['dist']][base]=base + '.jpg'
                    print('DEBUG:'+' imgToRemove ' + file['dist'],' '  ,type(imgToRemoveTrain[file['dist']])
                    ,'has been appended with: ',base + '.jpg')
                    print('The length of the images to remove ',file['dist']
                    ,' is ' ,len(imgToRemoveTrain[file['dist']]))
                    #TODO : try to remove the image from the dataset 
            #RemoveImgsWithNoanottations()
        print(len( imgToRemoveTrain['train'] ),' Will be renoved from train '
              ,len( imgToRemoveTrain['test'] ),' Will be renoved from test '
              ,len( imgToRemoveTrain['val'] ),' Will be renoved from  val ',
              '\n In Total:',len( imgToRemoveTrain['train'] )
              +len( imgToRemoveTrain['test'])+len( imgToRemoveTrain['val'])
              ,' will be removed because of currupted annotations json file',
              'Their Removement could be tempural if a iscrowded = 0'
              , 'will be used  and their polygons dots will be devied by factor',
              'of the image resize')
        print('would you like to remove the images? [Y , else] ')
        #Res=input()
        if (False):
            self.RemoveImgsWithNoanottations(imgToRemoveTrain)
    
    def DumpToAnnotationFile(self):
         
        for key in self.data:
            with open(os.path.join(self.args.output_dir, 'annotations','instances_'+key+'.json'), 'w') as f:
                json.dump(self.data[key], f)
        
        
    def __init__(self, pathes , DataDistrabutionTrainTestVal,Name,SetsInfo):
        self.pathes = pathes
        self.Name=Name
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.parser.add_argument('--input_dir', help='input annotated directory')
        self.parser.add_argument('--output_dir', help='output dataset directory')
        self.parser.add_argument('--labels', help='labels file', required=True)
        self.args = self.parser.parse_args('--input_dir arg1 --output_dir arg2 --labels arg3'.split( ))
        self.index=self.index=dict (train=1 , test=1 , val =1 ) #annotation index, 
        #TODO:support for appending exsiting dataset update value to be the last of exsting sets+1
        self.args.output_dir=pathes['output']
        self.args.input_dir=pathes['input']
        self.args.labels=pathes['labels']
        
        
        self.isappendable= self.exsistance()
        self.inputfile= FilesInDir(self.args.input_dir,'.json' ,'.ipg','png')
        
         
        
        if ( not self.isappendable):
            print ('new dataset is being created')
            self.data= dict (
            train=CocoEnteryDataFormat(Set_Name='train',SetsInfo).data
            ,test=CocoEnteryDataFormat(Set_Name='test',SetsInfo).data
            ,val=CocoEnteryDataFormat(Set_Name='val',SetsInfo).data
            )
            #add categories from  label file 
            self.class_name_to_id=self.Load_Categories_from_LabelFile()
            #make list of input images: 
            #sort input images between sets 
        else: #if dataset is appendable:
            #call class Coco CocoEnteryDataFormat with path to exsisting data 
            print ('a Data set has been created already')
            print('TODO: append Dataset\n',
                  '\t 1. Make list of images already in the dataset', 
                  '\n\t 2. Make list of images to add to the datasrt',
                  '\n\t 3. Remove exsisting images from list of images to add to the dataset', 
                  '\n\t 4. Figure How other functions should treat the Boolian isappendable', 
                  '\n\t\t 4.1 during json creation: if is appendable==True: append exsisting file')
        
        self.subsetDistanation = DetermineRandomSubset(self.inputfile,
                                                       DataDistrabutionTrainTestVal)
        
        self.AppendAnottation()
        
        self.DumpToAnnotationFile()










print('\n\nDebug:\t\t Build: CocoClass file  Built Successfully')
