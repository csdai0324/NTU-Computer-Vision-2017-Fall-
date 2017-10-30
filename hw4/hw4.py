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
                for ele in kernel:
                    a = i + ele[0]
                    b = j + ele[1]
                    if a >= 0 and a <= (height - 1) and \
                       b >= 0 and b <= (width - 1):
                        new_img[a][b] = 255 
    return new_img.astype('uint8')  

def erosion(img, kernel):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(height):
        for j in range(width):
            if img[i][j] > 0:
                flag = True
                for ele in kernel:
                    a = i + ele[0]
                    b = j + ele[1]
                    if a < 0 or a > (height - 1) or \
                       b < 0 or b > (width - 1) or img[a][b] == 0:
                        flag = False
                        break
                    if flag == True:
                        new_img[a][b] = 255
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
	binarized_img = Image.fromarray(binarize(img, 128), 'L')
	binarized_img.save('binarized-lena.bmp')
	dilation_img = Image.fromarray(dilation(binarized_img, kernel))
	dilation_img.save('dilation_lena.bmp')
	erosion_img = Image.fromarray(erosion(binarized_img, kernel))
	erosion_img.save('erosion_lena.bmp')
	closing_img = Image.fromarray(closing(binarized_img, kernel))
	closing_img.save('closing_lena.bmp')
	opening_img = Image.fromarray(opening(binarized_img, kernel))
	opening_img.save('opening_img.bmp')
	J_kernel = [[0, -1], [0, 0], [1, 0]]
	K_kernel = [[-1, 0], [-1, 1], [0, 1]]
	kernel = [J_kernel, K_kernel]
	output_img = Image.fromarray(hit_and_miss_transform(binarized_img, kernel))
	output_img.save('hit_and_miss.bmp')

if __name__ == '__main__':
	main()