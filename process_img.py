#!/usr/bin/python3
import cv2
import numpy as np
import time
import os

def getDistance(bounding_target, bounding_list):
    distance = []
    bx, by, bw, bh = cv2.boundingRect(bounding_target)
    for index in range(len(bounding_list)):
        x, y, w, h = cv2.boundingRect(bounding_list[index])
        d_x = bx - x
        d_y = by - y
        d = pow(d_x, 2) + pow(d_y, 2)
        d = pow(d, 0.5)
        distance.append(d)
    return distance

def splitText(img_res):
    contours, hierarchy = cv2.findContours(img_res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=lambda x: cv2.boundingRect(x)[2] * cv2.boundingRect(x)[3]) # small area first

    height, width = img_res.shape
    avg_height = height * 0.8
    avg_width  = width  * 0.25 * 0.7 # 4 char per img, padding is about 40% between chars
    avg_area   = avg_height * avg_width

    result = []
    finish_index = []
    for index in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[index])
        if index in finish_index:
            continue
        if (w * h) < avg_area * 0.1:
            continue

        if (w * h) < avg_area * 0.3: # 可能为i的点
            d = getDistance(contours[index], contours)
            min_value = min(i for i in d if i > 0)
            min_index = d.index(min_value)
            finish_index.append(min_index)
            x2, y2, w2, h2 = cv2.boundingRect(contours[min_index])

            new_x = min([x2, x])
            new_y = min([y2, y])
            new_w = max([(x2+w2), (x+w)]) - new_x
            new_h = max([(y2+h2), (y+h)]) - new_y
            box = np.int0([[new_x,new_y], [new_x+w,new_y], [new_x+new_w,new_y+new_h], [new_x,new_y+new_h]])
            result.append(box)
        elif w > avg_width * 1.3: # 可能两个字母叠在一起
            box_left  = np.int0([[x,y], [x+w/2,y], [x+w/2,y+h], [x,y+h]])
            box_right = np.int0([[x+w/2,y], [x+w,y], [x+w,y+h], [x+w/2,y+h]])
            result.append(box_left)
            result.append(box_right)
        else:
            box = np.int0([[x,y], [x+w,y], [x+w,y+h], [x,y+h]])
            result.append(box)
        finish_index.append(index);

    return result

def run(input_path, output_path, index_filename = 0):
    if (os.path.exists(output_path) == False):
        os.makedirs(output_path) #Create folder

    files = os.listdir(input_path)
    index = 0
    for filename in files:
        img = cv2.imread(os.path.join(input_path, filename))
        # 灰阶
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 二值化
        ret, img_inv = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
        kernel = 1/16*np.array([[1,2,1], [2,4,2], [1,2,1]])
        # 平滑
        img_blur = cv2.filter2D(img_inv,-1, kernel)
        # 二值化
        ret, img_res = cv2.threshold(img_blur, 127, 255, cv2.THRESH_BINARY)

        # 找轮廓，切割文字
        border = 5
        result = splitText(img_res)
        result.sort(key=lambda x: x[0][0]) # 按字母顺序左到右
        for box in result:
            roi = img_res[ box[0][1]:box[3][1], box[0][0]:box[1][0] ]
            roistd = cv2.resize(roi, (30, 30)) # 将字元图片统一调整为30*30
            roistd = cv2.copyMakeBorder(roistd, border, border, border, border, cv2.BORDER_CONSTANT, None, [0,0,0])
            if index_filename:
                index = index + 1
                filename = "{}.jpg".format(index)
            else:
                timestamp = int(time.time() * 1e6) # 使用时间戳避免档案重名
                filename = "{}.jpg".format(timestamp)
            cv2.imwrite(os.path.join(output_path, filename), roistd)

            # cv2.drawContours(img, [box], 0, (0, 0, 255), 1)

        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()