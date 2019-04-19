import cv2
from matplotlib import pyplot as plt
from collections import Counter
import numpy as np



def preprocess1(image):
    img = cv2.imread(image)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    img = cv2.bitwise_not(img)
    th2 = cv2.adaptiveThreshold(img,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,15,-2)
    #cv2.imshow("th2", th2)
    #cv2.imwrite("th2.jpg", th2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    horizontal = th2
    vertical = th2
    rows, cols = horizontal.shape

    #inverse the image, so that lines are black for masking
    horizontal_inv = cv2.bitwise_not(horizontal)
    #perform bitwise_and to mask the lines with provided mask
    masked_img = cv2.bitwise_and(img, img, mask=horizontal_inv)
    #reverse the image back to normal
    masked_img_inv = cv2.bitwise_not(masked_img)
    horizontalsize = int(cols / 30)
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize,1))
    horizontal = cv2.erode(horizontal, horizontalStructure, (-1, -1))
    horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, -1))

    print('Creating bars.png')

    horizontal_not = cv2.bitwise_not(horizontal)

    cv2.imwrite('bars.png',horizontal_not)
    #cv2.imshow('horizontal', horizontal)
    #cv2.waitKey(0)

    verticalsize = int(rows / 30)
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
    vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
    vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))

    vertical = cv2.bitwise_not(vertical)

    #step1
    # edges = cv2.adaptiveThreshold(vertical,255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,-2)
    #     #
    #     # #step2
    #     # kernel = np.ones((2, 2), dtype = "uint8")
    #     # dilated = cv2.dilate(edges, kernel)
    #     # # step3
    smooth = vertical.copy()
    #     # #step 4
    smooth = cv2.blur(smooth, (4,4))

    #step 5
    (rows, cols) = np.where(img == 0)
    vertical[rows, cols] = smooth[rows, cols]
    #cv2.imshow("vertical_final", vertical)
    #cv2.imwrite("vertical_final.jpg", vertical)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    print('returning vertical')

    return vertical


def preprocess(img, old=False):
    image = cv2.imread(img,0)
    image = cv2.fastNlMeansDenoising(image, None, 10, 7, 21)

    retval, img = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #cv2.imwrite('binarized.jpg', image)

    return img


def get_line_info(image):
    '''
    Detect line width, line spacing using run length encoding
    :param image:
    :return:
    '''
    n_rows = image.shape[0] #height pixels
    n_cols = image.shape[1] #width pixels

    cum_white_runs = [] #cumulative white run
    cum_black_runs = [] #cumulative black run
    sum_all_runs = []

    for i in range(n_cols): #look at columns 0----->
        column = image[:, i]
        runlen_col = []
        runlen_white = []
        runlen_black = []
        current_run = 0

        run_pixel = column[0]
        for j in range(n_rows): #look at rows w/in column
            if (column[j] == run_pixel): #if maintain same pixel color, continue run
                current_run+=1
            else: #else append run to specific color and continue with next run
                runlen_col.append(current_run)
                if(run_pixel==0):
                    runlen_black.append(current_run)
                else:
                    runlen_black.append(current_run)

                run_pixel = column[j]
                current_run = 1
        runlen_col.append(current_run)
        if(run_pixel == 0):
            runlen_black.append(current_run)
        else:
            runlen_white.append(current_run)

        sum_ = [sum(runlen_col[i: i + 2]) for x in range(len(runlen_col))]

        cum_black_runs.extend(runlen_black)
        cum_white_runs.extend(runlen_white)
        sum_all_runs.extend(sum_)

    black_runs = Counter(cum_black_runs)
    white_runs = Counter(cum_white_runs)

    line_spacing = white_runs.most_common(1)[0][0]
    line_thickness = black_runs.most_common(1)[0][0]

    return line_spacing, line_thickness


def retrieve_staff_area(img, bars, line_thickness):
    '''
    This function takes the original image, and the hough transformed image which contains only the barlines. It then generates the y values by starting in the top of the middle of the bar image and
    iterating downwards. Each time it reaches a barline, the location is cached. When this is finished the file is then read and the x location is found.
    :param img:
    :param bars:
    :param line_thickness:
    :return: cartesian_start_points, cartesian_end_points
    '''
    n_rows = img.shape[0]
    n_cols = img.shape[1]

    b_rows = bars.shape[0]
    b_cols = bars.shape[1]

    #print(f'bars rows = {b_rows}')
    #print(f'bars cols = {b_cols}')

    row_black_pixel_histogram = []  # create running tally of black pixels
    bars_black_pixel_histogram = []

    for i in range(n_rows):  # for each row in each column, check for black pixels, add at row location
        row = img[i]
        num_black_pixels = 0
        for j in range(len(row)):
            if (row[j] == 0):
                num_black_pixels += 1

        row_black_pixel_histogram.append(num_black_pixels)

    for x in range(b_rows):  # for each row in each column, check for black pixels, add at row location
        row = bars[x]
        num_black_pixels = 0
        for y in range(len(row)):
            if (row[y] == 0):
                num_black_pixels += 1

        bars_black_pixel_histogram.append(num_black_pixels)

    #print('bars_histogram:')
    #for i in range(len(bars_black_pixel_histogram)):
     #   print(f'{bars_black_pixel_histogram[i]}\t{row_black_pixel_histogram[i]}\t{i}')

    mid_loc = b_cols//2
    hit_location = []
    counter = 0

    for i in range(n_rows):
        if (bars[i][mid_loc] == 0):
            #print('--------------------------------------------')
            hit_location.append(i)

        else:
            pass
            #print(i)
    #print(hit_location)

    mark_for_delete = []


    for i in hit_location:
        if i+1 in hit_location:
            mark_for_delete.append(i+1)
    #print(mark_for_delete)

    hits = []

    for i in hit_location:
        if i not in mark_for_delete:
            hits.append(i)
    #print(hits)

    x_values = []

    for i in range(0,len(hits)):
        #print(hits[i])
        for j in range(len(bars[hits[i]])):
            if(bars[hits[i]][j] == 0):
                x_values.append(j)
                #print(f'y: {hits[i]}, x: {j}')
                break

    #print(x_values)


    cartesian_start_points = list(zip(x_values,hits))

    #print(cartesian_start_points)

    end_x_values = []

    for i in range(0,len(hits)):
        #print(hits[i])
        for j in reversed(range(0,len(bars[hits[i]]))):

            if(bars[hits[i]][j] == 0):
                end_x_values.append(j)
                #print(f'y: {hits[i]}, x: {j}')
                break

    cartesian_end_points = list(zip(end_x_values,hits))


    return cartesian_start_points, cartesian_end_points


    #print(set(x_values))

    #plt.plot(row_black_pixel_histogram)
    #plt.show()
    #plt.plot(bars_black_pixel_histogram)
    #plt.show()



