def print_log(message, logger_name=None):
    if logger_name == None or logger_name == "":
        print(f" * {message}")
    else:
        print(f" * [{logger_name}] {message}")
