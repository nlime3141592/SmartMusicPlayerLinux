import os
import time

import logmodule as logger

is_run = True
proc_ctx = None

def main(*args):
    os.setpgrp()
    proc_ctx = args[0]
    proc_ctx.shmem.swap_stream()

    logger.print_log("Process starts.", logger_name=proc_ctx.name)
    proc_ctx.handler_init()

    while is_run == True:
        proc_ctx.shmem.update()
        if proc_ctx.shmem.can_read():
            value = proc_ctx.shmem.read()
            if value == "0" or value == 0:
                break
            else:
                proc_ctx.handler_update(value)
                continue

    proc_ctx.handler_final()
    logger.print_log("Process ends.", logger_name=proc_ctx.name)
