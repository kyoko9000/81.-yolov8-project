from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load an official model

# Predict with the model
results = model('bus.jpg', save=True, project='81. yolov8 project', name='OBB')