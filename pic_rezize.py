import cv2
from time import sleep

print("画像の大きさを変更するプログラムです。")
sleep(1)

#このプログラムファイルがあるディレクトリの画像ファイル名を入力してください(例：example.jpg)
pic_name = input("大きさを変更する画像ファイルの名前を入力してください:")

#保存するファイル名を拡張子まで入力してください(例：example.jpg)
pic_rename = input("画像ファイルの新しい名前を入力してください:")

img = cv2.imread(pic_name)#行（高さ）x 列（幅）x 色（3）
width,height= map(int,input("新しい画像の width　height を半角スペース区切りで入力してください：").split())
img = cv2.resize(img,(width, height))#画像サイズの変更
cv2.imwrite(pic_rename,img)#画像の保存
print("画像のリサイズが完了しました。")
print("新しい画像の名前:" + pic_rename)