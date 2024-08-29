import cv2
import time
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2
import Adafruit_MCP4725


##############
# Face Time HD: 720 x 1280
# Freenove 8MP: 3264 x 2448 
#frame_size = (1280,720) #HD
frame_size = (960,540) #qHD

# Create a DAC instance.
dac = Adafruit_MCP4725.MCP4725(address = 0x60, busnum = 1)

#Rectangle/Detection Frame
start_point = (100,100)
end_point = (frame_size[0]-100,frame_size[1]-100)

mp_hands = mp.solutions.hands

#processing_time =[]
center = np.zeros(2)
output = 0

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def rescaleDetected(x):
    #return np.round(7.875*x-787.5).astype(int) #(HD 1280x720)
    return np.round(12.044*x-1204.412).astype(int) #(qHD 960x540)

#Cam setup/Rescale to qHD
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": frame_size}, lores={"size": (640, 480)}, display="main")
picam2.configure(camera_config)
picam2.start()


#image = picam2.capture_array()
#print(image.shape)


with mp_hands.Hands(
    model_complexity=0,
    max_num_hands = 1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

  while True:
    #start_time = time.time()
    image = picam2.capture_array()
    image.flags.writeable = False
    
    #Mediapipe processing
    results = hands.process(image)
    
    #Get coordinates
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
          d_coor = np.array((hand_landmarks.landmark[4].x , hand_landmarks.landmark[4].y)) #thumb landmark #4
          center = np.floor(d_coor*frame_size).astype(int)
    
    #check if coor inside bounds
    # if (100<center[0]<1180) & (100<center[1]<620):
    #     output = 720 - center[1]
    if (100<center[0]<860) & (100<center[1]<440):
        output = 540 - center[1]
    
    #Draw rectangle 
    image = cv2.rectangle(image, start_point, end_point, (255, 0,0), 2 )
    
    #Draw circle
    if results.multi_hand_landmarks:
        image = cv2.circle(image, center, radius=5, color=(255, 0, 0), thickness=5)
   
    #flip the image horizontally for a selfie-view display.
    image = cv2.flip(image, 1)

    #set DAC output voltage
    output_dac = rescaleDetected(output)
    dac.set_voltage(output_dac)

    #put text
    cv2.putText(image, str(np.round(5 * output_dac/4095, decimals = 2)) + 'V', (400,70), fontFace = 3,fontScale = 2, color = (255,0,0), thickness = 5 )


    cv2.imshow('CV Tracker', image)
    #stop_time = time.time()
    #processing_time.append(stop_time-start_time)
    
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
      #cv2.imwrite("output.png", image)
      break

    #np.savetxt("Processing_time.csv", processing_time, delimiter=',')

