#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: idolized22
"""
import PIL.Image
from matplotlib import pyplot
import numpy as np 



def resize_image (Img, DesieredSize=[1300,1300]): 
    #desired size to be passed as [width , height ]
    factor=1
    while (Img.size[0] * Img.size[1])>( DesieredSize[0]* DesieredSize[1]): 
        #reduce_size
        Img=Img.resize((Img.size[0]//2,Img.size[1]//2),resample=PIL.Image.LANCZOS)
        factor=factor+1
    
    return [Img , Img.size]

def resize_binary_mask(array, new_size):
    #from pycocotools  on github 
    image = PIL.Image.fromarray(array.astype(np.uint8)*255)
    image = image.resize(new_size)
    return np.asarray(image).astype(np.bool_)

