from flask import Flask
from flask import render_template

import api_root
import api_music
import api_cam

import os
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
    mpManager = mp.Manager()

    proc_ctx = pctx.ProcessContext()
    proc_ctx.name = "PROC_SERVICE"
    proc_ctx.shmem = shmem.SharedMemory(mpManager)
    proc_ctx.cam_bytes = bytearray(640 * 480 * 3)
    proc_ctx.cam_lock = mpManager.Lock()
    
    proc_ctx.current_dir = os.path.abspath(".")

    import service_handler as sv
    proc_ctx.handler_init = sv.init
    proc_ctx.handler_update_always = sv.update_always
    proc_ctx.handler_update = sv.update
    proc_ctx.handler_final = sv.final

    args = (proc_ctx,)

    process = mp.Process(target=proc.main, daemon=False, args=args)
    return process, proc_ctx

def create_proc_db():
    mpManager = mp.Manager()

    proc_ctx = pctx.ProcessContext()
    proc_ctx.name = "PROC_DB"
    proc_ctx.shmem = shmem.SharedMemory(mpManager)
    
    proc_ctx.current_dir = os.path.abspath(".")

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
    api_root.init(websv, __cntx_service)
    api_music.init(websv, __cntx_service)
    api_cam.init(websv, __cntx_service)

    __proc_service.start()
    websv.run(host="0.0.0.0", debug=True, port=5000, use_reloader=False)
    print("\n", end="")

    __cntx_service.shmem.write(0)
    __proc_service.join()
    logger.print_log("Server closed.", logger_name=__logger_name)

if __name__ == "__main__":
    main()
