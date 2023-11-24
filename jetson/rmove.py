import cv2

#from model_predict import Detect
#from qrcode import QRCode
from client import Client
from base import Base
from time import sleep

rubbish = [["bottle"], ["general waste"], ["empty"], ["carton"],["can"]]
camera_index = 0

#before recognize rubbish in list, we assume the item label is no_result_label
no_result_label = 2
rotation_speed = 30
rotation_time = 2
linear_speed = 30
linear_time = 4
#if rubbish is too close to the bin, abandon the result.
distance_percentage = 0.2
center_line_threshold = 0.1
ultrasonic_threshold_distance = 2
height_threshold = 0.7
hostaddr = "http://10.68.43.144:4000"

#initialize
    
#detect = Detect()
#qrcode = QRCode()
client = Client(host= hostaddr)

base = Base()


# rank the closest rubbish to the middle line to the top priority 
def rubbish_rank(element):
    return abs(0.5-element[2])

def bin_rank(element):
    return abs(0.5-element[1])

def find_rubbish():
    # Use OpenCV to capture video feed
    video_capture = cv2.VideoCapture(camera_index) 

    rubbish_detected, centre_vertical_line = False, False

    while True:
        # there is pause during the rotation for static recognition
        base.base_ctl(0,0,rotation_speed,0)
        sleep(rotation_time)
        base.base_ctl(0,0,0,0)
        

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

    base.base_ctl(0,0,0,0)
    print("rubbish is on the center ahead")
    print("rubbish type:", rubbish[rubbish_type])
    
    video_capture.release()
    return rubbish_type


def detect_rubbish(frame):
    # Implement rubbish detection logic using OpenCV
    # Return a boolean indicating if rubbish is detected and its position on the centre vertical line
    # Example: return True, centre_vertical_line, rubbish_index

    # find the nearest rubbish in the center line
    # list = [["bottle"(pattern),0.65(probability),0.2(x),0.5(y) ]] (center point of the item)
    # binlist = [[label_number,x,y]]
    #list = detect.detect_img(frame, callback)
    #binlist = qrcode.detect(frame)
    total = client.detect(frame)
    if not total:
        return False, False, no_result_label
    list, binlist = total
    print("list:", list)
    print("binlist: ", binlist)
    if list == []:
        return False, False, no_result_label
    else:
        list.sort(key= rubbish_rank)
        first_rubbish = list[0]


    for bin in binlist:
        if abs(first_rubbish[2] - bin[1]) < distance_percentage:
            return False, False, no_result_label

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
    
    while base.base_ctl(linear_speed,0,0,0) > ultrasonic_threshold_distance:
        print("approach the rubbish")
    base.base_ctl(0,0,0,0)
    print("in front of rubbish")
    base.base_ctl(0, 0, 0, 1)
    print('successfully collect rubbish')



def find_bin(index):
    # Use OpenCV to capture video feed for QR code scanning
    video_capture = cv2.VideoCapture(camera_index) 
    previous_status = ""

    while True:
        # rotation with pause
        base.base_ctl(0, 0, rotation_speed, 1)
        sleep(rotation_time)
        base.base_ctl(0, 0, 0, 1)

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
    print("successfully find the target bin")
    base.base_ctl(0,0,0,1)
    video_capture.release()
    

def detect_qrcode(frame, rubbish_index):
    # Implement QR detection logic using OpenCV
    # Return a boolean indicating if rubbish is detected and its position on the centre vertical line
    # Example: return True, True (QR code detection, center vertical line)
    # list = qrcode.detect(frame)
    total = client.detect(frame)
    if not total or len(total) == 1:
        return False, False
    list = total[1]
    print("binlist: ", list)
    if not list:
        return False, False
    else:
        list.sort(key=bin_rank)
        if list[0][0] == rubbish_index and list[0][1] < 0.5 + center_line_threshold and list[0][1] > 0.5 - center_line_threshold:
             return True, True
        elif list[0][0] > rubbish_index:
            base.base_ctl(0,-1*linear_speed,0,1)
            sleep(0.5*linear_time*(list[0][0]-rubbish_index))
            base.base_ctl(0,0,0,1)
        elif list[0][0] < rubbish_index:
            base.base_ctl(0, linear_speed, 0, 1)
            sleep(0.5*linear_time*(rubbish_index-list[0][0]))
            base.base_ctl(0, 0, 0, 1)
        return False, False

#if the center of QR code is too hight in the picture, it proves arrives at the QRcode position
def qrcode_distance(rubbish_index):
    video_capture = cv2.VideoCapture(camera_index) 
    ret, frame = video_capture.read()
    total = client.detect(frame)
    video_capture.release()
    if not total or len(total) == 1:
        return True
    list = total[1]
    print("binlist: ", list)
    if not list:
        return True
    else:
        list.sort(key=bin_rank)
        if list[0][0] == rubbish_index and list[0][2] > height_threshold:
            print("height: ",list[0][2])
            return False
        elif list[0][0] == rubbish_index and list[0][1] < 0.5 - center_line_threshold:
            base.base_ctl(0, linear_speed, 0, 1)
            sleep(0.5 * linear_time)
            base.base_ctl(0, 0, 0, 1)
        elif list[0][0] == rubbish_index and list[0][1] > 0.5 + center_line_threshold:
            base.base_ctl(0, -1 * linear_speed, 0, 1)
            sleep(0.5 * linear_time)
            base.base_ctl(0, 0, 0, 1)
        print("height: ", list[0][2])
        return True

def go_to_bin(rubbish_index):
    # Instruct the robot to go forward using ultrasonic sensor to sense the distance

    while qrcode_distance(rubbish_index):
        base.base_ctl(linear_speed,0,0,1)
        print("haven't arrived at bin yet")
    base.base_ctl(0,0,0,1)
    print("arrive at the bin")
    sleep(2)
    base.base_ctl(0,0,0,0)
    print("finished the process")


# go backward
def go_to_origin():
    base.base_ctl(-1*linear_speed, 0, 0, 0)
    sleep(linear_time)
    base.base_ctl(0, 0, 0, 0)

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
        go_to_bin(index)

        # Step 5: Go to origin
        go_to_origin()


    

        