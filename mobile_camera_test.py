import cv2

capture = cv2.VideoCapture('http://192.168.1.10:8080/video')
while(True):
   ret, frame = capture.read()
   frame = cv2.resize(src=frame,dsize=(1028,720))
   cv2.imshow('livestream', frame)
   if cv2.waitKey(1) == ord('q'):
      break
capture.release()
cv2.destroyAllWindows()