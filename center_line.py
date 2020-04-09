# 画像の中心線を引く関数
import cv2

#このプログラムファイルがあるディレクトリの画像ファイル名を入力してください
def center(img_name,img_rename):#描画する画像の名前と保存する画像の名前を入力　(例：example.jpg)
    img = cv2.imread(img_name)
    try:
        h, w, c = img.shape  # 画像の高さ、幅、色データ カラーの時
    except:
        h, w, = img.shape  # 画像の高さ、幅、色データ　白黒の時
    ch = int(h / 2)
    cw = int(w / 2)
    cv2.line(img, (cw, 0), (cw, h), (0, 0, 0))  # 線の色が黒の時はすべて0、白の時はすべて255
    cv2.line(img, (0, ch), (w, ch), (0, 0, 0))  # (B,G,R)の値を0~255で指定する。

    # 画像を表示(画像サイズが大きい場合見切れてしまうことを確認しています。保存された画像の表示の際には問題を確認していません。)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite(img_rename,img)#画像を保存


print("画像の中心線を表示するプログラムです。")

# 関数呼び出し
center(input("画像ファイルの名前を入力してください:"),input("保存する画像の名前を入力してください:"))
print("画像の保存が完了しました")
