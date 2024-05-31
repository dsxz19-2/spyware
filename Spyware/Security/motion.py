import cv2
import time
import datetime

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

detection = False
detection_stopped_time = None
timer_started = False
secondstorecordafternoface = 5

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("video.mp4", fourcc, 20, frame_size)
currtenttime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
out = cv2.VideoWriter(f"{currtenttime}.mp4", fourcc, 20, frame_size)
while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces)> 0:
        if detection:
            timer_started = False
        else:
            detection = True
            currtenttime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{currtenttime}.mp4", fourcc, 20, frame_size)
            print("Recording in progress")
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= secondstorecordafternoface:
                detection = False
                timer_started = False
                out.release()
                print("Recording stopped")
        else:
            timer_started = True
            detection_stopped_time = time.time()

    out.write(frame)

    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 225, 0), 3)


    cv2.imshow("cam", frame)
    if cv2.waitKey(1) == ord("q"):
        break

out.release()
cap.release()
cv2.destroyAllWindows()