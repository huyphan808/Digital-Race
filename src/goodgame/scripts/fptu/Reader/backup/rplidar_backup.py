#!/usr/bin/env python3

import os
import numpy as np
from std_msgs.msg import Header,String,Float32,Int8,Bool
from sensor_msgs.msg import CompressedImage,Image,LaserScan
import rospy
import cv2
import time
import math
from speed_up_lidar import lidar_speed,lidar_speed_backup

class rplidar:
    def __init__(self):
        
        self.distance_x_min= 99  
        self.distance_y_min= 99 
        self.distance_y_min_raw = 99 
        self.distance_x_min_raw = 99
        self.lidar_bool_obstacle = False
        self.lidar_bool_tradinh=0

        self.laserscan = rospy.Subscriber("/scan",
                                    LaserScan,
                                    self.scanCallback,
                                    queue_size=1000)  
        #bien bao cam 
        self.sign_noleft_noright= rospy.Publisher("/sign_noleft_noright",Bool,queue_size=1)

        self.detection = rospy.Publisher("/lidar_detection",Bool,queue_size = 1)       
        self.stop_avoid_obstacles = rospy.Publisher("/stop_avoid_obstacles",Bool,queue_size=1)

        '''
        sign_time:  bien stop
        sign_time_1:  bien re
        sign_time_2:  bien cam
        '''
        self.sign_time = rospy.Publisher("/sign_time",Bool,queue_size=1)

        self.sign_time_1= rospy.Publisher("/sign_time_1",Bool,queue_size=1)
        self.sign_time_2= rospy.Publisher("/sign_time_2",Bool,queue_size=1)

        
    def scanCallback(self,ros_data):
        #rospy.set_param('range_min', )
        #rospy.set_param('angle_increment', -0.5235987756)
        count = int(ros_data.scan_time / ros_data.time_increment)
        
        #rospy.loginfo("I heard a laser scan %s[%d]:",str(ros_data.header.frame_id),count)
        
        #rospy.loginfo("Angle_range, %f, %f",self.radtodeg(ros_data.angle_min),self.radtodeg(ros_data.angle_max))
        
        #print("hereeeeeeeeeeeeeeeeeeeee",ros_data.ranges)
        #distance_x_min = 99.0
        '''mo comment'''
        # lidar_bool,matran_tradinh_X,matran_tradinh_Y = lidar_speed(count,ros_data.ranges,self.distance_x_min,self.distance_y_min,self.distance_y_min_raw, self.distance_x_min_raw)
        '''dong comment'''
        bao_hieu_1,bao_hieu_2,bao_hieu_3,bao_hieu_4,matran_tradinh_X,matran_tradinh_Y = lidar_speed_backup(count,ros_data.ranges,self.distance_x_min,self.distance_y_min,self.distance_y_min_raw, self.distance_x_min_raw)
        '''
        bao_hieu_1=1:vat can
        bao_bieu_2 =1: stop
        bao_hieu_3 =1: bien re
        bao_hieu_4 = 1: bien bao cam
        '''
        # print("DDDDDDDDDDDAAAAAAAAAAAAAAAAAAAAAAAAATTTTTTTTTTTTTTTAAAAAAAAAAAAA", ros_data.ranges)
        #rospy.logerr("GIA TRI LIDAR:   " + str(lidar_bool))
        # anh_lidar =np.zeros((512,512,3), np.uint8)
        # print("herrrrreeeeeeeeeeeeeeee", anh_lidar)
        '''open comment'''
        #img_trab = cv2.imread('/home/goodgame/Desktop/hello.png') 
        #anh_lidar= np.zeros((768,768,3),np.uint8)
        # print('HERRRREEEEEEEEEEEEEEEEEEEEEEEEEEE1111111111111111111111', matran_tradinh_X)
        # print('hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee2222222222222222' ,matran_tradinh_Y)
        #for i in range(0,len(matran_tradinh_X)):
        #    if 0<matran_tradinh_X[i]<768 and 0< matran_tradinh_Y[i]<768:
        #        cv2.circle(anh_lidar,(768-matran_tradinh_X[i],768-matran_tradinh_Y[i]),2,(255,255,0), -1)
        #cv2.rectangle(anh_lidar,(384-5,384-11),(384+5,384+11),(0,0,255),-1)
        #cv2.imshow('hello',anh_lidar)
        #cv2.waitKey(1)
        '''end'''
        '''
        open comment here
        '''
        # print("sfhalkjfhalfhafjklasfhawl",lidar_bool)
        # if lidar_bool == -1:
        #     rospy.logerr("VAT CAN O DAY!!!")
        #     self.lidar_bool_obstacle = True
        #     self.detection.publish(True)
        #     self.lidar_bool_tradinh = 5
        # else:
        #     self.lidar_bool_tradinh = self.lidar_bool_tradinh-1
        '''
        close comment here
        '''
        if bao_hieu_1 == 1:
            rospy.logerr("VAT CAN O DAY!!!")
            self.lidar_bool_obstacle = True
            self.detection.publish(True)
            self.lidar_bool_tradinh = 5
        else:
            self.lidar_bool_tradinh = self.lidar_bool_tradinh-1
            
        #rospy.logerr("hello " +str(self.lidar_bool_tradinh) +str(min(ros_data.ranges[179:359])))
        #print("hereeeeeeeeeeeeeeeeeeeeee", min(ros_data.ranges))
        #print("fuckinggggggggggggggggggggggggg" ,ros_data.ranges[179:189], "hello" , min(ros_data.ranges[179:189]))

        if min(ros_data.ranges[179:359]) > 0.6 and self.lidar_bool_obstacle == True and self.lidar_bool_tradinh <1:
            self.stop_avoid_obstacles.publish(True)
            self.lidar_bool_obstacle = False
            rospy.logerr("BACK_RIGHT_LANE!!")
        #self.countdown = self.countdown -1
        self.distance_x_min=99
        self.distance_y_min=99
        self.distance_y_min_raw=99
        self.distance_x_min_raw = 99
        rospy.logerr("GIA TRI MIN:   " + str(min(ros_data.ranges[179:359])))
        
        # if 0.1 < min(ros_data.ranges[179:359]) <= 2:
        #     rospy.logerr("BIEN BAO CAM ")
        #     self.sign_noleft_noright.publish(True)
        # else:
        #     self.sign_noleft_noright.publish(False)
        #print("lidar_bool",lidar_bool)
        # if lidar_bool == 1:
        #     self.sign_time.publish(True)
        '''
        open comment here
        '''
        if bao_hieu_2 == 1:# bien stop
            self.sign_time.publish(True)
        if bao_hieu_3 == 1:# bien re
            self.sign_time_1.publish(True)
        if bao_hieu_4 == 1:# bien cam
            self.sign_time_2.publish(True)
        



if __name__ == '__main__':

    rospy.init_node('rplidar', anonymous=True)

    rplidar = rplidar()

    try:
        rospy.spin()
        # print('HERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR', matran)
        # cv2.imshow('lidar_map', matran)
    except KeyboardInterrupt:
        print("Shutting down ROS Image feature detector module")
    # cv2.waitKey(1)

    #cv2.destroyAllWindows():
