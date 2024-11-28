class ServiceTokenizer:
    def __init__(self, service_string, delimiter=";"):
        self.__service_string = service_string
        self.__delimiter = delimiter

    def read(self):
        idx_delim = self.__service_string.find(self.__delimiter)

        if idx_delim != -1:
            read_string = self.__service_string[0:idx_delim]
            self.__service_string = self.__service_string[idx_delim + 1:]
            return read_string
        elif len(self.__service_string) != 0:
            last_string = self.__service_string
            self.__service_string = ""
            return last_string
        else:
            return None