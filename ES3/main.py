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



def blur_filter(img_path, rgb_array, radius, weight):
    
    height, width, _ = rgb_array.shape
    
    blur = np.zeros((height, width, 3))
      
    # Apply functionality to every pixel of the image 
    for j in range(width):
        for i in range(height):
            
            # Integration and weight step
            pixels = 0
            for nj in range(j-radius, j+radius+1):
                if nj<0 or nj>width-1:
                    continue
                for ni in range(i-radius, i+radius+1):                
                    if ni<0 or ni>height-1:
                        continue                   
                    pixels += 1
                    blur[i,j,:] = (blur[i,j,:] + rgb_array[ni,nj,:]) if (nj!=j or ni!=i) else (blur[i,j,:] + weight*rgb_array[ni,nj,:])  
                 
            blur[i,j,:] = blur[i,j,:] / (pixels-1 + weight)
                      
    out_img_name = "blur-radius-{}-weight-{}.png".format(radius, weight)                  
    out_path_name = os.path.join(img_path, out_img_name)
    imsave(out_path_name, blur)    



def main(args):
       
    img_name = args.img_name
    option = args.option
    radius = args.radius
    weight = args.weight
    
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
    
    if option == 'rgb':
        rgb(img_path, red, green, blue)
    elif option == 'blur':
        blur_filter(img_path, rgb_array, radius, weight)
                   
    return
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ESSS3 - RGB Image Decomposition with Variable Stencil and Weighted Blur Filter')
    parser.add_argument(dest='option', type=str, help='Functionality option (e.g. rbg or blur)')
    parser.add_argument(dest='img_name', type=str, help='Image file name (e.g. original.jpg)')    
    parser.add_argument(dest='radius', type=int, help='Number of neighbors in each direction (e.g. radius = 1 gives a 3x3 windows)')
    parser.add_argument(dest='weight', type=int, help='Weight applied to central pixel')
    args = parser.parse_args()
    main(args)