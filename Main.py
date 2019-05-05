import matplotlib.pyplot as plt
import cv2
import ImageConverter as ic
import ImageTools as it
from BoundingBox import BoundingBox
from MusicObject import MusicObject
import Resource
from Resource import match
from Staff import Staff
from music21 import *

import os



#TODO make file system functional on macOS, Windows, and Linux
#TODO cleanup main


def show_box(img,x1,y1,x2,y2):
    #print(f'Generating Bounding Box')
    cv2.imwrite('preimage.png', img)
    im2 = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), thickness=1)

    cv2.imwrite('box.png', im2)

def match_templates(staff_img, staff, i, note_imgs_, note_lower_, note_upper_, note_thresh, notation, duration=0,rest=False):
    _boxes = Resource.locate_templates(staff_img, note_imgs_, note_lower_,
                                      note_upper_, note_thresh)
    _boxes = Resource.merge([j for i in _boxes for j in i], 0.5)


    for box in _boxes:
        box.draw(staff_img, (0, 0, 255), 1)
        text = f"{notation}"
        font = cv2.FONT_HERSHEY_DUPLEX
        textsize = cv2.getTextSize(text, font, fontScale=0.255, thickness=1)[0]
        x = int(box.getCorner()[0] - (textsize[0] // 2))
        y = int(box.getCorner()[1] + box.getHeight() + 20)
        cv2.putText(staff_img, text, (x, y), font, fontScale=0.25, color=(0, 0, 255), thickness=1)
        y_center = box.getCenter()
        # print(f'x_center {int(round(y_center[0]))} y_center {int(round(y_center[1]))}')
        pitch = staff.get_pitch(int(round((y_center)[1])))
        nimage = f'qnotes{i}.png'
        cv2.imwrite(nimage, staff_img)
        if(rest):
            obj = MusicObject(notation, 'rest', duration, box, pitch)
        else:
            obj = MusicObject(notation, 'note', duration, box, pitch)
        if(notation == 'sharp' or notation == 'flat'):
            return
        sequence.append(obj)

def find_cleff(staff_img, i,clef_imgs, clef_lower, clef_upper, clef_thresh):
    for clef in clef_imgs:
        # print("Matching {} clef template on staff".format(clef), i + 1)
        clef_boxes = Resource.locate_templates(staff_img, clef_imgs[clef], clef_lower, clef_upper, clef_thresh)
        clef_boxes = Resource.merge([j for i in clef_boxes for j in i], 0.5)

        if (len(clef_boxes) == 1):
            print("Clef Found: ", clef)
            staffs[i].setClef(clef)

            # print("[INFO] Displaying Matching Results on staff", i + 1)
            clef_boxes_img = staffs[i].getImage()
            clef_boxes_img = clef_boxes_img.copy()

            for boxes in clef_boxes:
                boxes.draw(staff_img, (0,255,0), 1)
                x = int(boxes.getCorner()[0] + (boxes.getWidth() // 2))
                y = int(boxes.getCorner()[1] + boxes.getHeight() + 10)
                cv2.putText(staff_img, "{} clef".format(clef), (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0,255,0))

def make_sequence(sequence):
    print('making sequence...')
    strm = stream.Stream()

    for s in sequence:
        # print('extracting values from sequence...')
        # print(s.get_type())
        if s.get_type() is 'note':
            n = note.Note(s.get_pitch())
            n.quarterLength = s.get_duration()
            # print(f'adding {s.get_duration()} {s.get_pitch()}')

            strm.append(n)
        elif s.get_type() is 'rest':
            r = note.Rest()
            r.quarterLength = s.get_duration()
            # print(f'adding {s.get_duration()} {s.get_pitch()}')
            strm.append(r)

    # strm.show('midi')
    strm.write('midi', 'output.mid')

if __name__ == "__main__":

    filename = "resources/examples/helloWorld2.png" #input file, should be higher resolution for more accurate reading
    original_image = cv2.imread(filename)
    img1 = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    f = ic.convertImage(filename)
    filename = "out.png"
    img0 = cv2.imread(filename)


    it.preprocess1(filename)

    img = it.preprocess(filename)
    print(f'finished preprocessing {filename}')
    bars = it.preprocess('bars.png')

    line_spacing, line_thickness = it.get_line_info(img)

    #print(f'filename {filename}: line spacing = {line_spacing}\tline thickness = {line_thickness}')

    #all_staffline_vertical_indices = it.get_staff_row(img, line_thickness, line_spacing)


    #all_staffline_horizontal_indices = it.get_staff_column(img, all_staffline_vertical_indices, line_thickness,line_spacing)

    start, end = it.retrieve_staff_area(img, bars, line_thickness)

    num_staffs = len(start) // 5

    # print(f'{start}\n{end}')



    box = BoundingBox(start[0][0],start[0][1], start[4][0],start[4][1])

    end_val = 4
    begin_val = 0
    cropped = []

    # **************OUTER BORDER FOR CROPPED IMAGE************
    expand_border = 10

    for i in range(0, len(start)//5):
        show_box(img0, start[begin_val][0]-expand_border, start[begin_val][1]-expand_border, end[end_val][0]+expand_border, end[end_val][1] + expand_border)
        crop_img = img0[start[begin_val][1]-expand_border:end[end_val][1]+expand_border, start[begin_val][0]+expand_border:end[end_val][0]+expand_border]

        #plt.imshow(crop_img)
        #plt.show()
        name = f'cropped{i}.png'

        cropped.append(crop_img)
        cv2.imwrite(name, crop_img)
        end_val += 5
        begin_val += 5

    staff_matrices = []
    staffs = []

    for i in range(len(start)):
        staff_matrices.append(start[i][1]-start[0][1]+expand_border)

    # print(f'staff_matrices: {staff_matrices}')
    count = 0
    for i in range(len(cropped)):
        staff = Staff(staff_matrices[:count+5], line_thickness, line_spacing, cropped[i])
        # print(f'creating staff {i}')
        staffs.append(staff)
        count += 5

    # for i in staffs:
    #     print(f'{i.line_one}\n{i.line_two}\n{i.line_three}\n{i.line_four}\n{i.line_five}')



    # print(f'Number of staffs: {num_staffs}')


    #######Getting templates###########
    quarter_note_imgs, half_note_imgs, whole_note_imgs = Resource.get_notes()
    eighth_rest_imgs, quarter_rest_imgs, half_rest_imgs, whole_rest_imgs = Resource.get_rest()
    eighth_flag_imgs = Resource.get_flag()
    sharp_imgs, flat_imgs = Resource.get_accidental()
    time_imgs = Resource.get_time()
    clef_imgs = Resource.get_cleff()
    bar_imgs = Resource.get_bar()



    sequence = []
    sequences = []

    for i in range(num_staffs): # find template matches of time, cleff
        staff_img = cropped[i]
        # find_cleff(staff_img,i,clef_imgs,Resource.clef_lower,Resource.clef_upper,Resource.clef_thresh)
    # Barlines
    # match_templates(staff_img, i, bar_imgs, Resource.bar_lower, Resource.bar_upper,
    # Resource.bar_thresh, 'barline')
    # Clef
    # match_templates(staff_img, i, cleff_imgs, Resource.clef_lower, Resource.clef_upper,
    # Resource.clef_thresh, 'Cleff')

    # Time
    # match_templates(staff_img, i, time_imgs, Resource.time_lower, Resource.time_upper,
    # Resource.time_thresh, 'Time Sign.')


    for i in range(num_staffs): # find template matches of rests and notes
        found_items = []
        staff_img = staffs[i]
        #print(staffs[i].shape)
        # Accidentals
        match_templates(cropped[i], staff_img, i, sharp_imgs, Resource.sharp_lower, Resource.sharp_upper,
                        Resource.sharp_thresh, 'sharp')
        match_templates(cropped[i], staff_img, i, flat_imgs, Resource.flat_lower, Resource.flat_upper,
                        Resource.flat_thresh, 'flat')


        # Rest
        match_templates(cropped[i],staff_img, i, quarter_rest_imgs, Resource.quarter_rest_lower, Resource.quarter_rest_upper,
                        Resource.quarter_rest_thresh, 'quarter', 1, rest=True)

        match_templates(cropped[i],staff_img, i, half_rest_imgs, Resource.half_rest_lower, Resource.half_rest_upper,
                        Resource.half_rest_thresh, 'half', 2, rest=True)

        match_templates(cropped[i],staff_img, i, whole_rest_imgs, Resource.whole_rest_lower, Resource.whole_rest_upper,
                        Resource.whole_rest_thresh, 'whole', 4, rest=True)

        # Note

        match_templates(cropped[i],staff_img, i, quarter_note_imgs, Resource.quarter_note_lower, Resource.quarter_note_upper,
                        Resource.quarter_note_thresh, 'quarter', 1)

        match_templates(cropped[i],staff_img, i, half_note_imgs, Resource.half_note_lower, Resource.half_note_upper,
                        Resource.half_note_thresh, 'half', 2)

        match_templates(cropped[i],staff_img, i, whole_note_imgs, Resource.whole_note_lower, Resource.whole_note_upper,
                        Resource.whole_note_thresh, 'whole', 4)

        # Flag

        # print(len(sequence))

        sequence.sort(key=lambda obj: obj.get_box().getCenter())

        sequences.extend(sequence)
        sequence = []

    for x in sequences:
        print(f'{x.get_object()} {x.get_type()} {x.get_duration()} {x.get_pitch()}')

    print(f'len sequence: {len(sequences)}')

    make_sequence(sequences)





    #TODO Stay positive

    print('\n\n\nFinished.')











