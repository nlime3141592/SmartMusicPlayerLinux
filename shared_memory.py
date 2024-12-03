import multiprocessing as mp

class SharedMemory:
    def __init__(self, manager, buffer_size = 1024):
        self.__buffer_size = buffer_size
        self.__in = manager.list([None] * buffer_size)
        self.__out = manager.list([None] * buffer_size)
        self.__ptr_f = manager.Value("i", 0)
        self.__ptr_m = manager.Value("i", 0)
        self.__ptr_r = manager.Value("i", 0)

        self.__lock = mp.Lock()

    def swap_stream(self):
        self.__in, self.__out = self.__out, self.__in

    def update(self):
        self.__ptr_m.value = self.__ptr_r.value

    def can_write(self):
        return (self.__ptr_r.value + 1) % self.__buffer_size != self.__ptr_f.value

    def can_read(self):
        return self.__ptr_m.value != self.__ptr_f.value

    def write(self, value):
        with self.__lock:
            i = self.__ptr_r.value
            self.__out[i] = value
            self.__ptr_r.value = (i + 1) % self.__buffer_size

    def read(self):
        with self.__lock:
            i = self.__ptr_f.value
            value = self.__in[i]
            self.__ptr_f.value = (i + 1) % self.__buffer_size
            return value

    def seek(self):
        if self.can_read():
            return None
        else:
            return self.__in[self.__ptr_f.value]
