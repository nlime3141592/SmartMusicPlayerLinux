from flask import render_template
from flask import redirect
from flask import request
from flask.views import MethodView

import logmodule as logger

class RootApi(MethodView):
    @staticmethod
    def init(websv, proc_cntx):
        api = RootApi.as_view("root_api", websv, proc_cntx)
        websv.add_url_rule("/", view_func=api, methods=["GET"])

    def __init__(self, websv, proc_cntx):
        self.__websv = websv
        self.__cntx = proc_cntx
        self.__logger_name = "MainAPI"

    def get(self):
        logger.print_log(f"Main page requested.", logger_name=self.__logger_name)
        return render_template("./index.html")
