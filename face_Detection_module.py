import mediapipe as mp
import cv2
import time

class FaceDetector():

    def __init__(self, minDetection_conf = 0.7):
        self.minDetection_conf = minDetection_conf
        self.mpfacedetection = mp.solutions.face_detection
        self.mpdraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpfacedetection.FaceDetection(self.minDetection_conf)
   
    def findFaces (self, img, draw = True):
        imgRGB = cv2.cvtColor (img, cv2.COLOR_BGR2RGB)
        self.result  =  self.faceDetection.process (imgRGB)
        bounding_boxs = []
    
        if self.result.detections:
            for id,detection in enumerate (self.result.detections):
                bounding_box_location = detection.location_data.relative_bounding_box #bboxc
                image_height , image_width, i_c = img.shape
                bounding_box =int (bounding_box_location.xmin * image_width)  , int (bounding_box_location.ymin * image_height), int(bounding_box_location.width * image_width)  , int (bounding_box_location.height * image_height) 
               
                bounding_boxs.append([id,bounding_box,detection.score])
                img =  self.drawfine(img,bounding_box)
             #   cv2.putText(img, f' {int (detection.score [0] * 100 )} % ', (bounding_box[0] -15 ,bounding_box[1]-10  ),cv2.FONT_HERSHEY_PLAIN, 2,(0,255,0,2),2)
        return img,bounding_boxs   
    def drawfine (self, img, bounding_box,l = 30,t =5, rt = 1):
        x,y,w,h = bounding_box
        x1,y1 = x+w,y+h

        cv2.rectangle (img ,bounding_box, (0, 0,255),2,rt)
        #Top Left
        cv2.line (img , (x,y), (x+l,y), (0,0,255),t ) 
        cv2.line (img , (x,y), (x,y+l), (0,0,255),t )


        #Top right
        cv2.line (img , (x1,y), (x1-l,y), (0,0,255),t ) 
        cv2.line (img , (x1,y), (x1,y+l), (0,0,255),t ) 
       

        #Botom Left
        cv2.line (img , (x,y1), (x+l,y1), (0,0,255),t ) 
        cv2.line (img , (x,y1), (x,y1-l), (0,0,255),t )


        #Botom right
        cv2.line (img , (x1,y1), (x1-l,y1), (0,0,255),t ) 
        cv2.line (img , (x1,y1), (x1,y1-l), (0,0,255),t ) 
      
        return img

def main():
    cap = cv2.VideoCapture(0)
    previous_time = 0
    detector = FaceDetector()

    while True:
        success, img = cap.read()
        img,bounding_boxs = detector.findFaces(img)
       # print (bboxs)
        imgRGB = cv2.cvtColor (img, cv2.COLOR_BGR2RGB)
      
        current_time = time.time()
        frames_Per_Seconds = 1/(current_time - previous_time)
        previous_time  = current_time
        cv2.putText(img, f' FPS: {int (frames_Per_Seconds)}', (0,50),cv2.FONT_HERSHEY_PLAIN, 3,(0,255,0,2),2)
       
        cv2.imshow("img", img,)
        if cv2.waitKey(20) & 0xFF == 27:
              break
if __name__  =="__main__":

    
    main()
