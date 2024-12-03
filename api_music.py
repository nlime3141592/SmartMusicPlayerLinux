from flask import render_template
from flask import redirect
from flask import request

import logmodule as logger

def init(websv, proc_cntx):
    __logger_name = "MusicAPI"

    @websv.route("/music", methods=["GET"])
    def music():
        return render_template("./music.html")

    @websv.route("/music/control/next", methods=["POST"])
    def music_control_next():
        proc_cntx.shmem.write("music;control;next;")
        return render_template("./music.html")

    @websv.route("/music/control/prev", methods=["POST"])
    def music_control_prev():
        proc_cntx.shmem.write("music;control;prev;")
        return render_template("./music.html")

    @websv.route("/music/control/change_shuffle", methods=["POST"])
    def music_control_changeShuffle():
        proc_cntx.shmem.write("music;control;change_shuffle;")
        return render_template("./music.html")

    @websv.route("/music/control/change_loop", methods=["POST"])
    def music_control_changeLoop():
        proc_cntx.shmem.write("music;control;change_loop;")
        return render_template("./music.html")

    @websv.route("/music/control/toggle_like", methods=["POST"])
    def music_control_toggleLike():
        proc_cntx.shmem.write("music;control;toggle_like;")
        return render_template("./music.html")

    @websv.route("/music/control/volup", methods=["POST"])
    def music_control_volup():
        proc_cntx.shmem.write("music;control;volup;")
        return render_template("./music.html")

    @websv.route("/music/control/voldown", methods=["POST"])
    def music_control_voldown():
        proc_cntx.shmem.write("music;control;voldown;")
        return render_template("./music.html")

    @websv.route("/music/control/volmute", methods=["POST"])
    def music_control_volmute():
        proc_cntx.shmem.write("music;control;volmute;")
        return render_template("./music.html")

    @websv.route("/music/control/toggle_playing", methods=["POST"])
    def music_control_togglePlaying():
        proc_cntx.shmem.write("music;control;toggle_playing;")
        return render_template("./music.html")
