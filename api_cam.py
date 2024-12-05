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
