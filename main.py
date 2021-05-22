#streamlit run main.py

import streamlit as st
import os
import numpy as np
from PIL import Image, ImageOps
import os 
from inference_onnx import inference

@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    with open(os.path.join("temp", image_file.name),"wb") as f:
        f.write(image_file.getbuffer())
    return img



@st.cache
def extractor(image_path, filename):
    
    # check input arguments
    if not os.path.exists(image_path):
        print('Cannot find input path: {0}'.format(image_path))
        exit()
    # get the path storing the background images
    output_path = 'silhouette/'
    # Modnet model directory required for execution
    model_path = 'modnet.onnx'
        
    ## call inference_onnx.py or demo2.py
    #print("Inference in Onnx")
    #print('... Cropping')
    inference(image_path,os.path.join(output_path,filename),model_path)

    # visualize all images
    image = Image.open(image_path)
    matte = Image.open(os.path.join(output_path,filename))



    ## convert image to greyscale
    #c_image = ImageOps.grayscale(image)
    image.putalpha(matte)
    print("... Done")
    #im2 = ImageOps.grayscale(matte)
    #im2.show()
    
    # save image to folder with same name as of original file
    image.save('cropped_images/'+os.path.splitext(filename)[0]+'.png')
    return ('cropped_images/'+os.path.splitext(filename)[0]+'.png')



if __name__ == '__main__':
    st.title("Background Remover")
    st.header("Removing background with Artificial Intelligence")
    st.write("""Removal of unwanted outer areas from a graphic or illustrated image; 
                this process usually consists of removing some of the peripheral regions 
                of an image to remove extraneous trash from the picture, improving its 
                framing, and accentuating or isolating the subject matter from its background.""")
    st.write("""Here, we have a web application that uses artificial intelligence to remove
                the background of any image or photo. It works 100% automatically, so you 
                don't need to select the background/foreground layers to separate them manually
                 - choose or select your image and instantly download the output image with the 
                 background removed.""")

    # Opening image and setting full page view
    image = Image.open('banner-app1.png')
    st.image(image, use_column_width=True)
    
    image_file = st.file_uploader("Upload Image",type=['png','jpeg','jpg'])
    if image_file is not None:
        # To See Details
        # st.write(type(image_file))
        #st.write(dir(image_file))
        #st.write(type(dir(image_file)))
        file_details = {"Filename":image_file.name,"FileType":image_file.type,"FileSize":image_file.size}
        st.write(file_details)
        st.write(image_file)
        img = load_image(image_file)
        #st.image(img,width=250,height=250)
        st.image(img)

        # Push to start the matchmaking process
        button = st.button("Click to Start cropping")
        if button:
            # brings in a progress bar
            with st.spinner('Cropping...'):
                # Vectorizing the New Data
                # df_v, input_df = vectorization(df, df.columns, new_profile)
                name = extractor(os.path.join('temp',image_file.name), image_file.name)
                st.write(name)
                cropped_image = Image.open(name)
                #st.image(img,width=250,height=250)
                st.image(cropped_image)
                # Scaling the New Data
                # new_df = scaling(df_v, input_df)
                # Success message , replacing the progress bar  
                st.success("Background removed!")    
                st.balloons()
                print()




