from flask import render_template
from flask import redirect
from flask import request
from flask.views import MethodView

import logmodule as logger

class MusicControlApi(MethodView):
    @staticmethod
    def init(websv, proc_cntx):
        api = MusicControlApi.as_view("music_control_api", websv, proc_cntx)
        websv.add_url_rule("/music/control/next", view_func=api, methods=["POST"])
        websv.add_url_rule("/music/control/prev", view_func=api, methods=["POST"])
        websv.add_url_rule("/music/control/change_shuffle", view_func=api, methods=["POST"])
        websv.add_url_rule("/music/control/change_loop", view_func=api, methods=["POST"])
        websv.add_url_rule("/music/control/toggle_like", view_func=api, methods=["POST"])
        websv.add_url_rule("/music/control/volup", view_func=api, methods=["POST"])
        websv.add_url_rule("/music/control/voldown", view_func=api, methods=["POST"])
        websv.add_url_rule("/music/control/volmute", view_func=api, methods=["POST"])
        websv.add_url_rule("/music/control/toggle_playing", view_func=api, methods=["POST"])

    def __init__(self, websv, proc_cntx):
        self.__websv = websv
        self.__cntx = proc_cntx
        self.__logger_name = "MusicControlAPI"

    def redirect(self):
        return render_template("./music.html")

    def post(self):
        service_type = request.path.split()[3]

        if service_type == "next":
            self.__cntx.shmem.write("music;control;next;")
            return self.redirect()
        elif service_type == "prev":
            self.__cntx.shmem.write("music;control;prev;")
            return self.redirect()
        elif service_type == "change_shuffle":
            self.__cntx.shmem.write("music;control;change_shuffle;")
            return self.redirect()
        elif service_type == "change_loop":
            self.__cntx.shmem.write("music;control;change_loop;")
            return self.redirect()
        elif service_type == "toggle_like":
            self.__cntx.shmem.write("music;control;toggle_like;")
            return self.redirect()
        elif service_type == "volup":
            self.__cntx.shmem.write("music;control;volup;")
            return self.redirect()
        elif service_type == "voldown":
            self.__cntx.shmem.write("music;control;voldown;")
            return self.redirect()
        elif service_type == "volmute":
            self.__cntx.shmem.write("music;control;volmute;")
            return self.redirect()
        elif service_type == "toggle_playing":
            self.__cntx.shmem.write("music;control;toggle_playing;")
            return self.redirect()
        else:
            logger.print_log("Invalid service requested, rejects.", logger_name=self.__logger_name)
            return self.redirect() # TODO: Show error page.

class MusicApi(MethodView):
    @staticmethod
    def init(websv, proc_cntx):
        api = MusicApi.as_view("music_api", websv, proc_cntx)
        websv.add_url_rule("/music", view_func=api, methods=["GET"])
        MusicControlApi.init(websv, proc_cntx)

    def __init__(self, websv, proc_cntx):
        self.__websv = websv
        self.__cntx = proc_cntx
        self.__logger_name = "MusicAPI"

        self.__websv.config["MUSIC_FOLDER"] = "./music/data"
        self.__websv.config["PLAYLIST_FOLDER"] = "./music/playlists"

    def get(self):
        return render_template("./music.html")