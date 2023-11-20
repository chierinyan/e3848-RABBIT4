import cv2
# import robot_arm_module  # Assume a module for robot arm control
# import ultrasonic_sensor_module  # Assume a module for ultrasonic sensor
# import arduino_module  # Assume a module for Arduino communication
from model_predict import Detect
from qrcode import QRCode
from base import base_ctl
from time import sleep

rubbish = [["carton"], ["can"], ["bottle"], ["noresult"]]
no_result_label = 3
rotation_speed = 30
rotation_time = 2
linear_speed = 30
linear_time = 3
#if rubbish is too close to the bin, abandon the result.
distance_percentage = 0.2
center_line_threshold = 0.05
ultrasonic_threshold_distance = 10

#initialize
def callback(img,infos):
    print(infos)
detect = Detect()
qrcode = QRCode()

# rank the closest rubbish to the middle line to the top priority 
def rank(element):
    return abs(0.5-element[2])

def find_rubbish():
    # Use OpenCV to capture video feed
    video_capture = cv2.VideoCapture(0) #the index of the webcam

    rubbish_detected, centre_vertical_line = False, False

    while True:
        # there is pause during the rotation
        base_ctl(0,0,rotation_speed,0)
        sleep(rotation_time)
        base_ctl(0,0,0,0)
        

        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if ret is False:
            print("error in camera")
            break

        # Implement rubbish detection logic using OpenCV
        rubbish_detected, centre_vertical_line, rubbish_type = detect_rubbish(frame)

        # If rubbish is found on the centre vertical line, break from the loop
        if rubbish_detected and centre_vertical_line:
            break

    base_ctl(0,0,0,0)
    print("rubbish is on the center ahead")
    print("rubbish type:", rubbish[rubbish_type])
    # Release the video capture object
    video_capture.release()

    return rubbish_type


def detect_rubbish(frame):
    # Implement rubbish detection logic using OpenCV
    # Return a boolean indicating if rubbish is detected and its position on the centre vertical line
    # Example: return True, centre_vertical_line, rubbish_index

    # find the nearest rubbish in the center line
    list = detect.detect_img(frame, callback)
    binlist = qrcode.detect(frame)
    if list == []:
        return False, False, 0
    else:
        list.sort(key= rank)
        first_rubbish = list[0]


    for bin in binlist:
        if abs(first_rubbish[2] - bin[1]) < distance_percentage:
            return False, False, 0

    #find the correct bin to dispose the rubbish
    rubbish_index = no_result_label
    for i in range(len(rubbish)):
        for j in rubbish[i]:
            if first_rubbish[0] == j:
                rubbish_index = i
                break

    # judge if the rubbish is on the list
    if rubbish_index == no_result_label:
        return False, False, 0
    
    # judge if it is in the centerline
    if first_rubbish[2] < 0.5 + center_line_threshold and first_rubbish[2] > 0.5 - center_line_threshold:
        is_center = True
    else:
        is_center = False

    return True, is_center, rubbish_index


def pick_up_rubbish():
    # Instruct the robot to go forward using ultrasonic sensor to sense the distance
    
    base_ctl(linear_speed,0,0,0)
    sleep(linear_time)
    base_ctl(0,0,0,1)

    '''
    while base_ctl(linear_speed,0,0,0) > ultrasonic_threshold_distance:
        continue
    base_ctl(0,0,0,0)
    '''

    base_ctl(0, 0, 0, 1)
    print("in front of rubbish")
    print('successfully collect rubbish')



def find_bin(index):
    # Use OpenCV to capture video feed for QR code scanning
    video_capture = cv2.VideoCapture(0)
    previous_status = ""

    while True:
        # rotation with pause
        base_ctl(0, 0, rotation_speed, 1)
        sleep(rotation_time)
        base_ctl(0, 0, 0, 1)

        #testing
        if previous_status != "find bin":
            print("find bin")
        previous_status = "find bin"

        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if ret is False:
            print("error in camera")
            break

        # Implement QR code scanning logic
        qr_code_found, central_vertical_line = detect_qrcode(frame, index)

        # If QR code is found, break from the loop
        if qr_code_found and central_vertical_line:
            break
    base_ctl(0,0,0,1)
    print("successfully find the target bin")
    # Release the video capture object
    video_capture.release()

def detect_qrcode(frame, rubbish_index):
    # Implement QR detection logic using OpenCV
    # Return a boolean indicating if rubbish is detected and its position on the centre vertical line
    # Example: return True, True (QR code detection, center vertical line)
    list = qrcode.detect(frame)
    if list == []:
        return False, False
    else:
        for bin in list:
                if bin[0] == rubbish_index and bin[1] < 0.5 + center_line_threshold and bin[1] > 0.5 - center_line_threshold:
                    return True, True
        return False, False



def go_to_bin():
    # Instruct the robot to go forward using ultrasonic sensor to sense the distance

    
    base_ctl(linear_speed,0,0,1)
    sleep(linear_time)
    base_ctl(0,0,0,0)
    

    '''
    while base_ctl(30,0,0,1) > ultrasonic_threshold_distance:
        continue
    base_ctl(0,0,0,1)
    base_ctl(0,0,0,0)
    '''
    print("finished the process")


def go_to_origin():
    base_ctl(-1*linear_speed, 0, 0, 0)
    sleep(linear_time)
    base_ctl(0, 0, 0, 0)

if __name__ == "__main__":
    # Main program flow
    while True:
        # Step 1: Find rubbish
        index = find_rubbish()

        # Step 2: Pick up rubbish
        pick_up_rubbish()

        # Step 3: Find bin
        find_bin(index)

        # Step 4: Go to the bin
        go_to_bin()

        # Step 5: Go to origin
        go_to_origin()

        