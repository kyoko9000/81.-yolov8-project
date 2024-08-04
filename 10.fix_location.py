# from ultralytics import YOLO
#
# # Load a model
# model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
#
# # Use the model
# model.train(data="coco8.yaml", epochs=1)

from ultralytics import settings

# Update a setting
# settings.update({"datasets_dir": "D:\\2.Python_projects\\81.-yolov8-project\\datasets"})

# # Reset settings to default values
# settings.reset()

# View all settings
print(settings)
