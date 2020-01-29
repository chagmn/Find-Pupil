# 한쪽 눈만 동공찾기
import cv2 as cv
import numpy as np

fullvideo = 'IMG_0192.mov'

cap = cv.VideoCapture(fullvideo)  # 파일명 넣기'originalleft.avi'
cap.set(3, 640)  # Set Size ( Width )
cap.set(4, 480)  # Set SizE ( Height )
wl = 0
hl = 0
xl = 0
yl = 0
cv.namedWindow('roi')
f = open("pupil_coordinates.txt", mode='wt')

# 트랙바
def nothing(x):
    pass
cv.createTrackbar('Pupil', 'roi', 0, 255, nothing)
cv.setTrackbarPos('Pupil', 'roi', 35)

kernel = np.ones((11, 11), np.uint8)

while True:
    ret, frame = cap.read(0)

    if not ret:
        break

    roi = frame
    roi = frame[250:600, 350:850]  # [start-y:y, start-x,x]

    rows, cols, _ = roi.shape

    gray_roi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    gray_roi = cv.medianBlur(gray_roi, 5)

    gray_roi = cv.erode(gray_roi, kernel, iterations=3)  # 침식
    gray_roi = cv.dilate(gray_roi, kernel, iterations=3)  # 팽창 연산
    gray_roi = cv.morphologyEx(gray_roi, cv.MORPH_CLOSE, kernel)

    pupil_th_val = cv.getTrackbarPos('Pupil', 'roi')  # 트랙바에서 값 가져오기

    _, pupil_threshold = cv.threshold(gray_roi, pupil_th_val, 255, cv.THRESH_BINARY_INV)
    _, pupil_contours, _ = cv.findContours(pupil_threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    pupil_contours = sorted(pupil_contours, key=lambda x: cv.contourArea(x), reverse=True)

    hough = frame
    hough = cv.resize(hough, dsize=(640, 480), interpolation=cv.INTER_AREA)
    rows, cols, _ = hough.shape
    cv.imshow("gray", gray_roi)

    circles = cv.HoughCircles(gray_roi, cv.HOUGH_GRADIENT, 1, 100, param1=120, param2=40, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        x, y, radius = circles[0][0]
        center = (x, y)
        cv.circle(hough, center, radius, (255, 0, 0), 2)
        cv.circle(hough, center, 3, (0, 255, 0), -1)
        f.write(str(x) + "\t" + str(y) + "\n")

    cv.imshow('Hough circle', hough)

    for cnt2 in pupil_contours:  # 동공
        (x2, y2, w2, h2) = cv.boundingRect(cnt2)
        rad = (int)(w2 / 2)
        x_val = x2 + int(w2 / 2)
        y_val = y2 + int(h2 / 2)
        cv.drawContours(roi, [cnt2], -1, (0, 0, 255), 2)
        cv.circle(roi, (x_val, y_val), 3, (0, 255, 0), -1)
        cv.circle(roi, (x_val, y_val), rad, (255, 0, 0), 2)
        break

    cv.imshow("roi", roi)
    cv.imshow("Pupil_Threshold", pupil_threshold)
    key = cv.waitKey(60)  # 45

    if key == ord('q'):
        break

cv.destroyAllWindows()
f.close()
#
