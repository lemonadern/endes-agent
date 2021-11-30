import cv2


def get_centroid(contour):
    # 輪郭のモーメントを計算する
    moment = cv2.moments(contour)
    # モーメントから重心を計算する
    center_x = moment["m10"] / moment["m00"]
    center_y = moment["m01"] / moment["m00"]
    return center_x, center_y
