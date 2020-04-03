from time import sleep
import cv2

print("画像の大きさを表示するプログラムです。")
sleep(1)

#このプログラムファイルがあるディレクトリの画像ファイル名を入力してください(例：example.jpg)
pic_name = str(input("画像ファイルの名前を入力してください:"))

# 対象画像読み込み
img = cv2.imread(pic_name,cv2.IMREAD_COLOR)

# 画像の大きさを取得
height, width, channels = img.shape[:3]

#結果を出力
print("width: " + str(width))
print("height: " + str(height))