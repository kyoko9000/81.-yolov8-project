from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n-obb.pt')  # load an official model

# Predict with the model
results = model('plane.jpg', save=True, project='81. yolov8 project', name='OBB')
for result in results:
    print(result.obb.xyxyxyxy)

path = model.export(format="onnx")