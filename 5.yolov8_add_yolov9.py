import cv2
from ultralytics import YOLO

# Load a model
# model = YOLO("yolov10n.pt")
model = YOLO("yolov9c.pt")
# model = YOLO("yolov9c-seg.pt")

# Use the model
results = model("video1.mp4", stream=True)  # predict on an image
for result in results:
    if result:
        # original image
        orig_img = result.orig_img
        # after predict image
        predict_img = result.plot()

        boxes = result.boxes.numpy()  # Boxes object for bbox outputs
        for box in boxes:  # there could be more than one detection
            print("class", box.cls)
            print("conf", box.conf)
            print("xyxy", box.xyxy)

        cv2.imshow("predict img", predict_img)
        cv2.waitKey(1)
