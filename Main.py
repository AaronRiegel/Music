import matplotlib.pyplot as plt
import cv2 as cv
import ImageConverter as ic
import ImageTools as it
from BoundingBox import BoundingBox

import os

#windows_path = PureWindowsPath(filename)


class Main:
    filename = "resources/examples/Twinkle.png"
    f = ic.convertImage(filename)
    filename = "out.png"
    img0 = cv.imread(filename)
    print('got to line 18')

    it.preprocess1(filename)

    img = it.preprocess(filename)
    print(f'finished preprocessing {filename}')
    bars = it.preprocess('bars.png')

    line_spacing, line_thickness = it.get_line_info(img)

    print(f'filename {filename}: line spacing = {line_spacing}\tline thickness = {line_thickness}')

    #all_staffline_vertical_indices = it.get_staff_row(img, line_thickness, line_spacing)


    #all_staffline_horizontal_indices = it.get_staff_column(img, all_staffline_vertical_indices, line_thickness,line_spacing)

    start, end = it.retrieve_staff_area(img, bars, line_thickness)

    print(f'{start}\n{end}')

    #staffs = []
    #half_dist_between_staffs = (all_staffline_vertical_indices[1][0][0] - all_staffline_vertical_indices[0][4][line_thickness - 1]) // 2



    box = BoundingBox(start[0][0],start[0][1], start[4][0],start[4][1])

    end_val = 4
    begin_val = 0
    for i in range(0,len(start)//5):
        box.show_box(img0, start[begin_val][0],start[begin_val][1], end[end_val][0],end[end_val][1])
        end_val+=5
        begin_val+=5






    #TODO Create bounding boxes class
    #TODO Add template extraction
    #TODO Stay positive











