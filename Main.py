import matplotlib.pyplot as plt
import cv2
import ImageConverter as ic
import ImageTools as it
from BoundingBox import BoundingBox
from MusicObject import MusicObject
import Resource
from Resource import match

import os

#windows_path = PureWindowsPath(filename)

#TODO make file system functional on macOS, Windows, and Linux

class Main:

    def show_box(img,x1,y1,x2,y2):
        #print(f'Generating Bounding Box')
        cv2.imwrite('preimage.png',img)
        im2 = cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),thickness=1)

        cv2.imwrite('box.png', im2)

    filename = "resources/examples/Twinkle.png"
    original_image = cv2.imread(filename)
    img1 = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    f = ic.convertImage(filename)
    filename = "out.png"
    img0 = cv2.imread(filename)
    print('got to line 18')

    it.preprocess1(filename)

    img = it.preprocess(filename)
    print(f'finished preprocessing {filename}')
    bars = it.preprocess('bars.png')

    line_spacing, line_thickness = it.get_line_info(img)

    #print(f'filename {filename}: line spacing = {line_spacing}\tline thickness = {line_thickness}')

    #all_staffline_vertical_indices = it.get_staff_row(img, line_thickness, line_spacing)


    #all_staffline_horizontal_indices = it.get_staff_column(img, all_staffline_vertical_indices, line_thickness,line_spacing)

    start, end = it.retrieve_staff_area(img, bars, line_thickness)

    #print(f'{start}\n{end}')

    #staffs = []
    #half_dist_between_staffs = (all_staffline_vertical_indices[1][0][0] - all_staffline_vertical_indices[0][4][line_thickness - 1]) // 2



    box = BoundingBox(start[0][0],start[0][1], start[4][0],start[4][1])

    end_val = 4
    begin_val = 0
    staffs = []

    expand_border = 10

    for i in range(0, len(start)//5):
        show_box(img0, start[begin_val][0]-expand_border, start[begin_val][1]-expand_border, end[end_val][0]+expand_border, end[end_val][1] + expand_border)
        crop_img = img0[start[begin_val][1]-expand_border:end[end_val][1]+expand_border, start[begin_val][0]+expand_border:end[end_val][0]+expand_border]
        #plt.imshow(crop_img)
        #plt.show()
        name = f'cropped{i}.png'
        staffs.append(crop_img)
        cv2.imwrite(name, crop_img)
        end_val += 5
        begin_val += 5


    num_staffs = len(start)//5

    print(f'Number of staffs: {num_staffs}')


    #######Getting templates###########
    quarter_note_imgs, half_note_imgs, whole_note_imgs = Resource.get_notes()


    # TODO Add template extraction
    for i in range(num_staffs): #find template matches
        found_items = []
        staff_img = staffs[i]
        #print(staffs[i].shape)
        # Accidentals
        # Barlines
        # Clef
        # Time
        # Rest

        # Note
        quarter_boxes = Resource.locate_templates(staff_img, quarter_note_imgs, Resource.quarter_note_lower, Resource.quarter_note_upper, Resource.quarter_note_thresh)
        quarter_boxes = Resource.merge([j for i in quarter_boxes for j in i], 0.5)


        for box in quarter_boxes:
            box.draw(staff_img, (0, 0, 255), 1)
            text = "1/4 note"
            font = cv2.FONT_HERSHEY_DUPLEX
            textsize = cv2.getTextSize(text, font, fontScale=0.7, thickness=1)[0]
            x = int(box.getCorner()[0] - (textsize[0] // 2))
            y = int(box.getCorner()[1] + box.getHeight() + 20)
            cv2.putText(staff_img, text, (x, y), font, fontScale=0.7, color=(0,0,255), thickness=1)
            nimage = f'qnotes{i}.png'
            cv2.imshow('lol',staff_img)
            cv2.waitKey(0)

        # Flag




    #TODO Stay positive











