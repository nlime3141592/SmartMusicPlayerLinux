from flask import Flask
from shared_memory import SharedMemory

import multiprocessing as mp
import numpy as np

class ProcessContext:
    name: str
    shmem: SharedMemory
    cam_bytes: bytes
    cam_lock: mp.Lock
    current_dir: str
    websv: Flask
    handler_init: [..., any]
    handler_update_always: [..., any]
    handler_update: [..., any]
    handler_final: [..., any]

    def __init__(self):
        self.name = ""
        self.shmem = None
        self.cam_bytes = None
        self.cam_lock = None
        self.current_dir = None
        self.websv = None
        self.handler_init = None
        self.handler_update_always = None
        self.handler_update = None
        self.handler_final = None
