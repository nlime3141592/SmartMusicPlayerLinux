import cv2

classNames = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}

def id_class_name(class_id, classes):
    return classes.get(class_id, "Unknown")

def try_capture_person(path_jpg):
    """
    Detects and counts the number of people in the image at the specified path.

    Args:
        path_jpg (str): Path to the image file.

    Returns:
        int: The number of people detected in the image.
    """
    try:
        # Load the model
        model = cv2.dnn.readNetFromTensorflow(
            '/home/rpi5/OpencvDnn/models/frozen_inference_graph.pb',
            '/home/rpi5/OpencvDnn/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
        )

        # Read the image
        image = cv2.imread(path_jpg)
        if image is None:
            print("Error: Unable to load image. Please check the file path.")
            return 0
		
        image = cv2.resize(image, (640, 480))
        image_height, image_width, _ = image.shape

        # Preprocess the image and make predictions
        model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
        output = model.forward()

        person_count = 0

        for detection in output[0, 0, :, :]:
            confidence = detection[2]
            if confidence > 0.5:  # Filter detections with confidence > 0.5
                class_id = int(detection[1])
                class_name = id_class_name(class_id, classNames)
                if class_name == "person":  # Count only persons
                    person_count += 1
                    box_x = int(detection[3] * image_width)
                    box_y = int(detection[4] * image_height)
                    box_width = int(detection[5] * image_width)
                    box_height = int(detection[6] * image_height)
                    cv2.rectangle(image, (box_x, box_y), (box_width, box_height), (23, 230, 210), thickness=2)
                    cv2.putText(image, f"{class_name} ({confidence:.2f})", (box_x, box_y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), thickness=1)

        # Show the result
        cv2.imshow("Detected Persons", image)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()

        return person_count

    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    img_path = input("Enter the image path: ")
    person_count = try_capture_person(img_path)
    print(f"Number of people detected: {person_count}")
