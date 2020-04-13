#画像を赤色で二植化し保存するプログラム

# BGRで特定の色を抽出する関数
def BGR_extraction(image, bgrLower, bgrUpper):
    img_mask = cv2.inRange(image, bgrLower, bgrUpper) # BGRからマスクを作成
    result = cv2.bitwise_and(image, image, mask=img_mask) # 元画像とマスクを合成
    return result

import sys
import cv2
import numpy as np


print("画像を赤色で二植化し保存するプログラムです。\n")

img = cv2.imread(input("読み込む画像ファイルの名前を入力してください\nex)sample.jpg sample.png\n画像ファイル名："))#画像ファイル名から画像データの読み込み(同じディレクトリにあること)
print("-------------------------------------------------")
pic_rename = input("保存する画像ファイルの名前を入力してください\nex)sample.jpg sample.png\n画像ファイル名：")

im = img#元画像
#img = cv2.resize(img,(1000, 700))#画像のリサイズ(画像、(横、縦))
img = BGR_extraction(img,np.array([0, 0, 110]),np.array([100, 60, 255]))#赤色だけ抽出(BGRで色の上限・下限を設定)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)#BGRをHSVに変換
h_img, s_img, v_img = cv2.split(hsv)#HSVに分解
ret, img = cv2.threshold(s_img, 0, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)#輪郭検知
try:
    biggest = max(contours, key=lambda x: cv2.contourArea(x))# 一番大きい輪郭を選択する。
except:
    print("\n検知できる赤色が存在しませんでした")
    print("プログラムを終了します")
    sys.exit()

cv2.imwrite(pic_rename,img)#画像を保存
print("\n「" + pic_rename + "」という名前で画像を保存しました")
