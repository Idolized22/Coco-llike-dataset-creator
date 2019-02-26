#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 23:55:54 2019

@author: Idolized22
"""

import json
JsonAnnotationFilePath='.' 
def Open_Json_File(JsonAnnotationFilePath):
    print ('Ido: openning Json file') 
    json_data=open(JsonAnnotationFilePath).read() 
    data = json.loads(json_data)
    print('Ido : data loaded successfuly')
    return data

def Approximate_BB(polygons_list):
    print('Generating BundingBox from annotations')
    print('Creating List of Heights')
    height_list=[]
    
    #function for debug test that script generated BBox are logit 
	
    ####TODO: test if the source at https://github.com/wkentaro/labelme 
    #Treated  the points as (x,y) or (height, Width)
    # I assumed (height, Width) if i am worg replace list index in for loops 
    # it's x y 
    
    for height in polygons_list:
        height_list.append(height[0]) #if xy replace to 1 
    sorted_height= sorted(height_list)
    Max_height=sorted_height[-1]
    Min_height=sorted_height[0]
    
    print('Creating List of Width')
    width_list=[]
    for width in polygons_list:
        width_list.append(width[1]) # if xy replace to 0 
    sorted_width= sorted(width_list)
    Max_width=sorted_width[-1]
    Min_width=sorted_width[0]
    print('BBox approximated Succesfuly')
    #           x           y           width                   height 
    return [Min_width , Min_height ,Max_width-Min_width ,Max_height-Min_height ] #  [x,y,width,height]
    #http://cocodataset.org/#format-data 
    #accurding to coco the format for the bounding boxes should be:  [x,y,width,height]

def Get_Polygons(data):     
    #print(data['shapes'])
    shapes_list= data['shapes']
    #shapes_list = shapes_list['points']
    index=0
    polygon_list = []
    for element in shapes_list:#['points']: I have checked and this way the loop is over a dict of all points
        index=index+1
        #polygon_list = []
        polygon_list.append(element['points'])
        #shape_list[Index]['points']
        print('\t\t\t', index,'Ido : polygons list of list of dots gotten succesfuly from\n\t')
        print([item for sublist in element['points'] for item in sublist])
    print (' GEt Poltgons : The image has', index , 'annotatins')
    return polygon_list
    #return [item for sublist in element['points'] for item in sublist]

def Get_PolygonsGEN(data):     
    #print(data['shapes'])
    shapes_list= data['shapes']
    #shapes_list = shapes_list['points']
    index=0
    for element in shapes_list:#['points']: I have checked and this way the loop is over a dict of all points
        index=index+1
        #polygon_list = []
        #polygon_list.append(element['points'])
        #shape_list[Index]['points']
        print('\t\t\t', index,'Ido : polygons list of list of dots gotten succesfuly from\n\t',element['points'])
        print([item for sublist in element['points'] for item in sublist])
        yield [item for sublist in element['points'] for item in sublist]
