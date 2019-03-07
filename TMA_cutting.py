#!/usr/bin/python
# -*- coding: utf-8 -*-


import cv2
from PIL import Image
from random import choice
import sys
import copy
import sys
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def foundPoints(img, xModify, yModify, sampleType):
    imgPos = img[yModify:yModify + 540, 827:2200]
    gray = cv2.cvtColor(imgPos, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

    images, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.CHAIN_APPROX_NONE, cv2.CHAIN_APPROX_SIMPLE)
    print("length of cnts: ", len(cnts))

    spotList = []
    for i in range(len(cnts)):
        # x,y,w,h = cv2.boundingRect(cnts[i])
        (x, y), radius = cv2.minEnclosingCircle(cnts[i])
        center = (int(x) + 827, int(y) + 609)
        radius = int(radius)
        if sampleType == 'LRG':
            if 15 < radius < 30:
                spotList.append(center)
                cv2.circle(img, center, radius, (0, 255, 0), 2)
            # if w > 20 and h > 20 and w < 60 and h < 60:
            # spotList.append((x+xModify+w//2, y+yModify+h//2))
            # cv2.rectangle(img,(x+xModify,y+yModify),(x+xModify+w,y+yModify+h),(0,255,0),2)
        elif sampleType == 'SML':
            if 5 < radius < 15:
                spotList.append(center)
                cv2.circle(img, center, radius, (0, 255, 0), 2)
            # if w > 10 and h > 10 and w < 30 and h < 30:
            # spotList.append((x+xModify+w//2, y+yModify+h//2))
            # cv2.rectangle(img,(x+xModify,y+yModify),(x+xModify+w,y+yModify+h),(0,255,0),2)
    randomX, randomY = choice(spotList)
    pt1 = (randomX + 7, randomY + 7)
    pt2 = (randomX - 7, randomY - 7)
    cv2.line(img, pt1, pt2, (255, 0, 0), 2)
    pt1 = (randomX + 7, randomY - 7)
    pt2 = (randomX - 7, randomY + 7)
    cv2.line(img, pt1, pt2, (255, 0, 0), 2)

    a = "contoursImage" + str(len(cnts)) + ".png"
    cv2.imwrite(a, img)
    imgshow = Image.fromarray(img)
    imgshow.show()
    print("length of spots: ", len(spotList), '\n')
    coodinate = (randomX, randomY)
    return spotList, coodinate


def imageToXML(coordinate):
    # transfer coordinate of carousel image to XML file coordinate
    x, y = coordinate
    xmlx = str(round(1035050 * x / 2600 - 518160))
    xmly = str(round(518160 - 1035050 * y / 2600))
    return xmlx, xmly


def XMLToImage(coordinate):
    # transfer coodinate of XML file to carousel image coordinate
    xmlx, xmly = coordinate
    x = str(round((xmlx + 518160) / 1035050 * 2600))
    y = str(round((518160 - xmly) / 1035050 * 2600))
    return x, y


def firstPointCoodinatExtractor(xmlName):
    # extract the point you selected from the carousel image, as xml coordinate and return
    xmlfile = ET.ElementTree(file=xmlName)
    root = xmlfile.getroot()
    coodinate = (int(root[0][-1][0].attrib['XAttrib']), int(root[0][-1][0].attrib['YAttrib']))
    return coodinate


def xmlFileWriter(xmlfileName, PointList, imgCoordinate):
    # based on XML file with the point you selected, add all the point recognized from carousel image,
    # then append to the end of that XML file
    realX, realY = firstPointCoodinatExtractor(xmlfileName)
    imgX, imgY = imgCoordinate  # in mm unit
    ErrorX = int(imgX) - int(realX)
    ErrorY = int(imgY) - int(realY)

    xmlfile = ET.ElementTree(file=xmlfileName)
    root = xmlfile.getroot()
    for i in range(1, len(PointList) + 1):  # mind here, need change
        a = copy.deepcopy(root[0][4])
        a.attrib = {'PointName': root[0][4].attrib['PointName'] + '_' + str(i)}
        tempX, tempY = imageToXML(PointList[i - 1])
        a[0].attrib['XAttrib'] = str(round(int(tempX) + ErrorX))
        a[0].attrib['YAttrib'] = str(round(int(tempY) + ErrorY))

        root[0].append(a)
    xmlfile.write('ALL_' + xmlfileName)
    return


def main():
    args = sys.argv[1:]
    if len(args) >= 1:
        img = cv2.imread(args[0])
        if args[2] == 'UP':
            pointsList, coordinate = foundPoints(img, 827, 609, args[1])
        elif args[2] == 'DOWN':
            pointsList, coordinate = foundPoints(img, 827, 1447, args[1])
        else:
            print('Wrong params, re-run the program.')
            return
        print('Please input the XML file name with the selected point and settings.')
        xmlName = input('please enter the name of xml File: ')
        xmlFileWriter(xmlName, pointsList, imageToXML(coordinate))


if __name__ == '__main__':
    main()

