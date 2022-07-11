# ある範囲内の色のみ抽出し、他が黒色のマスク画像を作成するプログラム
# 2022年4月20日(水)

import cv2
import numpy as np

for i in range(1000):
    try:  # 画像があったら
        image = cv2.imread("C:/Users/user/program/data5_NPC-off/SS1/"+str(i).zfill(6)+".jpg")  # 読み込む画像のパス
        bgrLower = np.array([240, 240, 240])  # 抽出する色の下限(BGRの順 0~255)
        bgrUpper = np.array([255, 255, 255])  # 抽出する色の上限(BGRの順 0~255)
        mask = cv2.inRange(image,bgrLower,bgrUpper)  # 作成したやつ
        # cv2.imshow('Road Sementation', mask)# 作成した画像を表示
        # cv2.waitKey(-1)
        cv2.imwrite("C:/Users/user/program/data5_NPC-off/SS1_bw/"+str(i).zfill(6)+".jpg",mask)
    except:
        None