# 양쪽 눈 동공 찾기
import cv2 as cv
import numpy as np

fullvideo = 'IMG_0192.mov'

cap = cv.VideoCapture(fullvideo)  # 파일명 넣기'originalleft.avi'
cap.set(cv.CAP_PROP_FPS,60)
cap.set(3, 640)  # Set Size ( Width )
cap.set(4, 480)  # Set SizE ( Height )
wl = 0
hl = 0
xl = 0
yl = 0
cv.namedWindow('roi_left')
cv.namedWindow('roi_right')
f1 = open("left.txt", mode='wt')
f2 = open("right.txt", mode='wt')

fps = cap.get(cv.CAP_PROP_FPS)
# 트랙바
def nothing(x):
    pass

cv.createTrackbar('left', 'roi_left', 0, 255, nothing)
cv.setTrackbarPos('left', 'roi_left', 28)
cv.createTrackbar('right', 'roi_right', 0, 255, nothing)
cv.setTrackbarPos('right', 'roi_right', 25)

kernel = np.ones((11, 11), np.uint8)

while True:
    ret, frame = cap.read(0)

    #print("fps =", fps)
    if not ret:
        break

    roi_left = frame.copy
    roi_left = frame[300:600, 400:800]  # [y:h, x,w]

    rows, cols, _ = roi_left.shape

    gray_roi = cv.cvtColor(roi_left, cv.COLOR_BGR2GRAY)
    gray_roi = cv.medianBlur(gray_roi, 5)

    gray_roi = cv.erode(gray_roi, kernel, iterations=3)  # 침식
    gray_roi = cv.dilate(gray_roi, kernel, iterations=3)  # 팽창 연산
    gray_roi = cv.morphologyEx(gray_roi, cv.MORPH_CLOSE, kernel)

    left_thres = cv.getTrackbarPos('left', 'roi_left')  # 트랙바에서 값 가져오기

    _, pupil_threshold2 = cv.threshold(gray_roi, left_thres, 255, cv.THRESH_BINARY_INV)
    _, pupil_contours2, _ = cv.findContours(pupil_threshold2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    pupil_contours2 = sorted(pupil_contours2, key=lambda x: cv.contourArea(x), reverse=True)

    for cnt2 in pupil_contours2:  # 동공
        (x2, y2, w2, h2) = cv.boundingRect(cnt2)
        rad2 = (int)(w2 / 2)
        x_val2 = x2 + int(w2 / 2)
        y_val2 = y2 + int(h2 / 2)
        #cv.drawContours(roi_left, [cnt2], -1, (0, 0, 255), 2)
        cv.circle(roi_left, (x_val2, y_val2), 2, (0, 255, 0), -1)
        cv.circle(roi_left, (x_val2, y_val2), rad2, (255, 0, 0), 2)
        f1.write(str(x_val2) + "\t" + str(y_val2) + "\n")
        break

    # 오른쪽 눈
    roi_right = frame.copy
    roi_right = frame[300:600, 1200:1600]
    rows1, cols1, _ = roi_right.shape

    gray_roi2 = cv.cvtColor(roi_right, cv.COLOR_BGR2GRAY)
    gray_roi2 = cv.medianBlur(gray_roi2, 5)

    gray_roi2 = cv.erode(gray_roi2, kernel, iterations=3)  # 침식
    gray_roi2 = cv.dilate(gray_roi2, kernel, iterations=3)  # 팽창 연산
    gray_roi2 = cv.morphologyEx(gray_roi2, cv.MORPH_CLOSE, kernel)

    right_thres = cv.getTrackbarPos('right', 'roi_right')  # 트랙바에서 값 가져오기

    _, pupil_threshold = cv.threshold(gray_roi2, right_thres, 255, cv.THRESH_BINARY_INV)
    _, pupil_contours, _ = cv.findContours(pupil_threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    pupil_contours = sorted(pupil_contours, key=lambda x: cv.contourArea(x), reverse=True)

    for cnt in pupil_contours:  # 동공
        (x, y, w, h) = cv.boundingRect(cnt)
        rad = (int)(w / 2)
        x_val = 0
        y_val = 0
        x_val = x + int(w / 2)
        y_val = y + int(h / 2)
        #cv.drawContours(roi_right, [cnt], -1, (0, 0, 255), 2)
        cv.circle(roi_right, (x_val, y_val), 2, (0, 255, 0), -1)
        cv.circle(roi_right, (x_val, y_val), rad, (255, 0, 0), 2)
        f2.write(str(x_val) + "\t" + str(y_val) + "\n")

    cv.imshow("roi_left", roi_left)
    cv.imshow("roi_right", roi_right)
    cv.imshow("LeftPupil_Threshold", pupil_threshold2)
    cv.imshow("RightPupil_Threshold", pupil_threshold)

    if cv.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
f1.close()
f2.close()
