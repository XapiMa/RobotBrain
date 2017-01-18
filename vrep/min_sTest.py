# -*- coding: utf-8 -*-
import sys
import minSim
import time
import cv2
# コマンドライン引数でパラメータを指定して実行する
# 学校のMac環境なら275が妥当。回転しすぎるなら大きく、回転不足なら小さくする
param =275
if len(sys.argv)>=1:
	param =float(sys.argv[1])
rmb = minSim.HurrySim("rmb",param)


b1_count = 0
b2_count = 0
while True:
    rmb.go()
    time.sleep(0.01)
