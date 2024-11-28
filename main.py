from flask import Flask
from flask import render_template

from root_api import RootApi
from music_api import MusicApi

import proc
import multiprocessing as mp
import process_context as pctx
import shared_memory as shmem
import logmodule as logger

websv = Flask(__name__)

__logger_name = "MAIN"
__proc_service = None
__cntx_service = None

def create_proc_service():
    proc_ctx = pctx.ProcessContext()
    proc_ctx.name = "PROC_SERVICE"
    proc_ctx.shmem = shmem.SharedMemory(mp.Manager())

    import service_handler as sv
    proc_ctx.handler_init = sv.init
    proc_ctx.handler_update_always = sv.update_always
    proc_ctx.handler_update = sv.update
    proc_ctx.handler_final = sv.final

    args = (proc_ctx,)

    process = mp.Process(target=proc.main, daemon=False, args=args)
    return process, proc_ctx

def create_proc_db():
    proc_ctx = pctx.ProcessContext()
    proc_ctx.name = "PROC_DB"
    proc_ctx.shmem = shmem.SharedMemory(mp.Manager())

    import db_handler as db
    proc_ctx.handler_init = db.init
    proc_ctx.handler_update_always = db.update_always
    proc_ctx.handler_update = db.update
    proc_ctx.handler_final = db.final

    args = (proc_ctx,)

    process = mp.Process(target=proc.main, daemon=False, args=args)
    return process, proc_ctx

def main():
    logger.print_log("Server will starts after some seconds.", logger_name=__logger_name)
    
    global __proc_service, __cntx_service
    __proc_service, __cntx_service = create_proc_service()

    # TODO: Initialize APIs here.
    RootApi.init(websv, __cntx_service)
    MusicApi.init(websv, __cntx_service)

    __proc_service.start()
    websv.run(host="0.0.0.0", debug=True, port=5000, use_reloader=False)
    print("\n", end="")

    __cntx_service.shmem.write(0)
    __proc_service.join()
    logger.print_log("Server closed.", logger_name=__logger_name)

if __name__ == "__main__":
    main()
