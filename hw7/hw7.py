import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

downsample_size = [64, 64]

def binarize(img, threshold):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(width):
        for j in range(height):
            if img[i][j] > 128:
                new_img[i][j] = 255
            else:
                new_img[i][j] = 0
                
    return new_img.astype('uint8')

def downsample(img):
    height, width = downsample_size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(width):
        for j in range(height):
            new_img[i][j] = img[i*8][j*8]
    
    return new_img.astype('uint8') 

def get_value(img, x, y):
    height, width = downsample_size
    img = np.asarray(img)
    if (x >= width) or (x < 0) or (y >= height) or (y < 0):
        return 0
    return img[x][y] / 255

def get_neighbor(img, x, y):
    return [get_value(img, x, y), get_value(img, x+1, y), get_value(img, x, y-1),   
            get_value(img, x-1,y), get_value(img, x,y+1), get_value(img, x+1, y+1), 
            get_value(img, x+1,y-1), get_value(img, x-1,y-1), get_value(img, x-1 ,y+1)]

def check(n):
    counter = 0
    local = list(n)
    del local[0]
    local.append(local[0])
    for i in range(0, len(local)):
        if i+1 < len(local):
            if local[i] < local[i+1] :
                counter += 1
    if counter == 1:
        return True
    else:
        return False

def first_thinning(n):
    if sum(n)-n[0] >= 2 and sum(n)-n[0] <=6 and check(n):
        if(n[1]*n[3]*n[5] == 0 and n[3]*n[5]*n[7] == 0 ):
            return True
    return False

def second_thinning(n):
    if sum(n)-n[0] >= 2 and sum(n)-n[0] <=6 and check(n):
        if(n[1]*n[3]*n[7] == 0 and n[1]*n[5]*n[7] == 0 ):
            return True
    return False    
   
def thinning(img):
    height, width = downsample_size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    counter = 0
    while True:
        counter += 1
        not_change = True
        delete = []
        for x in range(width):
            for y in range(height):
                if img[x][y]:
                    if first_thinning(get_neighbor(img, x, y)):
                        delete.append((x, y))
                        not_change = False
        for pixel in delete:
            new_img[pixel[0]][pixel[1]] = 0
            del pixel
        for x in range(width):
            for y in range(height):
                if img[x][y]:
                    if second_thinning(get_neighbor(img, x, y)):
                        delete.append((x, y))
                        notChange = False
        for pixel in delete:
            new_img[pixel[0]][pixel[1]] = 0
            del pixel
        if(not_change):
            break
    return new_img.astype('uint8') 
    
def main():
    img = Image.open('lena.bmp')
    plt.figure(1)
    original_lena_plt = plt.imshow(np.asarray(img), cmap='gray', vmin=0, vmax=255)
    plt.figure(2)
    binarized_downsample_img = Image.fromarray(downsample(binarize(img, 128)), 'L')
    binarized_downsample_img.save('binarized-downsample-lena.bmp')
    binarized_downsample_lena_plt = plt.imshow(np.asarray(binarized_downsample_img), cmap='gray', vmin=0, vmax=255)
    plt.figure(3)
    thinning_img = thinning(downsample(binarize(img, 128)))
    thinning_lena_plt = plt.imshow(np.asarray(thinning_img), cmap='gray', vmin=0, vmax=255)

if __name__ == '__main__':
    main()