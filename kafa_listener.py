#!/usr/bin/env python  
import roslib
# roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import time
import almath
from math import atan2, acos, sqrt, pi
from naoqi import ALProxy

def angleBetweenVectors(v1, v2):
    #print 'vectors ', v1, v2
    [up, down1, down2] = [0, 0, 0]
    for i in range(len(v1)):
        [up, down1, down2] = [up+v1[i]*v2[i], down1+v1[i]*v1[i], down2+v2[i]*v2[i]]
    return acos(up / sqrt(down1) / sqrt(down2))

def rad2deg(rad):
    return 180*rad/pi

if __name__ == '__main__':
    
    rospy.init_node('kollar_node')
    motionProxy = ALProxy("ALMotion", "192.168.1.113", 9559)
    motionProxy.setStiffnesses("Body", 1.0)
    listener = tf.TransformListener()
    fractionMaxSpeed = 0.2
    motionProxy.setMoveArmsEnabled(False, False)
    step_length = 0.04 # 4 cm

    rate = rospy.Rate(10.0)
    step = 0
    lastStep = -100

    while not rospy.is_shutdown():
        try:
            (left_shoulder_trans,left_shoulder_rot) = listener.lookupTransform('/left_shoulder_1', '/openni_depth_frame', rospy.Time(0))
            (left_hand_trans,left_hand_rot) = listener.lookupTransform('/left_hand_1', '/openni_depth_frame', rospy.Time(0))

            (right_shoulder_trans,right_shoulder_rot) = listener.lookupTransform('/right_shoulder_1', '/openni_depth_frame', rospy.Time(0))
            (right_hand_trans,right_hand_rot) = listener.lookupTransform('/right_hand_1', '/openni_depth_frame', rospy.Time(0))
            
            (left_knee_trans,left_knee_rot) = listener.lookupTransform('/left_knee_1', '/openni_depth_frame', rospy.Time(0))
            (left_hip_trans,left_hip_rot) = listener.lookupTransform('/left_hip_1', '/openni_depth_frame', rospy.Time(0))
            (left_foot_trans,left_foot_rot) = listener.lookupTransform('/left_foot_1', '/openni_depth_frame', rospy.Time(0))


        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print 'exception'
            continue
        
        step = step + 1

        angle_left_shoulder_pitch = angleBetweenVectors([left_hand_trans[1] - left_shoulder_trans[1], left_hand_trans[2] - left_shoulder_trans[2]], [-1, 0])
        angle_left_sholder_roll = angleBetweenVectors([left_hand_trans[0] - left_shoulder_trans[0], left_hand_trans[2] - left_shoulder_trans[2]], [0, 1])
        angle_right_shoulder_pitch = angleBetweenVectors([right_hand_trans[1] - right_shoulder_trans[1], right_hand_trans[2] - right_shoulder_trans[2]], [-1, 0])
        angle_left_knee = angleBetweenVectors([
                left_knee_trans[0] - left_hip_trans[0],
                left_knee_trans[1] - left_hip_trans[1],
                left_knee_trans[2] - left_hip_trans[2]
            ],
            [
                -left_foot_trans[0] + left_knee_trans[0], 
                -left_foot_trans[1] + left_knee_trans[1],
                -left_foot_trans[2] + left_knee_trans[2]
            ]
            )
        #print 'angle left shoulder roll ', rad2deg(angle_left_sholder_roll)
        #print 'angle left shoulder pitch ', rad2deg(angle_left_shoulder_pitch)
        #print 'angle right shoulder pitch ', rad2deg(angle_right_shoulder_pitch)
        #print 'angle left knee ', rad2deg(angle_left_knee)
        if step % 10 == 0:
            print ' acin:', left_hip_rot

        names = ['LShoulderPitch', 'LShoulderRoll', 'RShoulderPitch', 'RShoulderRoll']
        angles = [pi/2 - angle_right_shoulder_pitch, 0, pi/2 - angle_left_shoulder_pitch, 0]
        
        motionProxy.setAngles(names, angles, fractionMaxSpeed)
        if left_hip_rot[2] < 0.30 and left_hip_rot[2] >= 0.15:
            # lastStep = step
            print "ADIM ", left_hip_rot[2]
            motionProxy.moveTo(step_length,0,0)
        
        rate.sleep()
