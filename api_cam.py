from flask import render_template
from flask import redirect
from flask import request

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

        if proc_cntx.shmem.read() == "1":
            length = proc_cntx.shmem.read()
            frame = proc_cntx.shmem.read()
            return Response(self.__generate_frames(frame), mimetype="multipart/x-mixed-replace; boundary=frame")
        else:
            logger.print_log("Invalid service requested, rejects.", logger_name=__logger_name)
            return render_template("./cam.html")

    def __generate_frames(frame):
        yield (b"--frame\n"b"Content-Type: image/jpeg\n\n" + frame + b"\n\n")
