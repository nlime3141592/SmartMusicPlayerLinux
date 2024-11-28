import main
import logmodule as logger
import music_handler as music
import db_handler as db

__proc_db = None
__cntx_db = None
__logger_name = "ServiceHandler"

def init():
    global __proc_db, __cntx_db
    __proc_db, __cntx_db = main.create_proc_db()
    __proc_db.start()

def update(value):
    global __cntx_db

    tokens = value.split(";")

    if tokens[0] == None or tokens[0] == "":
        logger.print_log(f"Empty service requested. (message == {value})", logger_name=__logger_name)
    elif tokens[0] == "music":
        logger.print_log(f"Music service requested. (message == {value})", logger_name=__logger_name)
        music.update(tokens[1:])
    else:
        logger.print_log(f"Unknown service requested, rejects. (message == {value})", logger_name=__logger_name)

def final():
    global __cntx_db, __proc_db
    __cntx_db.shmem.write(0)
    __proc_db.join()
