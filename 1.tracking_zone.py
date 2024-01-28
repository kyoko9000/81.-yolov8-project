import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video file
cap = cv2.VideoCapture("video1.mp4")

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    x1 = 400
    x2 = 1000
    y1 = 200
    y2 = 700
    frame_cut = frame[y1:y2, x1:x2]
    # draw zone detect
    start_point = (x1, y1)
    end_point = (x2, y2)
    color = (255, 255, 0)
    thickness = 2
    frame = cv2.rectangle(frame, start_point, end_point, color, thickness)

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame_cut, persist=True)
        for result in results:
            if result:
                boxes = result.boxes.numpy()  # Boxes object for bbox outputs
                for box in boxes:  # there could be more than one detection
                    print("class", box.cls)
                    x11 = int(box.xyxy[0][0]) + x1
                    y11 = int(box.xyxy[0][1]) + y1
                    x21 = int(box.xyxy[0][2]) + x1
                    y21 = int(box.xyxy[0][3]) + y1
                    # draw rectangle
                    frame = cv2.rectangle(frame, (x11, y11), (x21, y21), color, thickness)
                    # draw text
                    location = (x11, y11-5)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    if box.id:
                        text = "ID: " + str(int(box.id[0]))
                        image = cv2.putText(frame, text, location, font,
                                            fontScale, (0, 0, 255), thickness, cv2.LINE_AA)

        # Display the frame
        cv2.imshow("YOLOv8 Tracking", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()