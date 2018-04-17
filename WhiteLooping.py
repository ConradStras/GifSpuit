import cv2
import numpy as np
import cython
white = (255, 255, 255)
red = (0, 0, 255)

# generating the arrays that resemble a line through the image
# we cannot enter tuples into np.arange
# this code definitely requires optimizing

def whiteindex(image):
    w = image.shape[1]
    h = image.shape[0]
    indexes = []
    #just take note x and y are swapped during the looping process
    ##!! Key Parameters This denotes the steppage, i.e. every nth (in this case 100th of the image, meaning
    #it will jump 5 pixels down and 6 pixels across every yth and xth [respectively] iteration) pixel of the
    #image gets sampled
    stepdown = int(1 / 100 * h)
    stepacross = int(1 / 100 * w)
    ##!! Key Parameters above
    for y in range(0, h, stepdown):
        for x in range(0, w, stepacross):
            if image[y, x] == 255 and (1 / 10) * h < y < h - (1 / 10) * h:
                indexes.append((y, x))
    return indexes

def clusters(indexes, image):
    w = image.shape[1]
    clustersindices = []
    h = image.shape[0]
    for j in indexes:
        ccount = 0
        y = j[0]
        x = j[1]
    # exception handling, i.e when a range lies within 6 of the edge of the image
        for k in range(y, y + int(h*1/100)-1):
            for i in range(x, x+int(w*1/100)-1):
                if image[k, i] == 255:
                    ccount = ccount + 1
        ##!! Key Parameter, this determines whether the amount of green present in a block is worthy of being a cluster
        threshold = int(1/30*(h*1/100*w*1/100))
        ##!! Key Parameter above
        if ccount > threshold:
            clustersindices.append(((y, x), (y+int(h*1/100), x+int(w*1/100))))
    return clustersindices