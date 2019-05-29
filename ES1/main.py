import numpy as np
import os
from PIL import Image 
from scipy.misc import imsave
import argparse


def main(args):
         
    img_name = args.img_name     
    img_path = os.getcwd()  
    img_path_name = os.path.join(img_path, img_name)
  
    image = Image.open(img_path_name)
      
    width, height = image.size
    
    red = np.zeros((height, width, 3))
    green = np.zeros((height, width, 3))
    blue = np.zeros((height, width, 3))
    
    for i in range(width):
        for j in range(height):
            r, g, b = image.getpixel((i, j))
            red[j,i,0] = r
            green[j,i,1] = g
            blue[j,i,2] = b
    
    out_path_name = os.path.join(img_path, 'red.png')
    imsave(out_path_name, red)
    out_path_name = os.path.join(img_path, 'green.png')
    imsave(out_path_name, green)
    out_path_name = os.path.join(img_path, 'blue.png')
    imsave(out_path_name, blue)
            
    return
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ESSS1 - RGB Image Decomposition')
    parser.add_argument(dest='img_name', type=str, help='Image file name (e.g. original.jpg)')
    args = parser.parse_args()
    main(args)