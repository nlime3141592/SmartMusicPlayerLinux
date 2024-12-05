import os
import glob
import cv2
import time
import datetime

import logmodule as logger

c_CAM_INDEX = -1

# NOTE:
# DO NOT exceed webcam hardware's maximum frame rate.
# Recommends setting c_FRAME_RATE to 24 or 30.
c_FRAME_RATE = 30

# NOTE: c_FRAME_RATE_VIDEO = c_FRAME_RATE * videoLengthSeconds
c_FRAME_RATE_VIDEO = c_FRAME_RATE * 5

__delta_time = 0.033 #1.0 / c_FRAME_RATE
__frame_time = 0
__frame_number = -1
__timestamp_beg = time.time()
__timestamp_end = time.time()

__logger_name = "WEBCAM"

__dir_images = [
    "./cam/img0/",
    "./cam/img1/"
]
__idx_dir_images = 0
__img_fname = "%08d.jpg"

__dir_video = "./cam/video/"
__videos = [ None, None ]

__capture = cv2.VideoCapture(0)
__read_complete, __frame = __capture.read()

def init_video():
    global c_FRAME_RATE
    global __dir_video
    
    h, w, l = (480, 640, 3)
    
    now = datetime.datetime.now()
    now_str = now.strftime("%Y%m%d_%H%M%S")
    fname = __dir_video + f"{now_str}.mp4"
    
    wr = cv2.VideoWriter_fourcc(*"mp4v")
    return cv2.VideoWriter(fname, wr, c_FRAME_RATE, (w, h))

def save_video():
    global __videos
    global __idx_dir_images

    __videos[__idx_dir_images].release()
    logger.print_log("Video Saved.", logger_name=__logger_name)

def create_video():
    global __frame_number
    global __idx_dir_images

    __idx_dir_images = 1 - __idx_dir_images
    __frame_number = -1
    __videos[__idx_dir_images] = init_video()

def record_video():
    global __read_complete, __frame
    global __capture
    global __delta_time
    global __frame_time
    global __frame_number
    global __timestamp_beg, __timestamp_end
    global __idx_dir_images
    global __dir_images, __img_fname
    global __videos

    __read_complete, __frame = __capture.read()

    if __name__ == "__main__":
        cv2.imshow("webcam", __frame)
        cv2.waitKey(1)

    if __frame_time >= __delta_time:
        __frame_number += 1
        fname = __dir_images[__idx_dir_images] + "{:08d}.jpg".format(__frame_number)
        cv2.imwrite(fname, __frame)
        __videos[__idx_dir_images].write(__frame)

        while __frame_time >= __delta_time:
            __frame_time -= __delta_time

        if __frame_number >= c_FRAME_RATE_VIDEO - 1:
            save_video()
            create_video()

    __timestamp_end = time.time()
    __frame_time += (__timestamp_end - __timestamp_beg)
    __timestamp_beg = __timestamp_end

def start_cam():
    global __timestamp_beg
    global __timestamp_end
    global __dir_images
    global __videos
    
    def clear_imgs(dir):
        files = glob.glob(os.path.join(dir, "*.jpg"))
        for file in files:
            if os.path.isfile(file):
                os.remove(file)
                
    clear_imgs(__dir_images[0])
    clear_imgs(__dir_images[1])
    
    __videos[0] = init_video()

    __timestamp_beg = time.time()
    __timestamp_end = time.time()

def update_always():
    record_video()

def final():
    save_video()

if __name__ == "__main__":
    try:
        cv2.imshow("webcam", __frame)
        logger.print_log("Webcam will start 3 seconds after.")
        time.sleep(3)
        start_cam()
        logger.print_log("Webcam starts.")
        while True:
            update_always()
    finally:
        create_video()
        __capture.release()
        cv2.destroyAllWindows()