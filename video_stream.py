import cv2

cap = cv2.VideoCapture(0)  # 0 for default camera, or 1, 2, etc. for additional cameras

while cap.isOpened():
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)# read a frame from the video stream

    cv2.imshow('Live Video Stream', frame)  # show the frame in a window named "Live Video Stream"

    if cv2.waitKey(1) == ord('q'):  # press 'q' to exit the program
        break

cap.release()  # release the video capture object
cv2.destroyAllWindows()  # destroy all windows
