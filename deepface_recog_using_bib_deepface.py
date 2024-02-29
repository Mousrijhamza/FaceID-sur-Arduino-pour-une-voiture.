import threading
import cv2
from deepface import DeepFace

# to define a video capture we wanted to
# find a camera we want to set the uh the
# property (W, and H) go go through
# this endless loop until we terminate it
# that just gets the frame and does
# something with it so what

#define the camera object 
cap = cv2.VideoCapture(0, ) #indicate which camera you want to use, so we picks the 1st camera
#set the prepotion and de,emsion
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

face_match = False
counter = 0
reference_img = cv2.imread("image.jpg") #loading the reference image

# keep track of because of course we don't
# want to uh to verify the faces we don't
# want to look for a match every single
# frame we want to do that once in a while
# because if you do it all the time first
# of all matching the faces determining if
# there is a match or not using this
# neural network behind the scenes we'll
# take more than just half a second so
# we're going to have to wait for the
# response and we don't want to start a
# new response with every single frame
# especially if you have 30 to 60 frames a
# second you want to do it once in a while
# and we're going to do that by using a
# counter variable


#fonction that check if the current image and the reference image are the face same one them
def check_face(frame):
    # face match Boolean that we Define
    # up here will be changed by that function
    # depending on whether there is a match or
    # not
    # ML DL
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False



while True:
    ret, frame = cap.read()  #get the frame from the camera copy
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 6)
    for x,y,w,h in face:
        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 3)

    if ret:
        if counter % 3 == 0:
            try: #start a threat to compare the frame from camera with the image reference
                threading.Thread(target = check_face, args =(frame.copy(),  )).start()   #check the face is it match
            except ValueError:
                #  if it doesn't recognize a face
                # in an image it tells you value error and
                # you're not going to be able to do
                # anything 
                pass
            
        counter += 1
        if face_match:
            #right in green
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 255, 0), 3)
        
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"): #every process should tape a key
        break

cv2.destroyAllWindows()