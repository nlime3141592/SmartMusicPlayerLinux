import main
import logmodule as logger
import music_handler as music
import db_handler as db
import service_tokenizer as tok

__proc_db = None
__cntx_db = None
__logger_name = "ServiceHandler"

def init():
    global __proc_db, __cntx_db
    __proc_db, __cntx_db = main.create_proc_db()
    __proc_db.start()

def update_always():
    music.update_always()

def update(service_string):
    global __cntx_db

    service_tokenizer = tok.ServiceTokenizer(service_string)
    service_type = service_tokenizer.read()

    if service_type == "music":
        music.update(service_tokenizer)
    else:
        logger.print_log(f"Unknown service requested, rejects. (message == {service_string})", logger_name=__logger_name)

def final():
    global __cntx_db, __proc_db
    __cntx_db.shmem.write(0)
    __proc_db.join()
