import numpy as np
import os
from PIL import Image 
from scipy.misc import imsave
import argparse


def rgb(img_path, red, green, blue):
    out_path_name = os.path.join(img_path, 'red.png')
    imsave(out_path_name, red)
    out_path_name = os.path.join(img_path, 'green.png')
    imsave(out_path_name, green)
    out_path_name = os.path.join(img_path, 'blue.png')
    imsave(out_path_name, blue)


def blur_filter(img_path, rgb_array):
    
    height, width, _ = rgb_array.shape
    
    blur = np.zeros((height, width, 3))
    
    # TODO Change the 'channel loop' by blur[i,j,:]
    for c in range(3):
        
        # Core
        for j in range(1,width-1):
            for i in range(1,height-1):
                blur[i,j,c] = (1/9)*(rgb_array[i,j,c]+rgb_array[i-1,j,c]+rgb_array[i+1,j,c]+rgb_array[i,j-1,c]+rgb_array[i,j+1,c]+rgb_array[i-1,j-1,c]+rgb_array[i+1,j+1,c]+rgb_array[i-1,j+1,c]+rgb_array[i+1,j-1,c])
        # Egdes
        j = 0
        for j in range(1,width-1):
            blur[i,j,c] = (1/6)*(rgb_array[i,j,c]+rgb_array[i-1,j,c]+rgb_array[i+1,j,c]+rgb_array[i,j+1,c]+rgb_array[i-1,j+1,c]+rgb_array[i+1,j+1,c])
        j = width-1
        for j in range(1,width-1):
            blur[i,j,c] = (1/6)*(rgb_array[i,j,c]+rgb_array[i-1,j,c]+rgb_array[i+1,j,c]+rgb_array[i,j-1,c]+rgb_array[i-1,j-1,c]+rgb_array[i+1,j-1,c])
        i = 0
        for i in range(1,height-1):
            blur[i,j,c] = (1/6)*(rgb_array[i,j,c]+rgb_array[i+1,j,c]+rgb_array[i,j+1,c]+rgb_array[i,j-1,c]+rgb_array[i+1,j+1,c]+rgb_array[i+1,j-1,c])        
        i = height-1
        for i in range(1,height-1):
            blur[i,j,c] = (1/6)*(rgb_array[i,j,c]+rgb_array[i-1,j,c]+rgb_array[i,j+1,c]+rgb_array[i,j-1,c]+rgb_array[i-1,j+1,c]+rgb_array[i-1,j-1,c])        
        # Corners
        i = j = 0
        blur[i,j,c] = (1/4)*(rgb_array[i,j,c]+rgb_array[i+1,j,c]+rgb_array[i,j+1,c]+rgb_array[i+1,j+1,c])
        j, i = 0, height-1
        blur[i,j,c] = (1/4)*(rgb_array[i,j,c]+rgb_array[i-1,j,c]+rgb_array[i,j+1,c]+rgb_array[i-1,j+1,c])
        j, i = width-1, 0
        blur[i,j,c] = (1/4)*(rgb_array[i,j,c]+rgb_array[i+1,j,c]+rgb_array[i,j-1,c]+rgb_array[i+1,j-1,c])        
        j, i = width-1, height-1
        blur[i,j,c] = (1/4)*(rgb_array[i,j,c]+rgb_array[i-1,j,c]+rgb_array[i,j-1,c]+rgb_array[i-1,j-1,c])
                
    out_path_name = os.path.join(img_path, 'blur.png')
    imsave(out_path_name, blur)    



def main(args):
         
    # General scope       
         
    img_name = args.img_name
    option = args.option
    
    img_path = os.getcwd()  
    img_path_name = os.path.join(img_path, img_name)
  
    image = Image.open(img_path_name)
      
    width, height = image.size
        
    red = np.zeros((height, width, 3))
    green = np.zeros((height, width, 3))
    blue = np.zeros((height, width, 3))  
    rgb_array = np.zeros((height, width, 3))
    
    for j in range(width):
        for i in range(height):
            r, g, b = image.getpixel((j, i))
            rgb_array[i,j,0] = red[i,j,0] = r
            rgb_array[i,j,1] = green[i,j,1] = g
            rgb_array[i,j,2] = blue[i,j,2] = b  
    
    # TODO: Implement argument options [-rgb, -blur]
    if option == 'rgb':
        rgb(img_path, red, green, blue)
    elif option == 'blur':
        blur_filter(img_path, rgb_array)
       
            
    return
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ESSS2 - RGB Image Decomposition and Blur Filter')
    parser.add_argument(dest='option', type=str, help='Functionality option (e.g. rbg or blur)')
    parser.add_argument(dest='img_name', type=str, help='Image file name (e.g. original.jpg)')    
    args = parser.parse_args()
    main(args)