from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n-obb.pt')  # load an official model

# Predict with the model
results = model('plane.jpg', save=True, project='OBB')
for result in results:
    print(result.obb.xyxyxyxy)