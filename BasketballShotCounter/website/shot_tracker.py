import cv2
from ultralytics import YOLO

def shot_counter(video_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened(): 
        return {"error": "Error opening video file"}

    shot_count = 0 
    make_count = 0 

    shot_cooldown = 0 #frames until new shot
    make_cooldown = 0 #frames until new make

    
    shot_frames = 0 

    yolo_model = YOLO("model_small.pt") #custom trained yolo model

    while(cap.isOpened()): 
          
        read, frame = cap.read() 

        if not read: 
            break 

        run_model = yolo_model(frame) 
        
        detections = run_model[0].boxes  

        
        shot_detected = False
        make_detected = False

        for detection in detections:
            detection_ID = detection.cls 
            detection_conf = detection.conf 

            if detection_ID == 0 and detection_conf > 0.8: #class_ID 0 is the class 'shot'
                shot_detected = True

            if detection_ID == 1 and detection_conf > 0.3: #class_ID 1 is the class 'make'
                make_detected = True


        if shot_detected:
            if shot_cooldown == 0: 
                shot_frames += 1 
                if shot_frames == 6: 
                    shot_frames = 0 
                    shot_count += 1 
                    shot_cooldown = 90  #next shot attempt after 90 frames
            else:
                shot_cooldown -= 1 

        else: 
            if shot_cooldown > 0:
                shot_cooldown -= 1 
            if shot_frames > 3: 
                shot_frames -= 1
            else: 
                shot_frames = 0

        if make_detected:
            if make_cooldown == 0: 
                make_count += 1 
                make_cooldown = 90 #next make after 90 frames
            else:
                make_cooldown -= 1

        else: 
            if make_cooldown > 0: 
                make_cooldown -= 1
   

        if shot_count > 0: #to stop it from dividing with 0
            FG = round(make_count/shot_count*100, 2) 
        else:
            FG = 0 
        
        if make_count > shot_count:
            return {"error": "Error processing video file"}
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

    cap.release()
    cv2.destroyAllWindows()
    
    return {
            "shot_count": shot_count,
            "make_count": make_count,
            "FG": FG
        }

