import cv2
import cam
import proc

import logmodule as logger

__logger_name = "CamService"

def init():
    cam.start_cam()

def update_always():
    cam.update_always()

def update(service_tokenizer):
    service_type = service_tokenizer.read()

    if service_type == "live":
        pass
    else:
        logger.print_log("Invalid service requested, rejects.", logger_name=__logger_name)

def final():
    pass

# NOTE: The entry point when testing this file.
if __name__ == "__main__":
    pass