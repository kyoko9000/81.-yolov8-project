from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
# model = YOLO("yolov9t.pt")  # load a pretrained model (recommended for training)
# model = YOLO("yolov10n.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="coco8.yaml", epochs=1)  # train the model
# model.train(data="cocosample.yaml", epochs=1)  # train the model
# model.train(data="cocosample.yaml", epochs=1, batch=2, imgsz=640, device='0', workers=2)