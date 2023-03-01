import cv2 as cv
import time


def main():
    camera_id="/dev/video1"
    cap = cv.VideoCapture(camera_id, cv.CAP_V4L2)
    cap.set(cv.CAP_PROP_FRAME_WIDTH,1080)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT,720)

    prev_time = 0
 
    new_time = 0
    
    if cap.isOpened():
        while(True):
            _, frame = cap.read()
            font = cv.FONT_HERSHEY_SIMPLEX
            new_time = time.time()
            fps = 1 / (new_time - prev_time)
            prev_time = new_time
            fps = int(fps)
            fps = str(fps)
            cv.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv.LINE_AA)
            cv.imshow("main Frame", frame)
            if cv.waitKey(1) & 0xFF == 27 or cv.waitKey(30) & 0xFF == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()


main()
