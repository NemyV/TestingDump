import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from Source.METHODS import im_screenshot

img1 = cv2.imread('Source\\Buttons\\Class\\keypoint_BARD.png', cv2.IMREAD_GRAYSCALE)  # queryImage
# img1 = cv2.imread('Source\\Buttons\\Daily Quest\\Misc\\PVP_myturn_HPBAR.png', cv2.IMREAD_GRAYSCALE)  # queryImage


def im_search_keypoint(image, matchmaking_method):
    img1 = image
    img2 = im_screenshot()  # trainImage
    if matchmaking_method == 1:
        # Initiate ORB detector
        orb = cv2.ORB_create()
        # find the keypoints and descriptors with ORB
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # Match descriptors.
        matches = bf.match(des1, des2)
        # Sort them in the order of their distance.
        matches = sorted(matches, key=lambda x: x.distance)
        # Draw first 10 matches.
        img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], None,
                               flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        plt.imshow(img3), plt.show()
    if matchmaking_method == 2:
        list_of_cords = []
        # Initiate SIFT detector
        sift = cv2.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        # Apply ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                # Get the matching keypoints for each of the images
                img2_idx = m.trainIdx
                # Get the coordinates x - columns y - rows
                (x2, y2) = kp2[img2_idx].pt
                # Append to each list
                list_of_cords.append((x2, y2))
                # THESE ARE COORDINATES OF KEYPOINTS
                good.append([m])
            else:
                123
        print("Number of good matches:", len(good))
        # cv2.drawMatchesKnn expects list of lists as matches.
        # DEBUGGING
        # img3 = cv2.drawMatchesKnn(img1, kp1,
        #                           img2, kp2, good, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        # plt.imshow(img3), plt.show()
        average = [sum(x) / len(x) for x in zip(*list_of_cords)]
        return average
    if matchmaking_method == 3:
        list_of_cords = []
        # Initiate SIFT detector
        sift = cv2.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)

        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        # FLANN_INDEX_LSH = 5
        # index_params = dict(algorithm=FLANN_INDEX_LSH,
        #                     table_number=6,  # 12
        #                     key_size=12,  # 20
        #                     multi_probe_level=1)  # 2

        search_params = dict(checks=50)  # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        # Need to draw only good matches, so create a mask
        matches_Mask = [[0, 0] for i in range(len(matches))]
        # ratio test as per Lowe's paper
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:
                # Get the matching keypoints for each of the images
                img2_idx = m.trainIdx
                # Get the coordinates x - columns y - rows
                (x2, y2) = kp2[img2_idx].pt
                # Append to each list
                list_of_cords.append((x2, y2))
                matches_Mask[i] = [1, 0]
        print("Number of good matches:", len(matches))
        #Debugging
        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=(255, 0, 0),
                           matchesMask=matches_Mask,
                           flags=cv2.DrawMatchesFlags_DEFAULT)
        img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
        plt.imshow(img3, ), plt.show()

        average = [sum(x) / len(x) for x in zip(*list_of_cords)]
        return average

print(im_search_keypoint(img1,3))