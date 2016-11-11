# -*- coding: utf-8 -*-
import cv2
import coldet as col

#################################
# 初期設定
#################################

cap = cv2.VideoCapture(0)
cap.set(3,640)  # カメラの横のサイズ
cap.set(4,480)  # カメラの縦のサイズ

cv2.namedWindow('image')
cv2.setMouseCallback('image', col.pick_color)

 #################################
 # while ループ
 #################################
while True:
    ret, im = cap.read()
    imc = im.copy()

    im_green, pos_x, pos_y, w, h = col.detect_color(imc)
    print "(x,y)=", pos_x, ",", pos_y
    cv2.imshow("green",im_green)
    cv2.imshow("image", imc)

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
