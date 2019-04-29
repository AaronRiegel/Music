import cv2
import numpy as np
from BoundingBox import BoundingBox


clef_paths = {
    'treble': [
        'resources/templates/clef/treble_1.jpg',
        'resources/templates/clef/treble_2.jpg'],
    'bass': [
        'resources/templates/clef/bass_1.jpg'
    ]
}

accidental_paths = {
    'sharp': [
        'resources/templates/accidental/sharp-line.png',
        'resources/templates/accidental/sharp-space.png'],
    'flat': [
        'resources/templates/accidental/flat-line.png',
        'resources/templates/accidental/flat-space.png']
}

note_paths = {
    'quarter': [
        'resources/templates/note/solid-note.png',
        'resources/templates/note/solid-note.png',
        'resources/templates/note/qfull.png',
        'resources/templates/note/qfull2.png'],
    'half': [
        'resources/templates/note/half-space.png',
        'resources/templates/note/half-note-line.png',
        'resources/templates/note/half-line.png',
        'resources/templates/note/half-note-space.png'],
    'whole': [
        'resources/templates/note/whole-space.png',
        'resources/templates/note/whole-note-line.png',
        'resources/templates/note/whole-line.png',
        'resources/templates/note/whole-note-space.png']
}
rest_paths = {
    'eighth': ['resources/templates/rest/eighth_rest.jpg'],
    'quarter': ['resources/templates/rest/quarter_rest.jpg'],
    'half': ['resources/templates/rest/half_rest_1.jpg',
            'resources/templates/rest/half_rest_2.jpg'],
    'whole': ['resources/templates/rest/whole_rest.jpg']
}

flag_paths = ['resources/templates/flag/eighth_flag_1.jpg',
                'resources/templates/flag/eighth_flag_2.jpg',
                'resources/templates/flag/eighth_flag_3.jpg',
                'resources/templates/flag/eighth_flag_4.jpg',
                'resources/templates/flag/eighth_flag_5.jpg',
                'resources/templates/flag/eighth_flag_6.jpg']

barline_paths = ['resources/templates/barline/barline_1.jpg',
                 'resources/templates/barline/barline_2.jpg',
                 'resources/templates/barline/barline_3.jpg',
                 'resources/templates/barline/barline_4.jpg']

# Clefs
clef_lower, clef_upper, clef_thresh = 50, 150, 0.88

# Time
time_lower, time_upper, time_thresh = 50, 150, 0.85

# Accidentals
sharp_lower, sharp_upper, sharp_thresh = 50, 150, 0.70
flat_lower, flat_upper, flat_thresh = 50, 150, 0.77

# Notes
quarter_note_lower, quarter_note_upper, quarter_note_thresh = 50, 150, 0.72
half_note_lower, half_note_upper, half_note_thresh = 50, 150, 0.70
whole_note_lower, whole_note_upper, whole_note_thresh = 50, 150, 0.70

# Rests
eighth_rest_lower, eighth_rest_upper, eighth_rest_thresh = 50, 150, 0.75
quarter_rest_lower, quarter_rest_upper, quarter_rest_thresh = 50, 150, 0.70
half_rest_lower, half_rest_upper, half_rest_thresh = 50, 150, 0.80
whole_rest_lower, whole_rest_upper, whole_rest_thresh = 50, 150, 0.80

# Eighth Flag
eighth_flag_lower, eighth_flag_upper, eighth_flag_thresh = 50, 150, 0.80

# Bar line
bar_lower, bar_upper, bar_thresh = 50, 150, 0.85


def get_cleff():

    clef_imgs = {
        "treble": [cv2.imread(clef_file, 0) for clef_file in clef_paths["treble"]],
        "bass": [cv2.imread(clef_file, 0) for clef_file in clef_paths["bass"]]
    }
    return clef_imgs


