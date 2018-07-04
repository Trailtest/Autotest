import sys
import cv2
import numpy as np
import pickle
import math


def storeLedPositions(posDict):
    upDict = {}
    lowDict = {}
    count = 0
    for key in sorted(posDict.iterkeys()):
        if(count < 4):
            upDict[posDict[key]] = key
        elif(count > 9):
            lowDict[posDict[key]] = key
        count += 1
    posDictList = posDict.keys()
    upDictList = upDict.keys()
    lowDictList = lowDict.keys()
    posDictList.sort()
    upDictList.sort()
    lowDictList.sort(reverse=True)

    count = 0
    finalPos = []
    while(count < 14):
        if(count < 4):
            finalPos.append([upDict[upDictList[count]], upDictList[count]])
        elif(count > 9):
            finalPos.append(
                [lowDict[lowDictList[count - 10]], lowDictList[count - 10]])
        else:
            finalPos.append([posDictList[count], posDict[posDictList[count]]])
        count += 1

    with open('ledPositions', 'wb') as fp:
        pickle.dump(finalPos, fp)


def loadLedPositions():
    finalPos = [[]]

    try:
        with open('ledPositions', 'rb') as f:
            finalPos = pickle.load(f)
        return finalPos
    except IOError:
        print "ledPositions file is missing. Please run the script in calibrate mode with the image containg all the LED's turned on\n \
ex: python led_detection_g.py <image> calibrate"
        sys.exit()


def getLedNumber(finalPos, xPos, yPos, calib):
    if calib is False:
        for i in range(len(finalPos)):
            d = math.sqrt(
                (pow((finalPos[i][0] - xPos), 2) + pow((finalPos[i][1] - yPos), 2)))
            if(d < 10):
                return (1 + i)
    return -1


def findColour(img, calib):
    red_counter = 0
    blue_counter = 0
    green_counter = 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]

    params = cv2.SimpleBlobDetector_Params()
    params.blobColor = 255
    params.filterByArea = False
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = True
    params.minInertiaRatio = 0.5
    params.maxInertiaRatio = 1
    #detector = cv2.SimpleBlobDetector(params)
    is_v2 = cv2.__version__.startswith("2.")
    if is_v2:
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(thresh)

    im_with_keypoints = cv2.drawKeypoints(thresh, keypoints, np.array(
        []), (255, 0, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
    '''cv2.namedWindow("Keypoints",0)
   cv2.resizeWindow("Keypoints",200,75)
   cv2.imshow("Keypoints", im_with_keypoints)
   cv2.waitKey(0)'''

    height, width, depth = img.shape
    posDict = {}
    finalPos = [[]]

    if calib is False:
        finalPos = loadLedPositions()
        finalPos.reverse()

    for keypoint in keypoints:
        mask = np.zeros((height, width), np.uint8)
        cv2.circle(mask, (int(keypoint.pt[0]), int(keypoint.pt[1])), int(
            keypoint.size / 2), (255, 255, 255), -1)
        mean = cv2.mean(img, mask=mask)
        if mean[0] > mean[1]:
            if mean[0] > mean[2]:
                print "led%d: RED " % (getLedNumber(finalPos, int(keypoint.pt[0]), int(keypoint.pt[1]), calib))
                red_counter += 1
            else:
                print "led%d: BLUE " % (getLedNumber(finalPos, int(keypoint.pt[0]), int(keypoint.pt[1]), calib))
                blue_counter += 1
        elif mean[1] > mean[2]:
            print "led%d: GREEN " % (getLedNumber(finalPos, int(keypoint.pt[0]), int(keypoint.pt[1]), calib))
            green_counter += 1
        else:
            print "led%d: BLUE " % (getLedNumber(finalPos, int(keypoint.pt[0]), int(keypoint.pt[1]), calib))
            blue_counter += 1
        # print "loc: %d,%d,%d" %(int(keypoint.pt[0]),int(keypoint.pt[1]),int(keypoint.size))
#     print "mean: %d,%d,%d" %(mean[0],mean[1],mean[2])
        posDict[int(keypoint.pt[0])] = int(keypoint.pt[1])
    print "\nNumber of green LED's on: %d\n\
Number of red LED's on: %d\n\
Number of blue LED's on: %d\n" % (green_counter, red_counter, blue_counter)

    if calib is True:
        if green_counter + red_counter + blue_counter == 14:
            storeLedPositions(posDict)
            print "Calibration Success"
        else:
            print "Calibration Failed\nPlease run the script with the image that contains all LED's turned on"


if __name__ == '__main__':
    # print len(sys.argv)
    img = cv2.imread(sys.argv[1])
    if len(sys.argv) == 3:
        if sys.argv[2] == 'calibrate':
            findColour(img, True)
    else:
        findColour(img, False)
