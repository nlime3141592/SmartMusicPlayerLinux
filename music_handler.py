import logmodule as logger
import music

__logger_name = "MusicService"

def init():
    pass

def final():
    pass

def update_always():
    if music.try_catch_end_event() == False:
        return

    mode_loop = music.get_mode_loop()
    mode_shuffle = music.get_mode_shuffle()

    if mode_loop == music.c_MODE_LOOP_MUSIC:
        music.play_begin()
    else:
        # TODO: get next music here.
        pass

def __update_music_control(service_tokenizer):
    service_type = service_tokenizer.read()

    if service_type == "next":
        logger.print_log("next executed.", logger_name=__logger_name)
    elif service_type == "prev":
        logger.print_log("prev executed.", logger_name=__logger_name)
    elif service_type == "change_shuffle":
        logger.print_log("change_shuffle executed.", logger_name=__logger_name)
    elif service_type == "change_loop":
        logger.print_log("change_loop executed.", logger_name=__logger_name)
    elif service_type == "toggle_like":
        logger.print_log("toggle_like executed.", logger_name=__logger_name)
    elif service_type == "volup":
        logger.print_log("volup executed.", logger_name=__logger_name)
    elif service_type == "voldown":
        logger.print_log("voldown executed.", logger_name=__logger_name)
    elif service_type == "volmute":
        logger.print_log("volmute executed.", logger_name=__logger_name)
    elif service_type == "toggle_playing":
        logger.print_log("toggle_playing executed.", logger_name=__logger_name)
    else:
        logger.print_log("Invalid service requested, rejects.", logger_name=__logger_name)

def __update_music_select(service_tokenizer):
    music_id = int(service_tokenizer.read())
    music.play(f"./music/data/{music_id}.mp3")
    pass

def __update_music_delete(service_tokenizer):
    music_id = int(service_tokenizer.read())
    pass

def update(service_tokenizer):
    service_type = service_tokenizer.read()

    if service_type == "control":
        __update_music_control(service_tokenizer)
    elif service_type == "select":
        __update_music_select(service_tokenizer)
    elif service_type == "delete":
        __update_music_delete(service_tokenizer)
    else:
        logger.print_log("Invalid service requested, rejects.", logger_name=__logger_name)

# NOTE: The entry point when testing this file.
if __name__ == "__main__":
    import service_tokenizer as tok
    tokenizer = tok.ServiceTokenizer("4;")
    __update_music_select(tokenizer)

    music.set_mode_loop(music.c_MODE_LOOP_MUSIC)
    music.set_volume(2)

    while True:
        update_always()
