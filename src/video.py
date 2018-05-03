# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML
from image_processing_pipeline import *
import os
import glob
import numpy as np

class image_processor_class():
    def __init__(self, clip, outputFile):
        videoClip = clip
        #
        self.timeStepCounter = 0
        self.left_fit_prev = np.array([0, 0, 0])
        self.right_fit_prev = np.array([0, 0, 0])
        
        # process video clip
        white_clip = videoClip.fl_image(self.process_image) 
        white_clip.write_videofile(outputFile, audio=False)        
    
    def process_image(self, image):
        # calculate perspective transform
        M, M_inv = calcPerspectiveTransform()
    
        # read camera calibration
        mtx, dist = load_cam_calibration()
        
       
        imgUndistort, left_fit, right_fit = laneMarker(image, M, mtx, dist, \
                               self.timeStepCounter, self.left_fit_prev, self.right_fit_prev)
        
        self.left_fit_prev = left_fit
        self.right_fit_prev = right_fit
        
#         # smoothing
#         weight_previous = 0.8
#         weight_current = 1.0 - weight_previous
#         if self.timeStepCounter == 0`:
#             left_fit = left_fit 
#             right_fit = right_fit 
#         else:
#             left_fit  = weight_current * left_fit + weight_previous * self.left_fit_prev
#             right_fit = weight_current * right_fit + weight_previous * self.right_fit_prev
#         
#         self.left_fit_prev = left_fit
#         self.right_fit_prev = right_fit
            
        marked_img = project_lane(imgUndistort, left_fit, right_fit, M_inv)
        self.timeStepCounter = self.timeStepCounter + 1 
        
        return marked_img

if __name__ == '__main__':
    
    #fileList = glob.glob("../*.mp4")
    fileList = [r'project_video.mp4']
    
    # iterate over all files
    for figIdx, fileName in enumerate(fileList):
    
        inputFile = '../' + fileName
        outputFile = '../output_videos/' + fileName
        print(inputFile)
        
        #clip1 = VideoFileClip(inputFile).subclip(38, 43)
        clip1 = VideoFileClip(inputFile)
        
        # process video clip
        oImageProc = image_processor_class(clip1, outputFile)