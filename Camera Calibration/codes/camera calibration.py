import numpy as np
import cv2 as cv
import glob

chessBoardSize = (8, 6)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.01)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessBoardSize[0] * chessBoardSize[1], 3), np.float32)
# we multiply the result by 0.25 because our squares sizes are 23*23 mm
objp[:, :2] = np.mgrid[0:chessBoardSize[0], 0:chessBoardSize[1]].T.reshape(-1, 2) * 2.3

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
images = glob.glob('../40 calibration (resized)/*.jpg')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, chessBoardSize, None)
    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (4, 4), (-1, -1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(img, chessBoardSize, corners2, ret)
        img = cv.resize(img, (900, 900))
        cv.imshow('img', img)
        cv.waitKey(500)

cv.destroyAllWindows()

# Calibration camera
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print("Camera Calibration: ", ret)
print("\nCamera Matrix: ", mtx)
print("\nDistortion Parameters: ", dist)
print("\nRotation Vectors: ", rvecs)
print("\nTranslation Vectors: ", tvecs)

np.savez("cameraParameters", cameraCalibration=ret, cameraMatrix=mtx, distortion=dist, rotation=rvecs, translation=tvecs)

# Re-projection error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
    mean_error += error
print("total error: {}".format(mean_error / len(objpoints)))
