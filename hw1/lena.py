import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def upside_down(img):
    
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    
    for i in range(height):
        new_img[i] = img[height - i - 1]
    
    return new_img.astype('uint8')

def rightside_left(img):
    
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    
    for i in range(width):
        for j in range(height):
            new_img[i][height - j - 1] = img[i][j]

    return new_img.astype('uint8')

def diagonally_mirrored(img):
    
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    
    for i in range(width):
        for j in range(height):
            new_img[j][i] = img[i][j]

    return new_img.astype('uint8')

if __name__ == '__main__':

	img = Image.open('lena.bmp')
	original_lena_plt = plt.imshow(np.asarray(img), cmap='gray', vmin=0, vmax=255)
	upside_down_img = Image.fromarray(upside_down(img), 'L')
	upside_down_img.save('upside-down-lena.bmp')
	upside_down_lena_plt = plt.imshow(np.asarray(upside_down_img), cmap='gray', vmin=0, vmax=255)
	rightside_left_img = Image.fromarray(rightside_left(img), 'L')
	rightside_left_img.save('rightside-left-lena.bmp')
	rightside_left_lena_plt = plt.imshow(np.asarray(rightside_left_img), cmap='gray', vmin=0, vmax=255)
	diagonally_mirrored_img = Image.fromarray(diagonally_mirrored(img), 'L')
	diagonally_mirrored_img.save('diagonally-mirrored-lena.bmp')
	diagonally_mirrored_lena_plt = plt.imshow(diagonally_mirrored(img), cmap='gray', vmin=0, vmax=255)



