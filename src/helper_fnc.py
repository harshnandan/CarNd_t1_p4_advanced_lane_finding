import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def plot_2_img(img1, img2):
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    f.tight_layout()
    
    ax1.imshow(img1)
    ax1.set_title('Original Image', fontsize=50)
    ax2.imshow(img2)
    ax2.set_title('Undistorted Image', fontsize=50)
    
    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
    
    plt.show()

def calibrateImg(imgList, nx, ny):
    
    
    for imgLoc in imgList:
        img = cv2.imread(imgLoc)
        # Convert to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # get corner of chess board, ret=1 if all corners are found
        ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
        # draw 
        if ret:
            imgpoints.append(corners)
            cornerMarkedImg = cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
            
            objpts = np.zeros((nx*ny, 3), dtype = np.float32)
            objpts[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)
            objpoints.append(objpts)
            
    return 
    #         return np.int8(img)
def undistort(img):
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[0:2][::-1], None, None)
    return cv2.undistort(img, mtx, dist, None, mtx)

def perspectiveTransform(corners, nx, ny):
    src = np.float32([corners[0], corners[nx-1], corners[-1], corners[-nx]])
#     dst = np.float32([[offset, offset], [image_size[0]-offset, offset], 
#                                  [image_size[0]-offset, image_size[1]-offset], 
#                                  [offset, image_size[1]-offset]])

# Read in an image
CalImgLocation = r'../camera_cal/*.jpg'
imgList = glob.glob(CalImgLocation)
imgpoints = []
objpoints = []
nx = 9;
ny = 5;

calibrateImg(imgList, nx, ny)
img = cv2.imread(imgList[0])
unDistortedImg= undistort(img)

plot_2_img(img, unDistortedImg)


