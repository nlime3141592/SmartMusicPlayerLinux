from flask import render_template
from flask import redirect
from flask import request
from flask.views import MethodView

import logmodule as logger
from service_tokenizer import ServiceTokenizer

class CamLiveApi(MethodView):
    @staticmethod
    def init(websv, proc_cntx):
        api = CamLiveApi.as_view("cam_live_api", websv, proc_cntx)
        websv.add_url_rule("/cam/live/image", view_func=api, methods=["POST"])

    def __init__(self, websv, proc_cntx):
        self.__websv = websv
        self.__cntx = proc_cntx
        self.__logger_name = "CamLiveAPI"

    def redirect(self):
        return render_template("./cam.html")

    def post(self):
        service_type = request.path.split("/")[3]

        if service_type == "image":
            self.__cntx.shmem.write("cam;live;image;")

            if self.__cntx.shmem.read() == "1":
                length = self.__cntx.shmem.read()
                frame = self.__cntx.shmem.read()
                return Response(self.__generate_frames(frame), mimetype="multipart/x-mixed-replace; boundary=frame")
            else:
                return self.redirect()
        else:
            logger.print_log("Invalid service requested, rejects.", logger_name=self.__logger_name)
            return self.redirect() # TODO: Show error page.

    def __generate_frames(self, frame):
        yield (b"--frame\n"b"Content-Type: image/jpeg\n\n" + frame + b"\n\n")

class CamApi(MethodView):
    @staticmethod
    def init(websv, proc_cntx):
        api = CamApi.as_view("cam_api", websv, proc_cntx)
        websv.add_url_rule("/cam", view_func=api, methods=["GET"])
        CamLiveApi.init(websv, proc_cntx)

    def __init__(self, websv, proc_cntx):
        self.__websv = websv
        self.__cntx = proc_cntx
        self.__logger_name = "CamAPI"

        self.__websv.config["CAM_IMG_FOLDER_0"] = "./cam/img0/"
        self.__websv.config["CAM_IMG_FOLDER_1"] = "./cam/img1/"
        self.__websv.config["CAM_VIDEO_FOLDER"] = "./cam/video/"

    def get(self):
        return render_template("./cam.html")
