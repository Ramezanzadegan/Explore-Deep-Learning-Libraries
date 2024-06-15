import os.path
import json
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
import os 
from os import listdir
from os.path import join 
from PIL import ImageOps, Image
import random

# In this exercise task you will implement an image generator. Generator objects in python are defined as having a next function.
# This next function returns the next generated object. In our case it returns the input of a neural network each time it gets called.
# This input consists of a batch of images and its corresponding labels.
class ImageGenerator:
    def __init__(self, file_path, label_path, batch_size, image_size, rotation=False, mirroring=False, shuffle=False):
        # Define all members of your generator class object as global members here.
        # These need to include:
        # the batch size
        # the image size
        # flags for different augmentations and whether the data should be shuffled for each epoch
        # Also depending on the size of your data-set you can consider loading all images into memory here already.
        # The labels are stored in json format and can be directly loaded as dictionary.
        # Note that the file names correspond to the dicts of the label dictionary.

        self.class_dict = {0: 'airplane', 1: 'automobile', 2: 'bird', 3: 'cat', 4: 'deer', 5: 'dog', 6: 'frog',
                           7: 'horse', 8: 'ship', 9: 'truck'}
        #TODO: implement constructor
        self.file_path= os.path.join("data", file_path)
        self.label_path= os.path.join("data", label_path)
        self.batch_size= batch_size
        self.image_size= (image_size[0], image_size[0])
        self.rotation= rotation
        self.mirroring = mirroring
        self.shuffle= shuffle
        self.folder_list= listdir(self.file_path)
        self.number_of_epochs = 0
        #self.temp_list= list()
        #print ("obj_created")


    def next(self):
        # This function creates a batch of images and corresponding labels and returns them.
        # In this context a "batch" of images just means a bunch, say 10 images that are forwarded at once.
        # Note that your amount of total data might not be divisible without remainder with the batch_size.
        # Think about how to handle such cases
        #TODO: implement next method
        images = list()
        lables = list()


        with open(self.label_path) as jFile:
            json_data = json.load(jFile)

        

        for i in range (0, self.batch_size):
            if len(self.folder_list) == 0:
                #self.folder_list = self.temp_list
                #print(" list is updated! ")
                self.folder_list = listdir(self.file_path)
                self.number_of_epochs += 1
            
            if self.shuffle :
                random.shuffle(self.folder_list)


            temp = self.folder_list.pop(0)
            #self.temp_list.append(temp)

            img = np.load (join (self.file_path, temp))

            if ( img.shape[0] != self.image_size[0]):
                pil_image= Image.fromarray(img)
                rsz_pil_image= pil_image.resize(self.image_size)
                img= np.array(rsz_pil_image)

            
            if(self.mirroring == True):
                img=self.augment(img)

            if(self.rotation== True):
                img= self.augment(img)


            images.append(img)
            
            
            file_name= temp.split('.')[0]
            label= json_data[file_name]
            lables.append(label)


        return np.array(images), lables

    def augment(self,img):
        # this function takes a single image as an input and performs a random transformation
        # (mirroring and/or rotation) on it and outputs the transformed image
        #TODO: implement augmentation function
       
            
        if(self.mirroring == True):
            if np.random.rand() < .5 :
                pil_img_M =  Image.fromarray(img)
                mirr_pil_img =  ImageOps.mirror(pil_img_M)
                modified_img = np.array(mirr_pil_img)
            else:
                modified_img = img 
        
        if(self.rotation== True):
            pil_image= Image.fromarray(img)
            x = np.random.rand()
            if  x <= 0.3 :
                rotated_image1 = pil_image.rotate(90)
                    
            elif 0.3 < x and x <= 0.6 :
                rotated_image1 = pil_image.rotate(180)

            elif 0.6 < x and x <= 1 :
                rotated_image1 = pil_image.rotate(270)
            modified_img= np.array(rotated_image1)

        
        return modified_img

    def class_name(self, x):
        # This function returns the class name for a specific input
        #TODO: implement class name function
        
        name= self.class_dict[x]

        return name
            
        
    def show(self):
        # In order to verify that the generator creates batches as required, this functions calls next to get a
        # batch of images and labels and visualizes it.
        #TODO: implement show method
        
        images, labels = self.next()

        fig=plt.figure(figsize=(16, 12))
        columns = 3
        rows= np.ceil(self.batch_size / columns )
        for z in range (1, len(images) +1 ):
            a= fig.add_subplot(rows, columns, z)
            a.imshow(images[z-1])
            a.set_title(self.class_name (labels[z-1]) )

        plt.show()

        return
    
    def current_epoch(self):
        # return the current epoch number
        return self.number_of_epochs





