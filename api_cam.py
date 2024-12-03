from flask import render_template
from flask import redirect
from flask import request

import numpy as np

import logmodule as logger
from service_tokenizer import ServiceTokenizer

def init(websv, proc_cntx):
    __logger_name = "CamAPI"

    @websv.route("/cam", methods=["GET"])
    def cam():
        return render_template("./cam.html")

    @websv.route("/cam/live/image", methods=["POST"])
    def cam_live_image():
        proc_cntx.shmem.write("cam;live;image;")

        shape = proc_cntx.shmem.read()
        dtype = proc_cntx.shmem.read()
        img_bytes = proc_cntx.shmem.read()

        frame = np.frombuffer(img_bytes, dtype=dtype).reshape(shape)

        return Response(__generate_frames(frame), mimetype="multipart/x-mixed-replace; boundary=frame")

    def __generate_frames(frame):
        yield (b"--frame\n"b"Content-Type: image/jpeg\n\n" + frame + b"\n\n")
