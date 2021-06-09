"""
Generate transparent image without background
"""

import numpy as np
from PIL import Image, ImageOps
import os 
from inference_onnx import inference
#from tkinter import *
from tkinter import filedialog




def get_folder_dir():
    """
       Opens a pop-up window to select the the folder directory
       which stores the images
    """
    dir_path = filedialog.askdirectory()
    return dir_path




if __name__ == '__main__':
    
    '''
    # dowload the onnx model for image matting
    model = 'modnet.onnx'
    if not os.path.exists(model):
        url = 'https://drive.google.com/uc?id=1cgycTQlYXpTh26gB9FTnthE7AvruV8hd'
        r = requests.get(url)

        urllib.request.urlretrieve(url, '/pretrained/modnet.onnx')
    
        #!gdown --id 1cgycTQlYXpTh26gB9FTnthE7AvruV8hd \
        #      -O pretrained/modnet.onnx
    '''


    # get the required folder directory
    image_path = get_folder_dir()
    # check input arguments
    if not os.path.exists(image_path):
        print('Cannot find input path: {0}'.format(image_path))
        exit()
    # get the path storing the background images
    output_path = 'silhouette/'
    # Modnet model directory required for execution
    model_path = 'modnet.onnx'
    print("USER DEFINED FOLDER:",image_path)
    
    
    #i=0
    for filename in os.listdir(image_path):
        
        # sometimes image folder might contain random hidden files like
        # .ini so they are being skipped
        if '.ini' in filename:
            continue
        
        # get file path
        name = os.path.join(image_path,filename)
        print("FIlENAME:", name)
        
        # call inference_onnx.py or demo2.py
        #print("Inference in Onnx")
        print('... Cropping')
        inference(name,os.path.join(output_path,filename),model_path)

        # visualize all images
        image = Image.open(name)
        matte = Image.open(os.path.join(output_path,filename))
        #display(combined_display(image, matte))



        # convert image to greyscale
        c_image = ImageOps.grayscale(image)
        c_image.putalpha(matte)
        print("... Done")
        #im2 = ImageOps.grayscale(matte)
        #im2.show()
        
        # save image to folder with same name as of original file
        c_image.save('cropped_images/'+os.path.splitext(filename)[0]+'.png')
        #i+=1
        print("File saved")

















