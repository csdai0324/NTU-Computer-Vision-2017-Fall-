import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

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

def dilation(img, kernel):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(height):
        for j in range(width):
            if img[i][j] > 0:
                maximum = 0
                for ele in kernel:
                    p, q = ele
                    if (i + p) >= 0 and (i + p) <= (width - 1) and \
                       (j + q) >= 0 and (j + q) <= (height - 1):
                        if img[i + p][j + q] > max_value:
                            maximum = img[i + p][j + q]
                for ele in kernel:
                    p, q = ele
                    if (i + p) >= 0 and (i + p) <= (width - 1) and \
                       (j + q) >= 0 and (j + q) <= (height - 1):
                        new_img[i + p][j + q] = maximum
    return new_img.astype('uint8')  

def erosion(img, kernel):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(height):
        for j in range(width):
            if img[i][j] > 0:
                flag = True
                minimun = np.inf
                for ele in kernel:
                    p, q = ele
                    if (i + p) >= 0 and (i + p) <= (height - 1) and \
                       (j + q) >= 0 and (j + q) <= (width - 1):
                        if img[i + p][j + q] == 0:
                            flag = False
                            break
                        if img[i + p][j + q] < minimun:
                            minimun = img[i + p][j + q]
                flag = True
                for ele in kernel:
                    p, q = ele
                    if (i + p) >= 0 and (i + p) <= (height - 1) and \
                       (j + q) >= 0 and (j + q) <= (width - 1):
                        if img[i + p][j + q] == 0:
                            flag = False
                            break
                    if (i + p) >= 0 and (i + p) <= (height- 1) and \
                       (j + q) >= 0 and (j + q) <= (width - 1) and \
                       flag:
                        new_img[i + p][j + q] = minimun
    return new_img.astype('uint8')

def closing(img, kernel):
    dilation_img = dilation(img, kernel)
    closing_img = erosion(Image.fromarray(dilation_img), kernel)
    return closing_img.astype('uint8')

def opening(img, kernel):
    erosion_img = erosion(img, kernel)
    opening_img = dilation(Image.fromarray(erosion_img), kernel)
    return opening_img.astype('uint8')

def hit_and_miss_transform(img, kernel):
    height, width = img.size
    new_img = np.empty(shape=(height, width)) 
    img = np.asarray(img)
    complement_img = -(img - 255)
    J_kernel, K_kernel = kernel
    erosion_img1 = erosion(Image.fromarray(img), J_kernel)
    erosion_img2 = erosion(Image.fromarray(complement_img), K_kernel)
    for i in range(height):
        for j in range(width):
            if erosion_img1[i][j] == 0 and erosion_img2[i][j] == 0:
                new_img[i][j] = 255
    return new_img.astype('uint8')

def main():
	# 3-5-5-5-3 octagon kernel process on white pixel
	kernel = [[-2, -1], [-2, 0], [-2, 1],
	          [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], 
	          [0, -2], [0, -1], [0, 0], [0, 1], [0, 2],
	          [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
	          [2, -1], [2, 0], [2, 1]]
	img = Image.open('lena.bmp')
	#plt.figure(1)
	#fig = plt.imshow(np.asarray(img), cmap='gray', vmin=0, vmax=255)
	dilation_img = Image.fromarray(dilation(img, kernel))
	dilation_img.save('dilation_lena.bmp')
	erosion_img = Image.fromarray(erosion(img, kernel))
	erosion_img.save('erosion_lena.bmp')
	closing_img = Image.fromarray(closing(img, kernel))
	closing_img.save('closing_lena.bmp')
	opening_img = Image.fromarray(opening(img, kernel))
	opening_img.save('opening_img.bmp')

if __name__ == '__main__':
	main()