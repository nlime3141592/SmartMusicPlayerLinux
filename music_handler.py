import logmodule as logger
import music

__logger_name = "MusicService"

def update(tokens):
    if tokens[0] == None or tokens[0] == "":
        logger.print_log("Empty service type.", logger_name=__logger_name)
    elif tokens[0] == "play":
        is_playing = music.toggle_playing()
        logger.print_log(f"music.is_playing == {is_playing}", logger_name=__logger_name)
    else:
        logger.print_log("Invalid service type", logger_name=__logger_name)
