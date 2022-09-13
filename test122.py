import cv2
import numpy as np
import mss
import os
import time
Buttons = "Buttons\\"
Resolution = [2560, 1080]
MiniMCOORD = [Resolution[0] / 100 * 86,
              Resolution[1] / 100 * 4.17,
              Resolution[0] / 100 * 98.7,
              Resolution[1] / 100 * 30.28]


def im_screenshot(filename='no_file_name', x1=0, y1=0, x2=Resolution[0], y2=Resolution[1]):
    with mss.mss() as sct:
        # The screen part to capture
        region = {'left': x1, 'top': y1, 'width': x2, 'height': y2}
        # Grab the data
        image_screenshot = mss.mss().grab(region)
        # try to remove
        try:
            os.remove(r'Temp_files\\Screenshot[' + filename + '].png')
            time.sleep(0.5)
            # print("REMOVED FILE")
        except IOError:
            # print("DIDN T REMOVE FILE")
            123
        # Save to the picture file
        mss.tools.to_png(image_screenshot.rgb, image_screenshot.size,
                         output=(r'Temp_files\\Screenshot[' + filename + '].png'))
    #  VERY IMPORTANT so that multiple process don't conflict on same file name
    # NEW SOLUTION DELETE IF IT DOESNT WORK  = , cv2.IMREAD_UNCHANGED)
    img_rgb = cv2.imread('Temp_files\\Screenshot[' + filename + '].png', cv2.IMREAD_UNCHANGED)
    if img_rgb is None:
        print("ERROR READING IMAGE FROM SCREENSHOT")
    return img_rgb


def imagesearch_fast_area(image, x1=0, y1=0, x2=Resolution[0], y2=Resolution[1], precision=0.8):
    file_name = "imagesearch_fast_area"
    img_rgb = im_screenshot(file_name, x1, y1, x2, y2)

    img_rgb = np.array(img_rgb)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # avg_x = (min_loc[0] + max_loc[0]) / 2
    # avg_y = (min_loc[1] + max_loc[1]) / 2
    #
    # center_of_image = [max_loc[0], max_loc[1]]
    if max_val < precision:
        return [-1, -1]
    # return max_loc
    return max_loc