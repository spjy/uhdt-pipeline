#
#  Use k-means clustering to find the most-common colors in an image
#
import cv2, time
import numpy as np
from sklearn.cluster import KMeans

# Class definition
def make_histogram(cluster):
    """
    Count the number of pixels in each cluster
    :param: KMeans cluster
    :return: numpy histogram
    """
    numLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    hist, _ = np.histogram(cluster.labels_, bins=numLabels)
    hist = hist.astype('float32')
    hist /= hist.sum()
    return hist


def make_bar(height, width, color):
    """
    Create an image of a given color
    :param: height of the image
    :param: width of the image
    :param: BGR pixel values of the color
    :return: tuple of bar, rgb values, and hsv values
    """
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    hsv_bar = cv2.cvtColor(bar, cv2.COLOR_BGR2HSV)
    hue, sat, val = hsv_bar[0][0]
    return bar, (red, green, blue), (hue, sat, val)


def sort_hsvs(hsv_list):
    """
    Sort the list of HSV values
    :param hsv_list: List of HSV tuples
    :return: List of indexes, sorted by hue, then saturation, then value
    """
    bars_with_indexes = []
    for index, hsv_val in enumerate(hsv_list):
        bars_with_indexes.append((index, hsv_val[0], hsv_val[1], hsv_val[2]))
    bars_with_indexes.sort(key=lambda elem: (elem[1], elem[2], elem[3]))
    return [item[0] for item in bars_with_indexes]

def find_color(hsv_val):
    """
    Translate the HSV values to a color if it fits in a specific color range
    :param hsv_val: The HSV values
    :return: The color that the HSV value translates to.
    """
    H = hsv_val[0]
    S = hsv_val[1]
    V = hsv_val[2]
    color = None
    
    if V<=10: color = "Black"
    #elif S<=10:
    #    if V>30 and V<=80: color = "Gray"
    #    elif V>=70 and V<=100: color = "White"
    elif H<10:
        if S>30 and V>50: color = "Red"
        #else: color = "White"
    elif H>=10 and H<30:
        if H>=20 and H<30:
            if S>=10: color = "Orange"
        if S>=10 and S<20:
            if V>=50: color = "Brown"
        elif S>60 and S<=70: color = "Orange"
        elif S>=40:
            if V>=40 and V<=70: color = "Brown"
            else: color = "Orange"
    elif H>=30 and H<=50:
        if S<=20 and V<=60: color = "Gray"
        elif S>=30 and V>=50: color = "Brown"
        if S>15:
            if V>60: color = "White"
        if S>= 80:
            if V >= 90: color = "Orange"
            elif V <= 80: color = "Brown"
        elif S>=40 and S<=60:
            if V>=80: color = "Purple"
        else:
            if V>=70: color = "White"
    elif H>50 and H<=60:
        if S <= 20:
            if V>=20 and V<90: color = "Gray"
            elif V>=90: color = "White"
        if S>=50:
            if V>=50 and V<90: color = "Yellow"
            elif V>=90: color = "White"
    #skipping H between 60 and 100, colors look like grass
    elif H>=100 and H<=150:
        if S>50 and V>50: color = "Green"
    elif H>160 and H<200:
        if S>=25 and V>=30: color = "Blue"
        else: color = "Gray"
    elif H>=200 and H<=250:
        if S<=10:
            if V>=70: color = "White"
        if S>=30:
            if V>=30: color = "Blue"
    elif H>250 and H<=340:
        if S>=15:
            if V>=30: color = "Purple"
        elif S>=20: color = "Brown"
    elif H>340 and H<=360:
        if S>=20 and V>=50: color = "Red"
    return color

# Main code starts here
def main(filename):
    #reads image and gets image pixel shape
    
    #filename = directory + '\DSC_' + str(index) + '.jpg'
