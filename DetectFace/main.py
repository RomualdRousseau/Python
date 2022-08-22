import sys
import cv2 as cv
import numpy as np

def main():

    face_cascade = cv.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml')

    #kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
    #fgbg = cv.createBackgroundSubtractorKNN()

    cap = cv.VideoCapture(0)
    if not (cap.isOpened()):
        print("Could not open video device")
        return

    cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

    image_area = 640 * 480  
    max_area = 0.95 * image_area
    min_area = 0.0005 * image_area    

    while(True):
        ret, frame = cap.read()
        
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.equalizeHist(gray)

        #mask = np.zeros(frame.shape[:2], np.uint8)
        #edges = cv.Canny(gray, 15, 150)
        #edges = cv.dilate(edges, None)
        #edges = cv.erode(edges, None)
        #_, edges = cv.threshold(edges, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)
        #contours = [(i, cv.contourArea(i)) 
        #        for i in cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)[-2]]
        #for contour in contours:
        #    if contour[1] > min_area and contour[1] < max_area:
        #        mask = cv.fillConvexPoly(mask, contour[0], (255))
        #mask = cv.dilate(mask, None, iterations=15)
        #mask = cv.erode(mask, None, iterations=15)
        #mask = cv.GaussianBlur(mask, (1, 1), 0)
        #gray = cv.bitwise_and(gray, gray, mask=mask)

        #fgmask = fgbg.apply(frame)
        #fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
        #frame = cv.bitwise_and(frame, frame, mask=fgmask)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #cv.imwrite("test.png", cv.resize(gray[y:y+h, x:x+h], (28, 28)))

        cv.imshow("preview", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    sys.exit(main())
