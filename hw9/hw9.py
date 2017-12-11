import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
def get_value(img, x, y):
    height, width = img.shape
    img = np.asarray(img)
    if (x >= width) or (x < 0) or (y >= height) or (y < 0):
        return 0
    return img[x][y] / 255

def get_neighbor(img, origin, sizes):
    x = origin[0]
    y = origin[1]
    half = int(sizes[0]/2)
    neighbors = [[0 for i in range(sizes[0])] for j in range(sizes[1])]
    for i in range(-half,  half+1):
        for j in range(-half, half+1):
            neighbors[half + j][half + i] = get_value(img,x + j,y + i)
    return neighbors

def L2_norm_magnitude(n, masks, threshold):
    x_len = len(masks[0])
    y_len = len(masks[0][0])
    magnitude = []
    for k in range(len(masks)):
        r = 0
        for i in range(y_len):
            for j in range(x_len):
                r += n[j][i]*masks[k][j][i]
        magnitude.append(k**2)
    return (np.sqrt(sum(magnitude)) > threshold)

def max_magnitude(n, masks, threshold):
    x_len = len(masks[0])
    y_len = len(masks[0][0])
    magnitude = []
    for k in range(len(masks)):
        r = 0
        for i in range(y_len):
            for j in xrange(x_len):
                r += n[j][i]*masks[k][j][i]
        magnitude.append(r)
    return (max(magnitude) > threshold)

def roberts_detector(origin, img, threshold):
    masks = [[[-1, 0], [0, 1]], [[0, -1],[1, 0]]]
    n = []
    x = origin[0]
    y = origin[1]
    n.append([get_value(img, x, y), get_value(img, x+1, y)])
    n.append([get_value(img, x, y+1), get_value(img, x+1, y+1)])
    return 0 if L2_norm_magnitude(n, masks, threshold) is True else 255

def roberts_image(img, threshold):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(width):
        for j in range(height):
            new_img[i][j] = roberts_detector((i, j), img, threshold)
    return new_img.astype('uint8') 

def prewit_detector(origin, img, threshold):
    masks = [[[-1, -1, -1], [0, 0, 0], [1, 1, 1]], [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]]
    n = get_neighbor(img, origin, [3, 3])
    return 0 if L2_norm_magnitude(n, masks, threshold) is True else 255

def prewit_image(img, threshold):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(width):
        for j in range(height):
            new_img[i][j] = prewit_detector((i, j), img, threshold)
    return new_img.astype('uint8') 

def sobel_detector(origin, img, threshold):
    masks = [[[-1, -2, -1], [0, 0, 0], [1, 2, 1]], [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]]
    n = get_neighbor(img, origin, [3, 3])
    return 0 if L2_norm_magnitude(n, masks, threshold) is True else 255

def sobel_image(img, threshold):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(width):
        for j in range(height):
            new_img[i][j] = sobel_detector((i, j), img, threshold)
    return new_img.astype('uint8') 

def frei_and_chen_detector(origin, img, threshold):
    sqrt2 = np.sqrt(2)
    masks = [[[-1, -sqrt2, -1], [0, 0, 0], [1, sqrt2, 1]], [[-1, 0, 1], [-sqrt2, 0, sqrt2], [-1, 0, 1]]]
    n = get_neighbor(img, origin, [3, 3])
    return 0 if L2_norm_magnitude(n, masks, threshold) is True else 255

def frei_and_chen_image(img, threshold):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(width):
        for j in range(height):
            new_img[i][j] = frei_and_chen_detector((i, j), img, threshold)
    return new_img.astype('uint8') 

def kirsch_detector(origin, img, threshold):
    masks = [[[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]],
             [[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]],
             [[5, 5, 5], [-3, 0, -3], [-3, -3, -3]],
             [[5, 5, -3], [5, 0, -3], [-3, -3, -3]],
             [[5, -3, -3], [5, 0, -3], [5, -3, -3]],
             [[-3, -3, -3], [5, 0, -3], [5, 5, -3]],
             [[-3, -3, -3], [-3, 0, -3], [5, 5, 5]],
             [[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]]
    n = get_neighbor(img, origin, [3, 3])
    return 0 if max_magnitude(n, masks, threshold) is True else 255

def kirsch_image(img, threshold):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(width):
        for j in range(height):
            new_img[i][j] = kirsch_detector((i, j), img, threshold)
    return new_img.astype('uint8') 

def robinson_detector(origin, img, threshold):
    masks = [[[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
             [[0, -1, -2], [1, 0, -1], [2, 1, 0]],
             [[1, 0, -1], [2, 0, -2], [1, 0, -1]],
             [[2, 1, 0], [1, 0, -1], [0, -1, -2]],
             [[1, 2, 1], [0, 0, 0], [-1, -2, -1]],
             [[0, 1, 2], [-1, 0, 1], [-2, -1, 0]],
             [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
             [[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]]
    n = get_neighbor(img, origin, [3, 3])
    return 0 if max_magnitude(n, masks, threshold) is True else 255

def robinson_image(img, threshold):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(width):
        for j in range(height):
            new_img[i][j] = robinson_detector((i, j), img, threshold)
    return new_img.astype('uint8') 

def nevatiababu_detector(origin, img, threshold):
    masks = [[[100, 100, 0, -100, -100], [100, 100, 0, -100, -100], [100, 100, 0, -100, -100], [100, 100, 0, -100, -100], [100, 100, 0, -100, -100]],
    [[100, 100, 100, 32, -100], [100, 100, 92, -78, -100], [100, 100, 0, -100, -100], [100, 78, -92, -100, -100], [100, -32, -100, -100, -100]],
    [[100, 100, 100, 100, 100], [100, 100, 100, 78, -32], [100, 92, 0, -92, -100], [32, -78, -100, -100, -100], [-100, -100, -100, -100, -100]],
    [[-100, -100, -100, -100, -100], [-100, -100, -100, -100, -100], [0, 0, 0, 0, 0], [100, 100, 100, 100, 100], [100, 100, 100, 100, 100]],
    [[-100, -100, -100, -100, -100], [32, -78, -100, -100, -100], [100, 92, 0, -92, -100], [100, 100, 100, 78, -32], [100, 100, 100, 100, 100]],
    [[100, -32, -100, -100, -100], [100, 78, -92, -100, -100], [100, 100, 0, -100, -100], [100, 100, 92, -78, -100], [100, 100, 100, 32, -100]],]
    n = get_neighbor(img, origin, [5, 5])
    return 0 if max_magnitude(n, masks, threshold) is True else 255

def nevatiababu_image(img, threshold):
    height, width = img.size
    new_img = np.empty(shape=(height, width))
    img = np.asarray(img)
    for i in range(width):
        for j in range(height):
            new_img[i][j] = nevatiababu_detector((i, j), img, threshold)
    return new_img.astype('uint8') 
    
def main():
    img = Image.open('lena.bmp')
    plt.figure(1)
    original_lena_plt = plt.imshow(np.asarray(img), cmap='gray', vmin=0, vmax=255)
    
if __name__ == '__main__':
    main()