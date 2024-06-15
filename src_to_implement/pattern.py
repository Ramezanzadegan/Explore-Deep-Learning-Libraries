import numpy as np
import matplotlib.pyplot as plt
import copy


class Checker :
    def __init__(self, resolution, tile_size):
        self.resolution= resolution
        self.tile_size= tile_size
        self.output=np.ones((resolution,resolution))
        self.x, self.y = np.meshgrid(np.arange(0,resolution), np.arange(0,resolution))
        return 

    def draw(self):
        maskx=np.floor(self.x/ self.tile_size) % 2 ==0
        masky=np.floor(self.y/ self.tile_size) % 2 ==0
        self.output[maskx == masky] = 0
        return copy.deepcopy(self.output)

    def show(self):
        self.draw()
        plt.imshow(self.output, cmap='gray')
        plt.show()
        return


class Circle:
    def __init__(self, resolution: int, radius: int, position: tuple):
        self.resolution = resolution
        self.radius = radius
        self.position = position
        self.output = None

    def draw(self):
        x, y = np.meshgrid(np.arange(self.resolution), np.arange(self.resolution))
        self.output = (x - self.position[0]) ** 2 + (y - self.position[1]) ** 2 <= self.radius ** 2
        return copy.deepcopy(self.output)

    def show(self):
        self.draw()
        plt.imshow(self.output, cmap="gray")
        plt.show()


class Spectrum:
    def __init__(self, resolution: int):
        self.resolution = resolution
        self.output = None

    def draw(self):
        self.output = np.zeros((self.resolution, self.resolution, 3))
        self.output[:, :, 0] = np.linspace(0, 1, self.resolution)
        self.output[:, :, 2] = np.linspace(1, 0, self.resolution)
        self.output[:, :, 1] = np.rot90(self.output[:, :, 2])
        return copy.deepcopy(self.output)

    def show(self):
        self.draw()
        plt.imshow(self.output) 
        plt.show()
