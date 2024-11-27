import os
import time

is_run = True
proc_ctx = None

def main(*args):
    os.setpgrp()
    proc_ctx = args[0]
    proc_ctx.shmem.swap_stream()

    print(f" * Process {proc_ctx.name} starts.")
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
    print(f" * Process {proc_ctx.name} ends.")
