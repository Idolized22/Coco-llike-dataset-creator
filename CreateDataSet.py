#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: idolized22

"""

from CocoCreatorClass import COCO_DATASET

import datetime
InputDict=dict(
        input='path to input images and annotations - see bug '
        ,output='path to where output data will be saved'+
        datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'),
        labels ='path to /labels.txt'
        )


now = datetime.datetime.now()
        
SetsInfo = dict(
        info=dict( 
        description='',
        url='',
        version='',
        year=now.year,
        contributor="",
        date_created=now.strftime('%Y-%m-%d %H:%M:%S.%f')),
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

Headstones_var = COCO_DATASET(InputDict,dict(train=60,test=20,val=20),'NameOf THE DataSet', SetsInfo)
print(datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'),'DATA created succefuly at:', InputDict['output'])
