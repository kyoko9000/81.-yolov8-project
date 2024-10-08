import cv2
from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")

# Train the model
# train_results = model.train(
#     data="coco8.yaml",  # path to dataset YAML
#     epochs=1,  # number of training epochs
#     imgsz=640,  # training image size
#     device="cpu",  # device to run on, i.e. device=0 or device=0,1,2,3 or device=cpu
# )

# Evaluate model performance on the validation set
# metrics = model.val()

# Perform object detection on an image
results = model("video1.mp4", stream=True)
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
# results[0].show()

# Export the model to ONNX format
# path = model.export(format="onnx")  # return path to exported model