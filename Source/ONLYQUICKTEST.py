import threading
import cv2
import pyautogui
import numpy as np
import imutils
import time
import random

Resolution = [1280, 720]
Resolution = [2560, 1080]


def r(num, rand):
    return num + rand * random.random()


def im_screenshot(filename='no_file_name', x1=0, y1=0, x2=Resolution[0], y2=Resolution[1]):
    """
    Taking screenshots in specific folder
        """
    file_path = (r"Temp_files\Screenshot[" + str(threading.get_ident()) + "#" + filename + "].jpg")
    # im = ImageGrab.grab(bbox=(x1, y1, x1 + x2, y1 + y2))
    import window_capture
    wincapture = window_capture.WindowCapture('LOST ARK (64-bit, DX9) v.2.7.0.1', file_path)
    img_rgb = wincapture.get_screenshot(x1=x1, y1=y1, x2=x2, y2=y2)
    # thread_string = str(threading.get_ident())
    # im.save(file_path)
    # with mss.mss() as sct:
    #     # The screen part to capture
    #     region = {'left': x1, 'top': y1, 'width': x2, 'height': y2}
    #     # Grab the data
    #     image_screenshot = mss.mss().grab(region)
    #     # try to remove
    #     try:
    #         os.remove(r'Temp_files\Screenshot[' + filename + '].png')
    #         time.sleep(0.5)
    #         print("REMOVED FILE")
    #         test = "REMOVED"
    #     except IOError:
    #         print("DIDN T REMOVE FILE")
    #         test = "NO REMOVE"
    #     # Save to the picture file
    #     mss.tools.to_png(image_screenshot.rgb, image_screenshot.size,
    #                      output=(r'Temp_files\Screenshot[' + filename + '].png'))

    #  VERY IMPORTANT so that multiple process don't conflict on same file name
    # NEW SOLUTION DELETE IF IT DOESNT WORK  = , cv2.IMREAD_UNCHANGED)

    # img_rgb = cv2.imread(file_path, cv2.IMREAD_COLOR)  # IMREAD_UNCHANGED
    # print(img_rgb)
    if img_rgb is None:
        print("ERROR READING IMAGE FROM SCREENSHOT")
        print("FILE PATCH is:" + file_path)
        print("TRYING TO SALVAGE")
        file_path = r'Temp_files/ScreenshotFIX[' + filename + '].jpg'
        # im.save(file_path)
        img_rgb = cv2.imread(file_path, cv2.IMREAD_COLOR)  # IMREAD_UNCHANGED
    # img_rgb = img_rgb[..., :3]  # POSSIBLY FIX ERRORS
    return img_rgb


def im_search(image, x1=0, y1=0, x2=Resolution[0], y2=Resolution[1], return_value="top_left",
              click=None, action="left", offset=0, delay=0.2, precision=0.7):
    """
        Searches for an image on the screen
        Return = coordinates
    """
    file_name = "im_search"
    img_rgb = im_screenshot(file_name, x1=x1, y1=y1, x2=x2, y2=y2)
    # number_of_channels, w, h = img_rgb.shape[::-1]
    # x1 = w
    # y1 = h
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    w, h = template.shape[::-1]
    # xtres, img_rgb_w, img_rgb_h = img_rgb.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    count = 0
    loc = np.where(res >= precision)
    if len(list(zip(*loc[::-1]))) < 1 and Resolution != [2560, 1080]:
        for scale in np.linspace(0.2, 1.0, 100)[::-1]:
            image = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            resized = imutils.resize(template, width=int(template.shape[1] * scale))
            w, h = resized.shape[::-1]
            res = cv2.matchTemplate(image, resized, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            loc = np.where(res >= precision)
            if len(list(zip(*loc[::-1]))) > 0 or scale < 0.4:
                break
        # # print("LOC was less than 3")
        # image = resize_image(image)
        # template = cv2.imread(image, 0)
        # w, h = template.shape[::-1]
        # res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # loc = np.where(res >= precision)
    for pt in zip(*loc[::-1]):  # Swap columns and rows
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),
                      2)  # // Uncomment to draw boxes around found occurances
        if click == "all":
            print("CLICKING ALL")
            # img = cv2.imread(image)
            # height, width, channels = img.shape
            pyautogui.moveTo(pt[0] + r(w / 2, offset) + x1,
                             pt[1] + r(h / 2, offset) + y1,
                             duration=0.2)
            pyautogui.click(button=action)
            time.sleep(delay)
        count = count + 1
    cv2.imwrite('0RESULT.png', img_rgb)  # // Uncomment to write output image with boxes drawn around occurances
    if return_value == "count":
        return count
    if max_val < precision:
        return [-1, -1]
    else:
        if return_value == "top_left" and click == "yes":
            img = cv2.imread(image)
            height, width, channels = img.shape
            pyautogui.moveTo(max_loc[0] + r(width / 2, offset) + x1,
                             max_loc[1] + r(height / 2, offset) + y1,
                             duration=0.4)
            pyautogui.click(button=action)
            time.sleep(delay)
        if return_value == "top_left":
            return max_loc
        if return_value == "center" and click == "yes":
            top_left = max_loc  # can change to min_loc or max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            avg_x = round((bottom_right[0] + top_left[0]) / 2)
            avg_y = round((bottom_right[1] + top_left[1]) / 2)
            average = [avg_x, avg_y]

            if click == "yes":
                img = cv2.imread(image)
                height, width, channels = img.shape
                pyautogui.moveTo(average[0] + r(width / 2, offset) + x1,
                                 average[1] + r(height / 2, offset) + y1,
                                 duration=0.4)
                pyautogui.click(button=action)
                time.sleep(delay)
        if return_value == "center":
            return average

import METHODS
test123 = "D:\BLostArk\LOSTARKB\Source\Buttons\Daily Quest\Misc\Accept_quest.png"
# test123 = "D:\BLostArk\LOSTARKB\Source\Buttons\Daily Quest\Misc\Testingsomeshit.png"
print(im_search(test123, x1=round(METHODS.Resolution[0]/100*24.6), y1=round(METHODS.Resolution[1]/100*60.7),
                x2=200, y2=25, precision=0.87))
