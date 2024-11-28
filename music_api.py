from flask import render_template
from flask import redirect
from flask import request
from flask.views import MethodView

import logmodule as logger

class MusicApi(MethodView):
    @staticmethod
    def init(websv, proc_cntx):
        api = MusicApi.as_view("music_api", websv, proc_cntx)
        websv.add_url_rule("/music/play", view_func=api, methods=["POST"])

    def __init__(self, websv, proc_cntx):
        self.__websv = websv
        self.__cntx = proc_cntx
        self.__logger_name = "MusicAPI"

        self.__websv.config["MUSIC_FOLDER"] = "./music/data"
        self.__websv.config["PLAYLIST_FOLDER"] = "./music/playlists"

    #def get(self):
        #return render_templates("index.html")

    def post(self):
        if request.path == "/music/play":
            self.__on_btn_click_music_play()
            return redirect("/")
        else:
            logger.print_log(f"Invalid service requested.", logger_name=self.__logger_name)
            return redirect("/")

    def __on_btn_click_music_play(self):
        logger.print_log(f"toggle_music service requested.", logger_name=self.__logger_name)
        self.__cntx.shmem.write("music;play;")
