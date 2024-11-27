from shared_memory import SharedMemory

class ProcessContext:
    name: str
    shmem: SharedMemory
    handler_init: [..., any]
    handler_update: [..., any]
    handler_final: [..., any]
