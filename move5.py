import cv2
# import robot_arm_module  # Assume a module for robot arm control
# import ultrasonic_sensor_module  # Assume a module for ultrasonic sensor
# import arduino_module  # Assume a module for Arduino communication
from model_predict import Detect
from qrcode import QRCode

# sb bin is 0 in QRcode analysis
# nb bin is 1 in QRcode analysis
# bottle bin is 2 in QR analysis
rubbish = ["sb", "nb", "bottle", "apple"]


#initialize
def callback(img,infos):
    print(infos)
detect = Detect()
qrcode = QRCode()



def find_rubbish():
    # Use OpenCV to capture video feed
    video_capture = cv2.VideoCapture(1) #the index of the webcam

    rubbish_detected, centre_vertical_line = False, False

    while True:
        '''
        arduino_module.rotation()
        '''

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

    '''
    arduino_module.stop()
    '''
    print("rubbish is on the center ahead")
    print("rubbish type:", rubbish[rubbish_type])
    # Release the video capture object
    video_capture.release()

    return rubbish_type


def detect_rubbish(frame):
    # Implement rubbish detection logic using OpenCV
    # Return a boolean indicating if rubbish is detected and its position on the centre vertical line
    # Example: return True, centre_vertical_line, rubbish_index

    list = detect.detect_img(frame, callback)
    if list == []:
        return False, False, 0
    else:
        first_rubbish = list[0]

    for i in range(len(rubbish)):
        if first_rubbish[0] == rubbish[i]:
            rubbish_index = i
            break

    threshold = 0.1
    if first_rubbish[2] < 0.5 + threshold and first_rubbish[2] > 0.5 - threshold:
        is_center = True
    else:
        is_center = False

    return True, is_center, rubbish_index


def pick_up_rubbish():
    # Instruct the robot to go forward using ultrasonic sensor to sense the distance
    threshold_distance = 10

    '''
        while ultrasonic_sensor_module.get_distance() > threshold_distance:
        arduino_module.move_forward()
    '''

    print("in front of rubbish")

    '''
    # Stop the robot
    arduino_module.stop()

    # Pick up the rubbish using the robot arm
    robot_arm_module.pick_up()
    '''

    print('successfully collect rubbish')



def find_bin(index):
    # Use OpenCV to capture video feed for QR code scanning
    video_capture = cv2.VideoCapture(1)

    while True:
        '''
        arduino_module.rotation()
        '''
        print("find bin")
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
    '''
    arduino_module.stop()
    '''
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
        threshold = 0.1
        for bin in list:
                if bin[0] == rubbish_index and bin[1] < 0.5 + threshold and bin[1] > 0.5 - threshold:
                    return True, True
        return False, False



def go_to_bin():
    # Instruct the robot to go forward using ultrasonic sensor to sense the distance
    threshold_distance = 10
    '''
        while ultrasonic_sensor_module.get_distance() > threshold_distance:
        arduino_module.move_forward()

    # Stop the robot
    arduino_module.stop()

    # Pick up the rubbish using the robot arm
    robot_arm_module.loose_arm()
    '''
    print("finished the process")



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

