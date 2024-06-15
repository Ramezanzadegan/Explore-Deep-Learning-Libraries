import os.path
import json
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize 
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
        self.file_path = os.path.join('data', file_path)
        self.label_path = os.path.join('data', label_path)
        self.batch_size = batch_size
        self.image_size = image_size
        self.rotation = rotation
        self.mirroring = mirroring
        self.shuffle = shuffle
        self.pointer = 0
        self.mirroring_or_rotating = None
        self.img_list = os.listdir(self.file_path) 
        self.img_list_back_up = list()
        self.imgs_in_one_batch = list()
        self.number_of_epochs = 0
        self.next_function_counter = 0




    def next(self):
        # This function creates a batch of images and corresponding labels and returns them.
        # In this context a "batch" of images just means a bunch, say 10 images that are forwarded at once.
        # Note that your amount of total data might not be divisible without remainder with the batch_size.
        # Think about how to handle such cases
        #TODO: implement next method
        images = list()
        labels = list()
        imgs_in_one_batch = list()

        if 100//self.batch_size < self.next_function_counter:
            self.number_of_epochs +=1
            self.next_function_counter = 0




        if self.shuffle :
            np.random.shuffle(self.img_list)


        if self.batch_size < len(self.img_list):
            imgs_in_one_batch = self.img_list[0:self.batch_size]
            self.img_list = self.img_list[self.batch_size:]
            self.img_list_back_up += imgs_in_one_batch
            self.next_function_counter +=1
           


        

        if self.batch_size >= len(self.img_list):
            imgs_in_one_batch = self.img_list[:]
            self.img_list_back_up += self.img_list[:]
            imgs_in_one_batch += self.img_list_back_up[:self.batch_size - len(self.img_list)]
            self.img_list = self.img_list_back_up
            self.img_list_back_up = list()
            self.next_function_counter += 1
        
         
    


        

        with open(self.label_path) as jFile:
            json_data = json.load(jFile)
        
        
        images = np.array([np.load ( os.path.join (self.file_path, img)) for img in imgs_in_one_batch]) 
        labels = np.array([json_data[img.split(".")[0]] for img in imgs_in_one_batch])

        height , width = self.image_size[0],self.image_size[1]

        if images[:].shape[1] != height or images[:].shape[2] != width:
            images =  resize(images,(images[:].shape[0],height,width,images[:].shape[3]),anti_aliasing=True)


        if self.rotation:
            self.mirroring_or_rotating = "rotation"
            random = np.random.rand(self.batch_size)<.5
            indices_of_true = np.where(random)[0]
            for index in indices_of_true:
                images[index] = self.augment(images[index])

        if self.mirroring:
            self.mirroring_or_rotating = "mirroring"
            random = np.random.rand(self.batch_size)<.5
            indices_of_true = np.where(random)[0]
            for index in indices_of_true:
                images[index] = self.augment(images[index])


        

        
        return images,labels

    def augment(self,img):
        # this function takes a single image as an input and performs a random transformation
        # (mirroring and/or rotation) on it and outputs the transformed image
        #TODO: implement augmentation function
        if self.mirroring_or_rotating == "mirroring":
            modified_img = np.fliplr(img)
        
        if self.mirroring_or_rotating == "rotation":
            random = np.random.choice(["rotation_90","rotation_180","rotation_270"])
            if random == "rotation_90":
                modified_img = np.rot90(img)

            elif random == "rotation_180":
                modified_img = np.rot90(img,2)

            elif random == "rotation_270":
                modified_img = np.rot90(img,3)
                

        return modified_img

    def current_epoch(self):
        # return the current epoch number
        return self.number_of_epochs

    def class_name(self, x):
        # This function returns the class name for a specific input
        #TODO: implement class name function
        return self.class_dict[x]
    

    def show(self):
        # In order to verify that the generator creates batches as required, this functions calls next to get a
        # batch of images and labels and visualizes it.
        #TODO: implement show method
        images, labels = self.next()

        fig=plt.figure(figsize=(16, 12))
        columns = 3
        rows= int(np.ceil(self.batch_size / columns ))
        for z in range (1, len(images) +1 ):
            a= fig.add_subplot(rows, columns, z)
            a.imshow(images[z-1])
            a.set_title(self.class_name (labels[z-1]) , color = "red" )
            plt.axis('off')

        plt.show()

        pass

