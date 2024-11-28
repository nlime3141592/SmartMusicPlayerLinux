from shared_memory import SharedMemory

class ProcessContext:
    name: str
    shmem: SharedMemory
    handler_init: [..., any]
    handler_update_always: [..., any]
    handler_update: [..., any]
    handler_final: [..., any]

    def __init__(self):
        self.name = ""
        self.shmem = None
        self.handler_init = None
        self.handler_update_always = None
        self.handler_update = None
        self.handler_final = None
