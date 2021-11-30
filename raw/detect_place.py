#!/usr/bin/python3

import cv2
import numpy as np
import io
import picamera

stream = io.BytesIO()
camera = picamera.PiCamera()
camera.resolution = (256, 256)

camera.hflip = True
camera.vflip = True

lineColor=(0,255,0)
lineWidth= 2



while(True):
    # カメラからの画像
    camera.capture(stream, format="jpeg")
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
    stream.seek(0)
    
    # hsv形式に変換
    img=cv2.imdecode(data,cv2.IMREAD_COLOR)
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h = img_hsv[:,:,0]
    s = img_hsv[:,:,1]
    v = img_hsv[:,:,2]
    
    # 緑色のマスク画像を生成
    mask = np.zeros(h.shape,dtype=np.uint8)
    mask[((h > 30) & (h < 85)) & (s > 128)] = 255
    
    # マスク画像の輪郭を取得し描画
    contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours,-1,(192,192,192),2)
    
    # 該当領域の最大面積部分を取得
    if (len(contours) != 0):
        mContour = contours[0]
        maxArea = 0.0
        for contour in contours:
            area = cv2.contourArea(contour)
            if (area > maxArea):
                maxArea = area
                mContour = contour
        # 　最大面積部分の輪郭を黄緑で描画
        cv2.drawContours(img, [mContour],0,lineColor,lineWidth)
        # 最大面積部分の直線成分を取得
        vx,vy,x0,y0 = cv2.fitLine(mContour, cv2.DIST_L2, 0, 0.01,0.01)
        x1 = 0
        x2 = 256
        if (vx >= 0.00001):
            
            y1 = (vy / vx)*(x1 - x0) + y0
            y2 = (vy / vx)*(x2 - x0) + y0
            # フィットする線を引く
            cv2.line(img, (x1,y1),(x2,y2), lineColor,lineWidth)
        
    cv2.imshow("contour image", img)
    if cv2.waitKey(10) & 0xFF == ord(" "):
       break

cv2.imwrite("caputureImage.jpg", img)
cv2.destroyAllWindows()

