import torch
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float64
from cv_bridge import CvBridge
import cv2

# or yolov5n - yolov5x6, custom
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
bridge = CvBridge()
ball_class = 32
ball_pos = [float(0.0), float(-1.0)]
image_detection_running = False

pos_X = -1
pos_Y = -1

# CONSTANTS FOR DISTANCE CALCULATION
SENSOR_HEIGHT = 2.70
FOCAL_LENGTH = 1.67  # 24
BALL_HEIGHT = 67
HEIGHT_CAMERA = 5.8
WIDTH_CAMERA = 13.3


def callback(img: Image):
    global ball_pos_pub, ball_pos, image_detection_running, ball_debug_pub

    # if image_detection_running:
    #     return

    image_detection_running = True

    # rospy.loginfo("Uhh I got a new image")

    cv_image1 = bridge.imgmsg_to_cv2(img, desired_encoding='passthrough')
    cv_image = cv2.flip(cv_image1, -1)
    cv2.imwrite('/app/cap.jpg', cv_image)
    # image_message = bridge.cv2_to_imgmsg(cv_image, encoding="passthrough")
    # ball_debug_pub.publish(img)

    # Inference
    results = model(cv_image)

    # results.print()
    p = results.pandas().xyxy[0]
    detections = p.to_dict(orient="records")
    ball_pos = [float(0.0), float(-1.0)]

    for d in detections:
        con = d['confidence']
        cs = d['class']
        x1 = int(d['xmin'])
        x2 = int(d['xmax'])
        # y1 = int(d['ymin'])
        # y2 = int(d['ymax'])
        x_center = int((x1 + x2) / 2)
        if cs == ball_class:

            # X POSITION
            rel = (BALL_HEIGHT/(x2-x1))
            pos_X_Pixel = (img.shape[1]/2) - (img.shape[1] - x_center)
            pos_X = pos_X_Pixel * rel

            # Y POSITION
            y1 = int(d['ymin'])
            y2 = int(d['ymax'])
            heightBallSensor = SENSOR_HEIGHT * ((y2-y1)/heightImg)
            relation_Height = heightBallSensor/FOCAL_LENGTH
            pos_Y = BALL_HEIGHT/relation_Height

            ball_pos = [pos_X, pos_Y]
            #float(x_center / cv_image.shape[1])
            # rospy.loginfo("I found a ball at %f with confidence %f", ball_pos, con)
            break
    image_detection_running = False


def loop():
    global ball_pos_pub, ball_pos
    if rospy.is_shutdown():
        return
    ball_pos_pub.publish(ball_pos)


def init():
    global ball_pos_pub, ball_debug_pub

    ball_pos_pub = rospy.Publisher('ball_pos', Float64MultiArray, queue_size=10)
    ball_debug_pub = rospy.Publisher('ball_debug', Image, queue_size=10)
    rospy.init_node('ball_schubser_detect', anonymous=True)
    rospy.Subscriber("cv_camera/image_raw", Image, callback)
    rospy.loginfo("Starting detection node ...")
    print("done")
    # rospy.spin()

    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        loop()
        rate.sleep()


if __name__ == '__main__':
    try:
        init()
    except rospy.ROSInterruptException:
        pass
