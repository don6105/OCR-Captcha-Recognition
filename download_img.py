import requests
import urllib.request
import os
import time

def run(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    folder_path = 'img'
    if (os.path.exists(folder_path) == False):
        os.makedirs(folder_path) #Create folder

    for index in range(0, 100):
        html = requests.get(url, headers = headers)
        img_name = folder_path + str(index + 1) + '.jpeg'
        with open(img_name,'wb') as file: #以byte的形式將圖片數據寫入
            file.write(html.content)
            file.flush()
        file.close() #close file
        print('第 %d 張' % (index + 1))
        time.sleep(1)
    print('Done')