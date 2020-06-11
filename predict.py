#!/usr/bin/python3
import cv2
import numpy as np
import os
import process_img
import pickle
from shutil import copyfile

# model = cv2.ml.KNearest_create()
# model.load('model.xml')
model = cv2.ml.KNearest_load('model.xml')

img_area = 40 * 40

# 将序列化的内容加载到内存中
f = open('id_label_map.txt', 'rb')
try:
    id_label_map = pickle.load(f)
except EOFError:
    pass
f.close()

filenames = os.listdir('img')
for filename in filenames:
    filelist = [ f for f in os.listdir('predict')]
    for f in filelist:
        os.remove(os.path.join('predict', f))

    copyfile(os.path.join('img', filename), os.path.join('predict', filename))
    img_captcha = cv2.imread(os.path.join('predict', filename))

    process_img.run('predict', 'result', 1)
    predict = sorted(os.listdir('result'))

    r = []
    for p in predict:
        img = cv2.imread(os.path.join('result', p), cv2.IMREAD_GRAYSCALE)
        sample = img.reshape((1, img_area)).astype(np.float32)
        ret, results, neighbours, distances = model.findNearest(sample, k = 3)
        label_id = int(results[0, 0])
        label = id_label_map[label_id]
        r.append(label)
    print(' '.join(r))

    cv2.imshow('image', img_captcha)
    key = cv2.waitKey(0)
    if key == 27:
        exit()
    else :  
        cv2.destroyAllWindows()