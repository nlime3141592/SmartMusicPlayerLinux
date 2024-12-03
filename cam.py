import os
import glob
import cv2
import time
import datetime
import subprocess

import logmodule as logger

c_CAM_INDEX = 0

# NOTE:
# DO NOT exceed webcam hardware's maximum frame rate.
# Recommends setting c_FRAME_RATE to 24 or 30.
c_FRAME_RATE = 30

# NOTE: c_FRAME_RATE_VIDEO = c_FRAME_RATE * videoLengthSeconds
c_FRAME_RATE_VIDEO = c_FRAME_RATE * 10

__delta_time = 0.033 #1.0 / c_FRAME_RATE
__frame_time = 0
__frame_number = 0
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

__capture = cv2.VideoCapture(0)
__read_complete, __frame = __capture.read()

__proc_video = None

def record_video():
    global __read_complete, __frame
    global __capture
    global __delta_time
    global __frame_time
    global __frame_number
    global __timestamp_beg, __timestamp_end
    global __idx_dir_images
    global __dir_images, __img_fname

    __read_complete, __frame = __capture.read()

    if __name__ == "__main__":
        cv2.imshow("webcam", __frame)
        cv2.waitKey(1)

    if __frame_time >= __delta_time:
        __frame_number += 1
        fname = __dir_images[__idx_dir_images] + "{:08d}.jpg".format(__frame_number)
        cv2.imwrite(fname, __frame)

        while __frame_time >= __delta_time:
            __frame_time -= __delta_time

    __timestamp_end = time.time()
    __frame_time += (__timestamp_end - __timestamp_beg)
    __timestamp_beg = __timestamp_end

def create_cli_command(tokens):
    command = ""
    for token in tokens:
        command += token + " "
    return command

def get_ffmpeg_command():
    global __ffmpeg_args
    global __dir_video

    #import pytz
    #timezone = pytz.timezone("Asia/Seoul")
    
    command = ""

    for token in __ffmpeg_args:
        command += token + " "

    return command

def get_live_img_data():
    global __frame
    global __dir_images
    global __idx_dir_images

    # NOTE: Busy-Waiting
    while __frame_number < 0:
        pass

    fname = __dir_images[__idx_dir_images] + "{:08d}.jpg".format(__frame_number)
    return os.path.abspath(fname)

def create_video():
    global __dir_video
    global __frame_number
    global __idx_dir_images
    global __proc_video

    if __frame_number < c_FRAME_RATE_VIDEO - 1:
        return

    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d-%H-%M-%S")
    fname = __dir_video + f"{now_str}.mp4"

    ffmpeg_args = [
    "ffmpeg",
    "-framerate", str(c_FRAME_RATE),
    "-i", __dir_images[__idx_dir_images] + __img_fname,
    "-c:v", "libx264",
    "-r", str(c_FRAME_RATE),
    "-pix_fmt", "yuv420p",
    fname
    ]

    command = create_cli_command(ffmpeg_args)
    logger.print_log(f"Create Video: {command}")
    __proc_video = subprocess.Popen(command)
    __frame_number = -1
    __idx_dir_images = 1 - __idx_dir_images

def check_video_creation_complete():
    global __proc_video
    global __dir_images
    global __idx_dir_images

    if __proc_video == None:
        return
    elif __proc_video.poll() is not None:
        __proc_video = None
        logger.print_log("Video creation completed.", logger_name=__logger_name)

        files = glob.glob(os.path.join(__dir_images[1 - __idx_dir_images], "*.jpg"))

        for file in files:
            if os.path.isfile(file):
                os.remove(file)

def start_cam():
    __timestamp_beg = time.time()
    __timestamp_end = time.time()

def generate_frame():
    global __read_complete, __frame

    if not __read_complete:
        return False, None

    read_complete, buffer = cv2.imencode(".jpg", __frame)

    if not read_complete:
        return False, None

    return True, buffer.tobytes()

def update_always():
    record_video()
    create_video()
    check_video_creation_complete()

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
        __capture.release()
        cv2.destroyAllWindows()