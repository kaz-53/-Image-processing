#赤色で二植化、重心検出・描画するプログラム
def LinePicture(state,pic,token,url,headers): #画像を送信する関数
	files = {"imageFile": open(pic, "rb")}
	payload = {'message': "%s:%s" %(state,pic)}
	res = requests.post(url, data = payload, headers = headers, files = files)
	if str(res) == '<Response [200]>':
		print ('%sを送信しました。' %(state))

def LineMessage(msg,token,url,headers): #メッセージのみを送信する関数
	payload = {'message':msg}
	requests.post(url,data=payload,headers=headers)

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

def inputs(pic_name):
    img_def = cv2.imread(pic_name)  # 画像ファイル名から画像データの読み込み(同じディレクトリにあること)
    img_red = BGR_extraction(img_def, np.array([0, 0, 110]), np.array([100, 60, 255]))  # 赤色だけ抽出(BGRで色の上限・下限を設定)
    hsv = cv2.cvtColor(img_red, cv2.COLOR_BGR2HSV)  # BGRをHSVに変換
    h_img, s_img, v_img = cv2.split(hsv)  # HSVに分解
    cv2.imwrite(pic_rename[:-4] + "_mask.jpg", s_img)  # マスク画像を保存
    ret, img_bl = cv2.threshold(s_img, 0, 255,cv2.THRESH_BINARY) 
    contours, hierarchy = cv2.findContours(img_bl, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 輪郭検知
    biggest = max(contours, key=lambda x: cv2.contourArea(x))  # 一番大きい輪郭を選択する。
    return img_def,img_red,img_bl,s_img,biggest#元画像、赤の画像、黒の画像、白黒の画像、一番大きい輪郭

def GXGY(biggest,s_img,img_def):
    # 重心
    M = cv2.moments(biggest)#biggestは一番大きい輪郭の情報
    cx = int(M["m10"] / M["m00"])  # 重心のｘ座標
    cy = int(M["m01"] / M["m00"])  # 重心のｙ座標
    h, w = s_img.shape  # ファイルサイズの取得(h×w=高さ×幅)
    hh = int(h / 2)  # 高さの半分
    hw = int(w / 2)  # 幅の半分（x,y=hw,hhで中心の座標になる）
    x = cx - hw  # 水平方向における重心の中心からの距離
    y = hh - cy  # 鉛直方向における重心の中心からの距離
    cv2.circle(img_def, (cx, cy), 10, 300, -1, 4)
    # (画像,中心座標,円の半径,円の色,円の線の太さ(負で塗りつぶし) thickness=1,線の種類 lineType=8, shift=0)
    return x,y



import sys
import cv2
import requests
import numpy as np

print("赤色で二植化、重心検出・描画・lineに送信するプログラムです。\n")

#lineのトークンは https://notify-bot.line.me/ja/ のマイペース→トークンを発行する→発行したいトークを選択し発行　によって入手してください
token = 'mgmxnUGIrj6pScylisJNpVVWn4Pp4Uf0dgOuHUX4CC'#exampleです
url = 'https://notify-api.line.me/api/notify'
headers = {'Authorization': 'Bearer ' + token}

pic_name = input("読込画像ファイル名：")
pic_rename = input("保存画像ファイル名：")
print("\n「" + pic_rename + "」という名前で画像を保存します")

img_def,img_red,img_bl,s_img,biggest = inputs(pic_name)
x,y = GXGY(biggest,s_img,img_def)#重心座標
center(img_def)#画像の中心線を引く(白・黒色)
cv2.imwrite(pic_rename,img_def)#合成した画像を保存


state = "元画像"
LinePicture(state,pic_name,token,url,headers)

state = "マスク画像"
LinePicture(state,pic_rename[:-4] + "_mask.jpg",token,url,headers)

state = "加工済み画像"
LinePicture(state,pic_rename,token,url,headers)#加工済み画像を送信
LineMessage("x:"+str(x)+" "+"y:"+str(y),token,url,headers)#重心座標をlineに送信
