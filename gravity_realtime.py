#リアルタイムで赤色物体の重心を追跡するプログラム

#↓参考にさせていただいたサイト
#https://qiita.com/jin237/items/0f6c8f43e70d3e787cfe

import cv2
import numpy as np

# BGRで特定の色を抽出する関数
def BGR_extraction(image, bgrLower, bgrUpper):
    img_mask = cv2.inRange(image, bgrLower, bgrUpper) # BGRからマスクを作成
    result = cv2.bitwise_and(image, image, mask=img_mask) # 元画像とマスクを合成
    return result

# 画像の中心線を引く関数
def center(img_name):
    try:
        h, w, c = img_name.shape#画像の高さ、幅、色データ カラーの時
    except:#白黒画像だった時のエラー回避
        h, w,  = img_name.shape  # 画像の高さ、幅、色データ　白黒の時
    ch = int(h / 2)
    cw = int(w / 2)
    cv2.line(img_name, (cw, 0), (cw, h), (255, 255, 255))#線の色が黒の時はすべて255
    cv2.line(img_name, (0, ch), (w, ch), (0, 0, 0))#線の色は白

def inputs(img_def):
    #img_def = cv2.imread(pic_name)  # 画像ファイル名から画像データの読み込み(同じディレクトリにあること)
    img_red = BGR_extraction(img_def, np.array([0, 0, 100]), np.array([100, 80, 255]))  # 赤色だけ抽出(BGRで色の上限・下限を設定)
    hsv = cv2.cvtColor(img_red, cv2.COLOR_BGR2HSV)  # BGRをHSVに変換
    h_img, s_img, v_img = cv2.split(hsv)  # HSVに分解
    #cv2.imwrite(pic_rename[:-4] + "_mask.jpg", s_img)  # マスク画像を保存
    ret, img_bl = cv2.threshold(s_img, 0, 255,cv2.THRESH_BINARY) 
    contours, hierarchy = cv2.findContours(img_bl, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 輪郭検知
    if contours == []:
        biggest = []
    else:
        biggest = max(contours, key=lambda x: cv2.contourArea(x))  # 一番大きい輪郭を選択する。

    return s_img, biggest #白黒の画像、一番大きい輪郭

def GXGY(biggest,s_img,img_def):
    # 重心
    M = cv2.moments(biggest)#biggestは一番大きい輪郭の情報
    if M["m00"] == 0:
        return img_def
    cx = int(M["m10"] / M["m00"])  # 重心のｘ座標
    cy = int(M["m01"] / M["m00"])  # 重心のｙ座標
    h, w = s_img.shape  # ファイルサイズの取得(h×w=高さ×幅)
    hh = int(h / 2)  # 高さの半分
    hw = int(w / 2)  # 幅の半分（x,y=hw,hhで中心の座標になる）
    x = cx - hw  # 水平方向における重心の中心からの距離
    y = hh - cy  # 鉛直方向における重心の中心からの距離
    cv2.circle(img_def, (cx, cy), 10, 300, -1, 4)
    # (画像,中心座標,円の半径,円の色,円の線の太さ(負で塗りつぶし) thickness=1,線の種類 lineType=8, shift=0)
    return img_def

#captureの準備
cap = cv2.VideoCapture(0)

#起動と画面表示まで
while(1):
    #capture frameの作成
    _, frame = cap.read()

    #originalの反転（鏡状態）
    original = cv2.flip(frame, 1)

    #binarization
    gray = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)

    #画像処理
    s_img, biggest = inputs(original)

    try:
        cv2.imshow('Red', GXGY(biggest, s_img, original))    
    except:#赤色を認識できなかったときは生画像を表示
        cv2.imshow('Red', original)            
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
