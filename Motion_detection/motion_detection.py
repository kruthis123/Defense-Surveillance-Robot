import serial
import time
import cv2

serialcomm = serial.Serial('COM5', 9600)
serialcomm.timeout = 1

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255,					cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE,		cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 2000:
            continue

        else:
            count += 1
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 				255, 255), 2)
            cv2.putText(frame1, 'Status: Movement', (20, 				40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow('video', frame1)
    if count != 0:
        i = "on"
    else:
        i = "off"
        
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        i = "done"
        break
    
    if i == "done":
        print('Finished')
        break
    
    serialcomm.write(i.encode())
    time.sleep(0.5)
    print(serialcomm.readline().decode('ascii'))

serialcomm.close()
cap.release()
cv2.destroyAllWindows()