#   filename = r'C:\Users\UHDT\Pictures\Test Targets' + '/DSC_0' + str(index) + '.jpg'
    img = cv2.imread(filename)
    height, width, _ = np.shape(img)

    #Crops images to get the center plus and minus 25 pixels from center
    width_center = width/2
    height_center = height/2

#    if(shape == "star"):
#        startingX = int(width_center -60)
#        startingY = int(height_center - 60)
#        endingX = int(width_center + 60)
#        endingY = int(height_center + 60)
#    elif(shape == "cross"):
#        startingX = int(width_center -50)
#        startingY = int(height_center - 50)
#        endingX = int(width_center + 50)
#        endingY = int(height_center + 50)

    startingX = int(width_center - 60)
    startingY = int(height_center - 65)

    endingX = int(width_center + 60)
    endingY = int(height_center + 60)

    crop_img = img[startingX:endingX, startingY:endingY]


    #Shows cropped image
    #cv2.imshow('crop_img', crop_img)

    # reshape the image to be a simple list of RGB pixels
    image = crop_img.reshape((-1, 3))

    # Gets the two most dominant colors
    num_clusters = 2
    clusters = KMeans(n_clusters=num_clusters)
    clusters.fit(image)

    # count the dominant colors and put them in "buckets"
    histogram = make_histogram(clusters)
    # then sort them, most-common first
    combined = zip(histogram, clusters.cluster_centers_)
    combined = sorted(combined, key=lambda x: x[0], reverse=True)

    #sprint(*combined)
    # finally, we'll output a graphic showing the colors in order
    bars = []
    hsv_values = []
    rgb_values = []
    for index, rows in enumerate(combined):
        bar, rgb, hsv = make_bar(100, 100, rows[1])

        #prints RGB values
    #    print(f'Bar {index + 1}')
    #    print(f'  RGB values: {rgb}')
        #print(hsv)
    #    print(*rgb)
        #HSV values then need to be multiplied by (2, 1/2.55, 1/2.55)
    #    print(*hsv)
    #    print(f'  HSV values: {hsv}')
        hsv_values.append(hsv)
        bars.append(bar)

    #print(hsv_values[0])
    #print(hsv_values[1])

    #Gets the color for the shape color
    dominant_color = [0] * 3
    dominant_color[0] = hsv_values[0][0] * 2
    dominant_color[1] = hsv_values[0][1] / 2.55
    dominant_color[2] = hsv_values[0][2] / 2.55
    print(dominant_color)
    shape_color = find_color(dominant_color)
    print("Primary color = ",shape_color)

    #Gets the color of alpahnumeric color
    secondary_color = [0] * 3
    secondary_color[0] = hsv_values[1][0] * 2
    secondary_color[1] = hsv_values[1][1] / 2.55
    secondary_color[2] = hsv_values[1][2] / 2.55
    print(secondary_color)
    alpha_color = find_color(secondary_color)
    print("Secondary color = ", alpha_color)


    # sort the bars[] list so that we can show the colored boxes sorted
    # by their HSV values -- sort by hue, then saturation
    sorted_bar_indexes = sort_hsvs(hsv_values)
    sorted_bars = [bars[idx] for idx in sorted_bar_indexes]

    #cv2.imshow('Sorted by HSV values', np.hstack(sorted_bars))
    #cv2.imshow(f'{num_clusters} Most Common Colors', np.hstack(bars))
    #cv2.waitKey(0)
    print("\n")
        
    colors = {
        "shape_color": shape_color,
        "alphanumeric_color": alpha_color
    }

    return colors

#start and ending indices
# start = 3358
# end = 3367

# #change directory accordingly
# directory = r"C:\Users\UHDT\Pictures\Test Targets"
# main(3358, directory)
#while(start <= end):
#    main(start, directory)
#    start += 1

#while start <= end:
#    if(start < 10): index = "00" + str(start)
#    elif(start < 100): index = "0" + str(start)
#    else: index = str(start)
#    main(index, directory)
#    start += 1