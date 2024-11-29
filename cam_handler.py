import cv2
import cam
import proc

__logger_name = "CamService"

def init():
    cam.start_cam()

def update_always():
    cam.update_always()

def __update_cam_live(service_tokenizer):
    service_type = service_tokenizer.read()

    if service_type == "image":
        read_complete, frame = cam.generate_frame()

        if read_complete:
            proc.proc_ctx.shmem.write("1")
            proc.proc_ctx.shmem.write(frame)
        else:
            proc.proc_ctx.shmem.write("0")
    else:
        logger.print_log("Invalid service requested, rejects.", logger_name=__logger_name)

def update(service_tokenizer):
    service_type = service_tokenizer.read()

    if service_type == "live":
        __update_cam_live(service_tokenizer)
    else:
        logger.print_log("Invalid service requested, rejects.", logger_name=__logger_name)

def final():
    pass

# NOTE: The entry point when testing this file.
if __name__ == "__main__":
    pass