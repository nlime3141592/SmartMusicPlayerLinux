from flask import Flask
from flask import render_template

import proc
import multiprocessing as mp
import process_context as pctx
import shared_memory as shmem

websv = Flask(__name__)

__proc_test = None
__cntx_test = None

@websv.route("/test")
def test():
    return render_template("./test.html")

@websv.route("/test/1")
def test_send():
    global __cntx_test
    __cntx_test.shmem.write(1)
    return render_template("./test.html")

def create_proc_test():
    proc_ctx = pctx.ProcessContext()
    proc_ctx.name = "PROC_TEST"
    proc_ctx.shmem = shmem.SharedMemory(mp.Manager())
    import test_handler as ts
    proc_ctx.handler_init = ts.init
    proc_ctx.handler_update = ts.update
    proc_ctx.handler_final = ts.final

    args = (proc_ctx,)

    process = mp.Process(target=proc.main, daemon=False, args=args)
    return process, proc_ctx

def create_proc_db():
    proc_ctx = pctx.ProcessContext()
    proc_ctx.name = "PROC_DB"
    proc_ctx.shmem = shmem.SharedMemory(mp.Manager())

    import db_handler as db
    proc_ctx.handler_init = db.init
    proc_ctx.handler_update = db.update
    proc_ctx.handler_final = db.final

    args = (proc_ctx,)

    process = mp.Process(target=proc.main, daemon=False, args=args)
    return process, proc_ctx

def main():
    print("server will start after some seconds.")
    
    global __proc_test, __cntx_test
    __proc_test, __cntx_test = create_proc_test()
    __proc_test.start()

    websv.run(host="0.0.0.0", debug=True, port=5000, use_reloader=False)
    print("\n", end="")

    __cntx_test.shmem.write(0)
    __proc_test.join()
    print("server closed.")

if __name__ == "__main__":
    main()
