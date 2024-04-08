import cv2
from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")

# Use the model
results = model("video1.mp4", stream=True)  # predict on an image
for result in results:
    # original image
    orig_img = result.orig_img
    # after predict image
    predict_img = result.plot()
    frame = orig_img
    if result:
        boxes = result.boxes.numpy()  # Boxes object for bbox outputs
        all_box = boxes.xyxy  # total list
        y1_box = boxes.xyxy[:, 1]  # list of y1
        print("all_box", all_box)
        print("x1_box", y1_box)

        # Chuyển đổi tất cả các phần tử trong new_list thành int
        int_y1_box = [int(x) for x in y1_box]
        # In danh sách mới với các số dạng int
        print("x1 int list:", int_y1_box)

        y1_max = max(int_y1_box)  # find y1 max
        print("y1_max", y1_max)
        y1_max_pos = int_y1_box.index(y1_max)  # find y1 max position
        print("x1_max_pos", int_y1_box.index(y1_max))

        coordinates_we_need = all_box[y1_max_pos]  # this is coordinates near camera
        print("coordinates near camera", coordinates_we_need)

        x1 = int(coordinates_we_need[0])
        y1 = int(coordinates_we_need[1])
        x2 = int(coordinates_we_need[2])
        y2 = int(coordinates_we_need[3])
        # draw rectangle
        color = (255, 255, 0)
        thickness = 2
        frame = cv2.rectangle(orig_img, (x1, y1), (x2, y2), color, thickness)

    cv2.imshow("predict img", frame)
    cv2.waitKey(1)