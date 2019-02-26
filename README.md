# Coco-like-dataset-creator
Convert Data created with [labelme] (https://github.com/wkentaro/labelme#anaconda ) to coco format data set. 
This repo is aimed  at creating a full dataset which include the following subsets: 

        1. train set ~60% of the input images by default  
        2. test set ~20% of the input images bt default 
        3. validation set ~20% of the input images. 
The output has been tasted (so far all I can tell is that the training began)
on [facebookresearch/maskrcnn-benchmark](https://github.com/facebookresearch/maskrcnn-benchmark)
for instance segmentation. 

create the class with the file: 
CreateDastaSet.py 

## Installation 

I have based this script on the labelme labelme2coco script 
therefore follow the labelme installation instraction at [ wkentaro/labelme](https://github.com/wkentaro/labelme)

## How to Create the Dataset 

1. use the [ wkentaro/labelme](https://github.com/wkentaro/labelme) to annotate your data 
2. edit CreateDataSet inputDict  as follows 
  -input = path\to\your\Inputfolder   at the following format : (Bug therefore the fornat is required ) 
   * Inputfoder
      -subfolder1 - containing  data - Imgs and annotations  
      -subfolder2 - containing  data - Imgs and annotations 
      -subfolder3 - containing  data  - Imgs and annotations 
   * outputfoler= path\to\where\output\data\will\be\created
   *labels = 'path\to\label.txt'
   3. verify the output with the following [notebook](https://github.com/waspinator/pycococreator/blob/master/examples/shapes/visualize_coco.ipynb) from [pycococreator] (https://github.com/waspinator/pycococreator)
  
3. run the CreateDataSet.py script  

## TODO: 
- [x]  1. add annotations field BoundingBox 
- [x]  2. convert to work with iscrowded =0 , aka polygons dots 
- [ ]  3. add support to appending exsiting dataset (MUST Backup   Previous version to dir\old\setname+timeframe )   
- [ ]  4. re-enble parser 
- [ ]  5. solve directory in directory bug for list of json files gathering 
- [ ]  6. add a change directory function to \usedforcreatingdataset of input images 
        in order to avoid using them for appending the dataset. 
- [ ] 7. use imantics - Annotation to calculate BBox and area in stade of labelme function 

 ##  Knowon Bugs : 
 - [X] solved - appended empty annotations to the sets
 - [ ]  Input dircteroy has to be parent directory bug 
 
 


## credits: 
[labelme] (https://github.com/wkentaro/labelme#anaconda )
[pycococreator] (https://github.com/waspinator/pycococreator)       



