# -*- coding: utf-8 -*-
import cv2
import coldet as col


#################################
# 初期設定
#################################

cap = cv2.VideoCapture(0)
cap.set(3,640)  # カメラの横のサイズ
cap.set(4,480)  # カメラの縦のサイズ

#imageという名前のウィンドウを作成
cv2.namedWindow('image')

# ウィンドウにマウスイベントに応じた関数を関連づける
cv2.setMouseCallback('image', col.pick_color)

#################################
# while ループ
#################################
while True:
    # 画面キャプチャ
    ret, img = cap.read()
    img_a = img.copy()

    # 色認識
    img_detect, pos_x, pos_y, w, h = col.detect_color(img_a)
    print "(x,y)=", pos_x, ",", pos_y

    # 画面出力
    cv2.imshow("detect",img_detect)
    cv2.imshow("image", img_a)

    # キーが押されたらループから抜ける
    if cv2.waitKey(10) > 0:
          break

 #################################
 # 終了処理
 #################################

# キャプチャー解放
cap.release()
# ウィンドウ破棄
cv2.destroyAllWindows()
