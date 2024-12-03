from flask import render_template
from flask import redirect
from flask import request
from flask.views import MethodView

import logmodule as logger

def init(websv, proc_cntx):
    __logger_name = "MainAPI"

    @websv.route("/", methods=["GET"])
    def root():
        return render_template("./index.html")