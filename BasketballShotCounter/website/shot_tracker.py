import cv2 
from ultralytics import YOLO 
 
def shot_counter(video_path): 
 
    cap = cv2.VideoCapture(video_path) 
 
    if not cap.isOpened(): #if video didnt open 
        return {"error": "Error opening video file"} 
 
    shot_count = 0 #counts number of shots attempted 
    make_count = 0 #counts number of shots made 
 
    shot_cooldown = 0 #frames until new shot 
    make_cooldown = 0 #frames until new make 
 
    #num of frames detected in a row 
    shot_frames = 0  
 
    yolo_model = YOLO("model_small.pt") #custom trained yolo model 
 
    while(cap.isOpened()): #loops through every frame 
           
        read, frame = cap.read()  
 
        if not read: #breaks loop if video is finished 
            break  
 
        run_model = yolo_model(frame) #runs the model on each frame 
         
        detections = run_model[0].boxes  #gets detected objects and their conf score 
 
        #variables that track whether a shot or make has been detected or not 
        shot_detected = False 
        make_detected = False 
 
        for detection in detections: 
            detection_ID = detection.cls #gets the ID of the detected object 
            detection_conf = detection.conf #gets the confidence score of the detected object 
 
            if detection_ID == 0 and detection_conf > 0.8: #class_ID 0 is the class 'shot' 
                shot_detected = True 
 
            if detection_ID == 1 and detection_conf > 0.3: #class_ID 1 is the class 'make' 
                make_detected = True 
 
 
        if shot_detected: 
            if shot_cooldown == 0: #checks if it is a new shot attempt 
                shot_frames += 1  
                if shot_frames == 6: #checks if shot has been detected in 6 frames in a row 
                    shot_frames = 0 #shot frames reset so next shot can be counted 
                    shot_count += 1 #a new shot has been attempted 
                    shot_cooldown = 90  #next shot attempt after 90 frames 
            else: 
                shot_cooldown -= 1  
 
        else: #if no shot is detected 
            if shot_cooldown > 0: 
                shot_cooldown -= 1  
            if shot_frames > 3: #if a shot was detected in more than 2 previous frames 
                shot_frames -= 1 
            else: #if a shot was detected less than 3 frames in a row 
                shot_frames = 0 
 
        if make_detected: 
            if make_cooldown == 0: #checks if it is a new make 
                make_count += 1 #a new shot has been made 
                make_cooldown = 90 #next make after 90 frames 
            else: 
                make_cooldown -= 1 
 
        else: #if no make is detected 
            if make_cooldown > 0: #less than 90 frames have passed since last make 
                make_cooldown -= 1 
    
 
        if shot_count > 0: #to stop it from dividing with 0 
            FG = round(make_count/shot_count*100, 2) #rounds it to 2 decimal places 
        else: 
            FG = 0  
         
        if make_count > shot_count: 
            return {"error": "Error processing video file"} 
         
        if cv2.waitKey(1) & 0xFF == ord('q'):  #puts 1 milliseconds between each frame 
            break 
 
    cap.release() 
    cv2.destroyAllWindows() 
     
    return { 
            "shot_count": shot_count, 
            "make_count": make_count, 
            "FG": FG 
        } 
 