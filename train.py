#!/usr/bin/python3
import cv2
import numpy as np
import os
import pickle
import process_img
import download_img

img_area = 40 * 40

download_img.run('https://www.yiqifa.com/front/common/getcode')
process_img.run('img', 'char')

filenames = os.listdir("label")
samples = np.empty((0, img_area))
labels = []
for filename in filenames:    
    filepath = os.path.join("label", filename)
    label = filename.split(".")[0].split("_")[-1]
    labels.append(label)
    im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    sample = im.reshape((1, img_area)).astype(np.float32)
    samples = np.append(samples, sample, 0)
    samples = samples.astype(np.float32)
    unique_labels = list(set(labels))
    unique_ids = list(range(len(unique_labels)))
    label_id_map = dict(zip(unique_labels, unique_ids))
    id_label_map = dict(zip(unique_ids, unique_labels))
    label_ids = list(map(lambda x: label_id_map[x], labels))
    label_ids = np.array(label_ids).reshape((-1, 1)).astype(np.float32)

model = cv2.ml.KNearest_create()
model.train(samples, cv2.ml.ROW_SAMPLE, label_ids)
model.save('model.xml')
print('training finish. save as model.xml')

# 序列化变量到文件中
f = open('id_label_map.txt', 'wb')
pickle.dump(id_label_map, f)
f.close()