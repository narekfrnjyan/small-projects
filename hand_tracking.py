import time
import cv2
from cvzone.HandTrackingModule import HandDetector
from djitellopy import Tello
left_right_velocity = 0
forward_backward_velocity = 0
up_down_velocity = 0
yaw_velocity = 0
detector = HandDetector(detectionCon = 0.8,maxHands = 2)
me = Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()
height = 580
width =600
me.takeoff()
me.move('up', 50)
min_bbox_width = 90
max_bbox_width = 120
min_bbox_height =140
max_bbox_height = 180
min_x_coordinate = 90
max_x_coordinate = 400
min_y_coordinate = 40
max_y_coordinate = 130
while True:
    frame_read = me.get_frame_read()
    frame = frame_read.frame
    hands, img = detector.findHands(frame)

    if hands and hands[0]['bbox'][2] < min_bbox_width and hands[0]['bbox'][3] < min_bbox_height \
            and (hands[0]['type'] == 'Right' ):
        forward_backward_velocity = 40

    elif hands and hands[0]['bbox'][2] > max_bbox_width and hands[0]['bbox'][3]>max_bbox_height \
            and (hands[0]['type'] == 'Right'):
        forward_backward_velocity = -40

    else:
        forward_backward_velocity = 0


    if  hands and hands[0]['bbox'][0] < min_x_coordinate \
            and (hands[0]['type'] == 'Right' ):
        left_right_velocity = -40
        print('lrft')
    elif hands and hands[0]['bbox'][0] > max_x_coordinate \
            and (hands[0]['type'] == 'Right' ):
        left_right_velocity = 40
        print('Right')
    else:
        left_right_velocity = 0


    if  hands and hands[0]['bbox'][1] < min_y_coordinate \
            and (hands[0]['type'] == 'Right'):
        up_down_velocity = 40

    elif hands and hands[0]['bbox'][1] > max_y_coordinate \
            and (hands[0]['type'] == 'Right' ):
        up_down_velocity = -40

    else:
        up_down_velocity = 0










    if hands and 0.2 < hands[0]['bbox'][2]/hands[0]['bbox'][3]<0.55 \
            and (hands[0]['type'] == 'Right'):
        yaw_velocity = -40
        left_right_velocity = 40
        print('frramgy')

    elif hands and 0.2 < hands[0]['bbox'][2]/hands[0]['bbox'][3]<0.55 \
            and (hands[0]['type'] == 'Left' ):

        yaw_velocity = 40
        left_right_velocity = -40

    else :
        yaw_velocity = 0

    # 2

    me.send_rc_control(left_right_velocity,forward_backward_velocity,up_down_velocity,yaw_velocity)
    cv2.imshow('img', img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & cv2.waitKey(1) == 113:
        me.land()
        break

me.land()