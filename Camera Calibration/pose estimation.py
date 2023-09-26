import numpy as np
import cv2 as cv
import glob

# Load previously saved data
with np.load('CameraParameters.npz') as file:
    mtx, dist, rvecs, tvecs = [file[i] for i in ('cameraMatrix', 'distortion', 'rotation', 'translation')]


def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 10)
    img = cv.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 10)
    img = cv.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 10)

    return img


def drawBoxes(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)

    # draw ground floor in green
    img = cv.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), -3)

    # draw pillars in blue color
    for i, j in zip(range(4), range(4, 8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)

    # draw top layer in red color
    img = cv.drawContours(img, [imgpts[4:]], -1, (0, 0, 255), 3)

    return img


criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
chessBoardSize = (6, 8)

objp = np.zeros((chessBoardSize[0] * chessBoardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessBoardSize[0], 0:chessBoardSize[1]].T.reshape(-1, 2) * 2.5
axis = np.float32([[7.5, 0, 0], [0, 7.5, 0], [0, 0, -7.5]]).reshape(-1, 3)
axisBoxes = np.float32([[0, 0, 0], [0, 7.5, 0], [7.5, 7.5, 0], [7.5, 0, 0],
                        [0, 0, -7.5], [0, 7.5, -7.5], [7.5, 7.5, -7.5], [7.5, 0, -7.5]])

for image in glob.glob('../LapseIt-Sequence/*.jpg'):

    img = cv.imread(image)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, chessBoardSize, None)

    if ret:

        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # Find the rotation and translation vectors.
        ret, rvecs, tvecs = cv.solvePnP(objp, corners2, mtx, dist)

        if ret:
            # Compute distance between camera and object
            print('Distance Vector:', tvecs)
            print('Distance:', np.linalg.norm(tvecs), '\n')
        else:
            print('Failed to estimate object pose')

        # Project 3D points to image plane
        imgpts, jac = cv.projectPoints(axisBoxes, rvecs, tvecs, mtx, dist)

        img = drawBoxes(img, corners2, imgpts)
        img = cv.resize(img, (900, 900))
        cv.imshow('img', img)

        k = cv.waitKey(0) & 0xFF
        if k == ord('s'):
            cv.imwrite('pose' + image, img)

cv.destroyAllWindows()
