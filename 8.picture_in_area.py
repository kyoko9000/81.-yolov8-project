import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
cap = cv2.VideoCapture("video1.mp4")
list_number = []
while cap.isOpened():
    # đọc từng khung hình trong video
    success, frame = cap.read()
    x1 = 600
    x2 = 850
    y1 = 230
    y2 = 500
    # frame_cut = frame[y1:y2, x1:x2]
    #vẽ vùng phát hiện
    start_point = (x1, y1)
    end_point = (x2, y2)
    color = (0, 255, 0)
    thickness = 2

    frame = cv2.rectangle(frame, start_point, end_point, color, thickness)

    frame1 = frame.copy()

    if success:
        # chạy YOLOv8 để theo dõi trên khung hình, duy trì các đối tượng qua các khung hình
        results = model.track(frame, persist=True, conf=0.4)
        """conf=0.4 là để khi dự đoán vật, nếu tỷ lệ nhỏ hơn 0.4 nó sẽ bỏ qua để tránh một vật dự đoán 2 class
        số này có thể thay đổi tùy vào khả năng dự đoán của model
        """
        #print("rs:",results)

        for result in results:
            if result:
                boxes = result.boxes.numpy()  # đối tượng boxes cho đầu ra hình hộp
                for box in boxes:  #có thể có nhiều hơn một phát hiện
                    # print("So doi tuong", len(boxes))
                    # print("class", box.cls)
                    x11 = int(box.xyxy[0][0])
                    y11 = int(box.xyxy[0][1])
                    x21 = int(box.xyxy[0][2])
                    y21 = int(box.xyxy[0][3])
                    frame = cv2.rectangle(frame, (x11, y11), (x21, y21), color, thickness)
                    # vẽ hình chữ nhật
                    if x11 > x1 and y11 > y1 + 50 and x21 < x2 and y21 < y2:
                        """
                        y1+50 là để xe nó ở giữa khung ảnh cho nó đẹp, số 50 đó có thể cao hay thấp
                        tùy vào kích cở ảnh để điều chỉnh cho phù hợp, bạn hãy test với video1.mp4 trong 
                        project số 81 của mình
                        """
                        # vẽ văn bản
                        location = (x11, y11 - 5)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 1
                        if box.id:
                            # print("box.id", box.id)
                            text = "xe:" + str(int(box.id[0]))
                            frame = cv2.putText(frame, text, location, font,
                                                fontScale, (0, 0, 255), thickness, cv2.LINE_AA)

                            # cắt và lưu hình ảnh kết quả
                            # roi = frame[y11:y21, x11:x21]
                            roi = frame1[y1: y2, x1: x2]
                            ID = int(box.id[0])
                            cv2.imwrite(f"hinh/xe vi pham{ID}.jpg", roi)
                            """
                            hinh/xe vi pham{ID}.jpg : hinh là folder tên hinh ở bên trong dự án cho nó gọn không bỏ
                            hình lung tung trong project nhìn nó sấu, nên phải tạo cái folder tên đó thì code mới chạy
                            được
                            """

        # Hiển thị khung hình.
        cv2.imshow("Theo dõi YOLOv8", frame)

        # thoát khỏi vòng lặp nếu đã đọc hết video
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Giải phóng đối tượng capture video và đóng cửa sổ hiển thị
cap.release()
cv2.destroyAllWindows()
