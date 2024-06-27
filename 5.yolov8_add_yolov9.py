import cv2
from ultralytics import YOLO

# Load a model
# model = YOLO("yolov8n.pt")
# model = YOLO("yolov9t.pt")
# model = YOLO("yolov9c-seg.pt")
model = YOLO("yolov10n.pt")


# Use the model
results = model("video1.mp4", stream=True)  # predict on an image
for result in results:
    # original image
    orig_img = result.orig_img
    # after predict image
    predict_img = result.plot()
    if result:
        boxes = result.boxes.numpy()  # Boxes object for bbox outputs
        for box in boxes:  # there could be more than one detection
            print("class", box.cls)
            print("conf", box.conf)
            print("xyxy", box.xyxy)

    # show original image
    # cv2.imshow("predict img", orig_img)

    # show image after predict
    cv2.imshow("predict img", predict_img)
    cv2.waitKey(1)
