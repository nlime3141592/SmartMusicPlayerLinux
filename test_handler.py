import main
import db_handler as db

__proc_db = None
__cntx_db = None

def init():
    global __proc_db, __cntx_db
    __proc_db, __cntx_db = main.create_proc_db()
    __proc_db.start()

def update(value):
    global __cntx_db

    print(" * Received Value == %s" % (value))
    __cntx_db.shmem.write(value)

def final():
    global __cntx_db, __proc_db
    __cntx_db.shmem.write(0)
    __proc_db.join()