def get_time():

    time_imgs = {
        "common": [cv2.imread(time, 0) for time in ["resources/templates/time/common.jpg"]],
        "4-4": [cv2.imread(time, 0) for time in ["resources/templates/time/44.jpg"]],
        "3-4": [cv2.imread(time, 0) for time in ["resources/templates/time/34.jpg"]],
        "2-4": [cv2.imread(time, 0) for time in ["resources/templates/time/24.jpg"]],
        "6-8": [cv2.imread(time, 0) for time in ["resources/templates/time/68.jpg"]]
    }

    return time_imgs


def get_accidental():

    sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in accidental_paths["sharp"]]
    flat_imgs = [cv2.imread(flat_file, 0) for flat_file in accidental_paths["flat"]]
    return sharp_imgs, flat_imgs


def get_notes():

    quarter_note_imgs = [cv2.imread(quarter, 0) for quarter in note_paths["quarter"]]
    half_note_imgs = [cv2.imread(half, 0) for half in note_paths["half"]]
    whole_note_imgs = [cv2.imread(whole, 0) for whole in note_paths['whole']]
    return quarter_note_imgs, half_note_imgs, whole_note_imgs


def get_rest():

    eighth_rest_imgs = [cv2.imread(eighth, 0) for eighth in rest_paths["eighth"]]
    quarter_rest_imgs = [cv2.imread(quarter, 0) for quarter in rest_paths["quarter"]]
    half_rest_imgs = [cv2.imread(half, 0) for half in rest_paths["half"]]
    whole_rest_imgs = [cv2.imread(whole, 0) for whole in rest_paths['whole']]
    return eighth_rest_imgs, quarter_rest_imgs, half_rest_imgs, whole_rest_imgs


def get_flag():

    eighth_flag_imgs = [cv2.imread(flag, 0) for flag in flag_paths]
    return eighth_flag_imgs


def get_bar():

    bar_imgs = [cv2.imread(barline, 0) for barline in barline_paths]

    return bar_imgs


def match(img, templates, start_percent, stop_percent, threshold):
    # img_width, img_height = img.shape[::-1]
    best_location_count = -1
    best_locations = []
    best_scale = 1
    #print('Matching...')

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #print(f'image shape inside match: {img.shape}')
    #print(f'templates {templates}')

    x = []
    y = []
    for scale in [i/100.0 for i in range(start_percent, stop_percent + 1, 3)]:
        locations = []
        location_count = 0


        for template in templates:
            if (scale*template.shape[0] > img.shape[0] or scale*template.shape[1] > img.shape[1]):
                continue

            template = cv2.resize(template, None, fx = scale, fy = scale, interpolation = cv2.INTER_CUBIC)
            result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            #result = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
            result = np.where(result >= threshold)
            location_count += len(result[0])
            locations += [result]


        x.append(location_count)
        y.append(scale)

        if (location_count > best_location_count):
            best_location_count = location_count
            best_locations = locations
            best_scale = scale

        elif (location_count < best_location_count):
            pass


    return best_locations, best_scale


def locate_templates(img, templates, start, stop, threshold):
    #print('Locating Templates...')
    #print(f'templates in locate: {templates}')
    locations, scale = match(img, templates, start, stop, threshold)
    img_locations = []
    for i in range(len(templates)):
        w, h = templates[i].shape[::-1]
        w *= scale
        h *= scale
        img_locations.append([BoundingBox(pt[0], pt[1], w, h) for pt in zip(*locations[i][::-1])])
    return img_locations


def merge(recs, threshold):
    filtered_recs = []
    while len(recs) > 0:
        r = recs.pop(0)
        recs.sort(key=lambda rec: rec.distance(r))
        merged = True
        while merged:
            merged = False
            i = 0
            for _ in range(len(recs)):
                if r.overlap(recs[i]) > threshold or recs[i].overlap(r) > threshold:
                    r = r.merge(recs.pop(i))
                    merged = True
                elif recs[i].distance(r) > r.w/2 + recs[i].w/2:
                    break
                else:
                    i += 1
        filtered_recs.append(r)
    return filtered_recs




