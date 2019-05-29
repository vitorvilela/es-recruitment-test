import os
import argparse
import numpy as np
from PIL import Image 


class Grid(object):
    """
    A class used to represent 2D grids along a variable numbers of layers
    E.G. Height x Width x Channels
    
    Attributes
    ----------    
    name : str
        Class name
    version : str
        Version control number
    array : ndarray
        Numpy array of rank 3 holding pixel values

    Methods
    -------
    neighborhoodList(index, radius)
        Gives a list of (i, j, value) neighbors for a given pixel
    """
              
    name = 'Grid'
    version = '0.1'
        
    def __init__(self):   
        """
        Initializes a zeroed array with shape (1, 1, 1)        
        """        
        self.array = np.zeros((1, 1, 1))
        
    def __iter__(self):   
        """
        Defines class iterator to yield every (i, j) of the Grid
        i and j are the height and width indices of the Grid, respectively          
        """        
        height, width, _ = self.array.shape        
        for j in range(width):
            for i in range(height):                
                yield (i, j)
        
    def neighborhoodList(self, index, radius): 
        """
        Gives a list of pixels (ni, nj, value) adjacent to a given (i, j) pixel, restricted to a radius windows
        ni and nj are height and width indices, respectively, and pixel is a np.uint8 value in the range [0-255]  
        """ 
        i, j = index
        height, width, _ = self.array.shape               
        y = [ nj for nj in range(j-radius, j+radius+1) if (nj>=0 and nj<width) ]
        x = [ ni for ni in range(i-radius, i+radius+1) if (ni>=0 and ni<height) ]
        pixel_windows = [(ni, nj, self.array[ni,nj,:]) for nj in y for ni in x]                
        return pixel_windows
              
          
   
class SingleChannelGrid(Grid): 
    """
    A class derived from Grid used to represent a 2D grid for a single channel image
    E.G. Height x Width x 1
    
    Attributes
    ----------    
    name : str
        Class name
    version : str
        Version control number
    array : ndarray
        Numpy array of rank 3 holding pixel values

    Methods
    -------
    blurFilter(grid_filter)
        Gives a {'filter name': filtered array} dict
    saveAsImage(grid_dict, label)
        Saves the filtered Grid as image         
    """   
    
    name = 'SingleChannelGrid'
    version = '0.1'            
    
    def __init__(self, image):    
        """
        Initializes an array from a single channel image and expand its dimension in order to rank 3       
        
        Parameters
        ----------
        image : PIL.Image
            Single channel image
        """
        self.array = np.expand_dims(np.asarray(image), axis=2)
                
    def blurFilter(self, grid_filter):  
        """
        Applies the Blur filter to a singleChannelGrid object (OR object based on derived classes)       
        
        Parameters
        ----------
        grid_filter : GridFilter
            GridFilter object holding its parameters            
        """    
        height, width, rank = self.array.shape                          
        blur = np.zeros((height, width, rank))
        for i, j in self.__iter__():
            pixel_windows = self.neighborhoodList((i, j), grid_filter.radius)             
            for ni, nj, pixel in pixel_windows:   
                blur[i,j,:] = (blur[i,j,:] + pixel[:]) if (ni, nj) != (i, j) else (blur[i,j,:] + np.multiply(pixel, grid_filter.weight))       
            blur[i,j,:] = np.divide(blur[i,j,:], (len(pixel_windows)-1 + grid_filter.weight))                
        return {'blur': blur.astype(np.uint8)}    
    
    def saveAsImage(self, grid_dict, label):
        """
        Saves as 'L' mode image the filtered Grid array given by {'filter name': filtered array} dict      
        
        Parameters
        ----------
        grid_filter : BlurFilter
            Filter object holding its parameters  
        label : str
            Image name prefix
        """
        for key, channel in grid_dict.items():
            out_name = '{}{}{}'.format(label, key, '.png')
            img_path = os.getcwd()
            out_path_name = os.path.join(img_path, out_name)
            out_image = Image.fromarray(np.squeeze(channel, axis=2).astype('uint8'), mode='L')
            out_image.save(out_path_name)  
              
              

