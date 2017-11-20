import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

downsample_size = [64, 64]
output_path = 'result.txt'

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
    height, width = img.size
    img = np.asarray(img)
    if (x >= width) or (x < 0) or (y >= height) or (y < 0):
        return 0
    return img[x][y]

def get_neighbor(img, x, y):
    return [get_value(img, x, y), get_value(img, x+1, y), get_value(img, x, y-1),   
            get_value(img, x-1,y), get_value(img, x,y+1), get_value(img, x+1, y+1), 
            get_value(img, x+1,y-1), get_value(img, x-1,y-1), get_value(img, x-1 ,y+1)]

def h(b, c, d, e):
    if b == c and (d!=b or e!=b):
        return 'q'
    elif b == c and (d==b or e==b):
        return 'r'
    elif b != c:
        return 's'

def f(a1, a2, a3, a4):
    n = [a1, a2, a3, a4]
    if n.count('r') == len(n): 
        return 5
    else:
        return n.count('q')

def Yokoi(n):
    return f(h(n[0], n[1], n[6], n[2]), 
             h(n[0], n[2], n[7], n[3]), 
             h(n[0], n[3], n[8], n[4]), 
             h(n[0], n[4], n[5], n[1]))

def find_matrix(img):
    height, width = downsample_size
    matrix = np.empty(shape=(height, width))
    _img = np.asarray(img)
    for i in range(width):
        for j in range(height):
            if _img[i][j] != 0:
                matrix[i][j] = Yokoi(get_neighbor(img, i, j))
                
    return matrix.astype('uint8') 

def write_matrix(matrix, output_path):
    if os.path.isfile(output_path):
        os.remove(output_path)
    with open('result.txt', 'a') as output:
        height, width = matrix.shape
        for i in range(height):    
            for j in range(width):
                if matrix[i][j] > 0:
                    output.write(str(matrix[i][j]))
                elif matrix[i][j] == 0:
                    output.write(' ')
            output.write('\r\n')

def main():
    img = Image.open('lena.bmp')
    plt.figure(1)
    original_lena_plt = plt.imshow(np.asarray(img), cmap='gray', vmin=0, vmax=255)
    plt.figure(2)
    downsample_img = Image.fromarray(downsample(img), 'L')
    downsample_img.save('downsample-lena.bmp')
    downsample_lena_plt = plt.imshow(np.asarray(downsample_img), cmap='gray', vmin=0, vmax=255)
    plt.figure(3)
    binarized_downsample_img = Image.fromarray(downsample(binarize(img, 128)), 'L')
    binarized_downsample_img.save('binarized-downsample-lena.bmp')
    binarized_downsample_lena_plt = plt.imshow(np.asarray(binarized_downsample_img), cmap='gray', vmin=0, vmax=255)
    matrix = find_matrix(binarized_downsample_img)
    write_matrix(matrix, output_path)

if __name__ == '__main__':
    main()