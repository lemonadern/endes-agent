import cv2

contours = []

for i, cnt in enumerate(contours):
    # 輪郭のモーメントを計算する。
    M = cv2.moments(cnt)
    # モーメントから重心を計算する。
    cx = M["m10"] / M["m00"]
    cy = M["m01"] / M["m00"]
    print(f"contour: {i}, centroid: ({cx:.2f}, {cy:.2f})")
