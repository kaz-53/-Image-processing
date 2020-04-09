import cv2

print("画像に含まれるエッジを表示するプログラムです。")

# 画像の読込　(例：example.jpg)
image = cv2.imread(str(input("読み込む画像ファイルの名前を入力してください:")))

#エッジの検出
edges = cv2.Canny(image,100,200)

# 画像を表示
cv2.imshow("image", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()