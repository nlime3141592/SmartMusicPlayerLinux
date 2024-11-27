import main
import db_handler as db

__proc_db = None
__cntx_db = None

def init():
    global __proc_db, __cntx_db
    __proc_db, __cntx_db = main.create_proc_db()
    print("TYPE == %s" % (type(__cntx_db)))
    __proc_db.start()

def update(value):
    global __cntx_db

    print(" * Request service: %s" % (value))

    if value == "1" or value == 1:
        # NOTE: test for DB connection.
        print(" * TEST SERVICE STARTS.")
        __cntx_db.shmem.write(1)
        print(" * TEST SERVICE ENDS.")
        return

    tokens = value.split(";")

    if tokens[0] == "2":
        print("test 2")
    else:
        print(" * Reject service: %s" % (value))

def final():
    global __cntx_db, __proc_db
    __cntx_db.shmem.write(0)
    __proc_db.join()