class MultiChannelGrid(SingleChannelGrid):    
    """
    A class derived from SingleChannelGrid used to represent 2D grids for a multi channel image
    E.G. Height x Width x Channels
    
    Attributes
    ----------    
    name : str
        Class name
    version : str
        Version control number
    array : ndarray
        Numpy array of rank 3 holding pixel values

    Methods
    -------
    splitFilter(grid_filter)
        Gives a {'filter name': filtered array} dict
    saveAsImage(grid_dict, label)
        Saves the filtered Grid as image         
    """ 
    
    name = 'MultiChannelGrid'
    version = '0.1'   
                
    def __init__(self, image): 
        """
        Initializes an array from a multi channel image       
        
        Parameters
        ----------
        image : PIL.Image
            Multi channel image
        """
        self.array = np.asarray(image)
                              
    def splitFilter(self, gridFilter):
        """
        Applies the Split filter to a multiChannelGrid object (OR object based on derived classes)       
        
        Parameters
        ----------
        grid_filter : GridFilter
            GridFilter object holding its parameters            
        """
        height, width, rank = self.array.shape        
        red = np.zeros((height, width, rank))
        green = np.zeros((height, width, rank))
        blue = np.zeros((height, width, rank))                 
        red[:,:,0] = self.array[:,:,0]
        green[:,:,1] = self.array[:,:,1]
        blue[:,:,2] = self.array[:,:,2]        
        return {'red': red, 'green': green, 'blue': blue}
    
    def saveAsImage(self, grid_dict, label): 
        """
        Saves as 'RGB' mode image the filtered Grid array given by {'filter name': filtered array} dict      
        
        Parameters
        ----------
        grid_filter : BlurFilter
            Filter object holding its parameters  
        label : str
            Image name prefix
        """
        for k, channel in grid_dict.items():
            out_name = '{}{}{}'.format(label, k, '.png')
            img_path = os.getcwd()
            out_path_name = os.path.join(img_path, out_name)
            out_image = Image.fromarray(channel.astype('uint8'), mode='RGB')
            out_image.save(out_path_name)  



class GridFilter(object):
    """
    A filter base class
    """
    pass



class SplitFilter(GridFilter):
    """
    A class derived from GridFilter used to create SplitFilter objects
    """ 
    
    name = 'SplitFilter'
    version = '0.1'    
            
    def __init__(self):
        pass

    
    
class BlurFilter(GridFilter):
    """
    A class derived from GridFilter used to create BlurFilter objects
    """ 
    
    name = 'BlurFilter'
    version = '0.1'    
            
    def __init__(self, radius, weight):
        """
        Initializes BlurFilter       
        
        Parameters
        ----------
        radius : int
            Coverage parameter for getting a windows of closer pixels
        weight : int
            Multiplication factor for the centered pixel of the windows    
        """
        self.radius = radius
        self.weight = weight
        


def main(args):
    
    print('Image App Interface\n')
    
    # Loading image
    img_path = os.getcwd()
    img_name = args.img_name
    img_path_name = os.path.join(img_path, img_name)  
    image = Image.open(img_path_name)
    
    if(image.mode == 'L'):
        
        single_channel_grid = SingleChannelGrid(image)      
        print('Available filters for your image:\n1. Blur\n')
        filter_number = input('Type the selected filter number: ')
        
        if (filter_number == '1'):
            radius = int(input('Type the Blur radius: '))
            weight = int(input('Type the Blur weight: '))
            applied_filter = BlurFilter(radius, weight)    
            filtered_grid_dict = single_channel_grid.blurFilter(applied_filter)  
            label = '{}-radius:{}-weight:{}-'.format(image.mode, radius, weight) 
            single_channel_grid.saveAsImage(filtered_grid_dict, label)      
                
    else:  
        
        multi_channel_grid = MultiChannelGrid(image)
        print('Available filters for your image:\n1. Blur\n2. RGB Split\n')
        filter_number = input('Type the selected filter number: ')       
     
        if (filter_number == '1'):
            radius = int(input('Type the Blur radius: '))
            weight = int(input('Type the Blur weight: '))
               
            applied_filter = BlurFilter(radius, weight)    
            filtered_grid_dict = multi_channel_grid.blurFilter(applied_filter)  
            label = '{}-radius:{}-weight:{}-'.format(image.mode, radius, weight) 
            multi_channel_grid.saveAsImage(filtered_grid_dict, label)
            
        elif (filter_number == '2'):    
            applied_filter = SplitFilter()
            filtered_grid_dict = multi_channel_grid.splitFilter(applied_filter)
            label = '{}-'.format(image.mode)
            multi_channel_grid.saveAsImage(filtered_grid_dict, label)
        
        
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ESSS4 - OOP Applied to Image Filtering')   
    parser.add_argument(dest='img_name', type=str, help='Image file name (e.g. original.jpg)')   
    args = parser.parse_args()
    main(args)