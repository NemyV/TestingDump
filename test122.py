import numpy as np
import cv2
import imutils
from PIL import ImageGrab
import threading
Resolution = [2560, 1080]
# template = "D:\BLostArk\LOSTARKB\Source\Buttons\Daily Quest\Misc\Testingsomeshit.png"
# template = "D:\BLostArk\LOSTARKB\Source\Buttons\Daily Quest\Misc\Accept_quest.png"
template = "D:\BLostArk\LOSTARKB\Source\Buttons\Fishing\OPENSkills\old\Lifeskill_bar.png"
# template = "D:\BLostArk\LOSTARKB\Source\Buttons\Fishing\OPENSkills\old\LOSTARK_eImXiUEdrJ.png"

def im_screenshot(filename='no_file_name', x1=0, y1=0, x2=Resolution[0], y2=Resolution[1]):
    """
    Taking screenshots in specific folder
        """
    im = ImageGrab.grab(bbox=(x1, y1, x1+x2, y1+y2))
    file_path = 'Temp_files/Screenshot[T:' + str(threading.get_ident()) + '|' + filename + '].jpg'
    im.save(file_path)
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

    img_rgb = cv2.imread(file_path, cv2.IMREAD_COLOR)  # IMREAD_UNCHANGED
    if img_rgb is None:
        print("ERROR READING IMAGE FROM SCREENSHOT")
        print("FILE PATCH is:" + file_path)
        print("TRYING TO SALVAGE")
        file_path = r'Temp_files/ScreenshotFIX[' + filename + '].jpg'
        im.save(file_path)
        img_rgb = cv2.imread(file_path, cv2.IMREAD_COLOR)  # IMREAD_UNCHANGED
    img_rgb = img_rgb[..., :3]  # POSSIBLY FIX ERRORS
    return img_rgb
    # return file_path


def resize_image(image, increment=0.2, precision=0.7):
    template = cv2.imread(image)  # template image
    img_screenshot = im_screenshot()  #x1=700, y1=700, x2=400, y2=150)

    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(img_screenshot, cv2.COLOR_BGR2GRAY)
    debugging = False
    loc = False
    w, h = template.shape[::-1]
    for scale in np.linspace(increment, 1.0, 100)[::-1]:
        print(scale)
        resized = imutils.resize(template, width=int(template.shape[1] * scale))
        w, h = resized.shape[::-1]
        res = cv2.matchTemplate(image, resized, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= precision)
        if len(list(zip(*loc[::-1]))) > 0 or scale < 0.4:
            if len(list(zip(*loc[::-1]))) > 0:
                debugging = True
            break

    if loc and len(list(zip(*loc[::-1]))) > 0:
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_screenshot, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    if debugging:
        cv2.imshow('Matched Template', img_screenshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


resize_image(template)