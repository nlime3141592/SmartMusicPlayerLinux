import logmodule as logger
import music

__logger_name = "MusicService"

# TODO: Move this code to music service handling python file.
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
        self.__cntx.shmem.write("music;next;")
    elif service_type == "prev":
        self.__cntx.shmem.write("music;prev;")
    elif service_type == "change_shuffle":
        self.__cntx.shmem.write("music;change_shuffle;")
    elif service_type == "change_loop":
        self.__cntx.shmem.write("music;change_loop;")
    elif service_type == "toggle_like":
        self.__cntx.shmem.write("music;toggle_like;")
    elif service_type == "volup":
        self.__cntx.shmem.write("music;volup;")
    elif service_type == "voldown":
        self.__cntx.shmem.write("music;voldown;")
    elif service_type == "volmute":
        self.__cntx.shmem.write("music;volmute;")
    elif service_type == "toggle_playing":
        self.__cntx.shmem.write("music;toggle_playing;")
    else:
        logger.print_log("Invalid service requested, rejects.", logger_name=self.__logger_name)

def __update_music_select(service_tokenizer):
    music_id = int(service_tokenizer.read())
    music.play(f"./music/data/{music_id}.mp3")
    pass

def __update_music_delete(service_tokenizer):
    music_id = int(service_tokenizer.read())
    pass

def update(service_tokenizer):
    service_type = tokens.read()

    if service_type == "control":
        __update_music_control(service_tokenizer)
    elif service_type == "select":
        __update_music_select(service_tokenizer)
    elif service_type == "delete":
        __update_music_delete(service_tokenizer)
    else:
        logger.print_log("Invalid service requested, rejects.", logger_name=self.__logger_name)

# NOTE: The entry point when testing this file.
if __name__ == "__main__":
    import service_tokenizer as tok
    tokenizer = tok.ServiceTokenizer("4;")
    __update_music_select(tokenizer)

    music.set_mode_loop(music.c_MODE_LOOP_LIST)
    music.set_volume(2)

    while True:
        update_always()