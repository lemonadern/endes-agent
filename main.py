#!/usr/bin/python3

import cv2
import numpy as np
import io
import picamera

# カメラの設定
stream = io.BytesIO()
camera = picamera.PiCamera()

camera_size = {
    'width': 300,
    'height': 300
}
camera.resolution = (camera_size['width'], camera_size['height'])

camera.hflip = True
camera.vflip = True


# 各種定数
red = (0, 0, 255)
blue = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

line_color = green
line_width = 2


center_of_img = {
    'x': camera_size['width'] // 2,
    'y': camera_size['height'] // 2,
}

target_area_side_length = 100
target_area = {
    'x_left': center_of_img['x'] - target_area_side_length // 2,
    'x_right': center_of_img['x'] + target_area_side_length // 2,
    'y_upper': center_of_img['y'] + target_area_side_length // 2,
    'y_lower': center_of_img['y'] - target_area_side_length // 2,
}

# state vaiables
reticle_color = white
degree: int = 0


def get_centroid(contour):  # 重心を求める
    # 輪郭のモーメントを計算する
    moment = cv2.moments(contour)
    # モーメントから重心を計算する
    center_x = moment["m10"] / moment["m00"]
    center_y = moment["m01"] / moment["m00"]
    return (center_x, center_y)


def get_max_contour(contours):  # 最大の面積を持つ輪郭を求める
    return max(contours, key=lambda x: cv2.contourArea(x))


def x_in_target_area(x):
    return target_area['x_left'] < x < target_area['x_right']


def y_in_target_area(y):
    return target_area['y_lower'] < y < target_area['y_upper']


def is_in_target_area(x, y):
    return x_in_target_area(x) and y_in_target_area(y)


while(True):
    # カメラからの画像
    camera.capture(stream, format="jpeg")
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
    stream.seek(0)

    # hsv形式に変換
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = img_hsv[:, :, 0]
    s = img_hsv[:, :, 1]
    v = img_hsv[:, :, 2]

    # 緑色のマスク画像を生成
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h > 30) & (h < 85)) & (s > 128)] = 255

    # マスク画像の輪郭を取得
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 該当領域の最大面積部分を取得
    contour = get_max_contour(contours)
    cv2.drawContours(img, [contour], 0, line_color, line_width)

    # 重心を取得
    centroid = get_centroid(contour)
    # 重心を中心に円を描画(塗りつぶし)
    cv2.circle(img, centroid, 10, red, thickness=-1)

    # # 重心のx座標がターゲット領域内にあるかどうかを判定
    # if x_in_target_area(centroid[0]):
    #     pass
    # else:
    #     if centroid[0] < target_area['x_left']:
    #         pass  # 右にうごかす
    #     else:
    #         pass  # 左にうごかす

    # # 重心のy座標がターゲット領域内にあるかどうかを判定
    # if y_in_target_area(centroid[1]):
    #     pass
    # else:
    #     if centroid[1] < target_area['y_lower']:
    #         pass  # 上にうごかす
    #     else:
    #         pass  # 下にうごかす

    if is_in_target_area(centroid[0], centroid[1]):
        reticle_color = green
    else:
        reticle_color = white
    # ターゲット領域を描画
    cv2.rectangle(img, (target_area['x_left'], target_area['y_upper']),
                  (target_area['x_right'], target_area['y_lower']), reticle_color, thickness=5)

    cv2.imshow("contour image", img)
    if cv2.waitKey(10) & 0xFF == ord(" "):
        break

cv2.imwrite("caputureImage.jpg", img)
cv2.destroyAllWindows()
