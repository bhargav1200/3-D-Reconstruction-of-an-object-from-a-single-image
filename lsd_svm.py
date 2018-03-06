#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-19 02:09:53
# @Author  : Gefu Tang (tanggefu@gmail.com)
# @Link    : https://github.com/primetang/pylsd
# @Version : 0.0.1

import cv2
import numpy as np
import os
import math
from pylsd import lsd
from matplotlib import pyplot as plt
from sklearn import linear_model, datasets
from sklearn.cluster import KMeans
import sys
import sys

fullName = 'Box_Image3.jpg'
folder, imgName = os.path.split(fullName)
axes_num = 3

src = cv2.imread(fullName, cv2.IMREAD_COLOR)
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

src_ran = src.copy()

lines = lsd.lsd(gray)
lines = lines[:,:]

points_dict = {}
points_dict['x']=[]
points_dict['y']=[]
points_dict['z']=[]

# Get the angle ranges for the axes
for i in range(lines.shape[0]):
    pt1i = (int(lines[i, 0]), int(lines[i, 1]))
    pt2i = (int(lines[i, 2]), int(lines[i, 3]))
    width = lines[i, 4]
    if(pt1i[1]<pt2i[1]):
        pt1i,pt2i=pt2i,pt1i
    angle=math.degrees(math.atan2((pt1i[0]-pt2i[0]),(pt1i[1])-pt2i[1]))
    print(angle)
    if((angle>50)and(angle<68)):
        points_dict['y'].extend((pt1i,pt2i))
        cv2.line(src, pt1i, pt2i, (0, 0, 255), int(np.ceil(width/2)))

    if((angle>-90)and(angle<-20)):
        points_dict['x'].extend((pt1i,pt2i))
        cv2.line(src, pt1i, pt2i, (0, 255, 0), int(np.ceil(width/2)))

    if((angle>-20)and(angle<0)):
        points_dict['z'].extend((pt1i,pt2i))
        cv2.line(src, pt1i, pt2i, (255, 0, 0), int(np.ceil(width/2)))

cv2.namedWindow('box',cv2.WINDOW_NORMAL)
cv2.imshow('box',src)

# On observing the detected lines, we find that one of the edges on the z axes is impossible to detect accurately. We thus obtain only 2 edges for this axes.
clusters_num = [3,3,2]

# Use k-means to cluster points of a line together
kmeans_dict={}
line_dict={}
file_dict={}
axes = ['x','y','z']
for k_idx in range(3):
    kmeans = KMeans(init='k-means++', n_clusters=clusters_num[k_idx])
    kmeans.fit(points_dict[axes[k_idx]])
    kmeans_dict[axes[k_idx]] = kmeans.labels_
    kmeans_dict[axes[k_idx]] = np.array(kmeans_dict[axes[k_idx]])
    print(kmeans_dict[axes[k_idx]])


    # Find the 3 lines for each axis
    line_dict[axes[k_idx]] = [[] for i in range(axes_num)]
    file_dict[axes[k_idx]] = [[[] for j in range(2)] for i in range(clusters_num[k_idx])]

    for line_idx in range(clusters_num[k_idx]):
        line_dict[axes[k_idx]][line_idx] = np.array(points_dict[axes[k_idx]])[np.where(kmeans_dict[axes[k_idx]]==line_idx)[0]]

        # Fit line and display
        [vx,vy,x,y] = cv2.fitLine(line_dict[axes[k_idx]][line_idx],cv2.DIST_WELSCH,0,0.01,0.01)
        lefty = int((-x*vy/vx) + y)
        righty = int(((gray.shape[1]-x)*vy/vx)+y)

        cv2.line(src_ran,(src_ran.shape[1]-1,righty),(0,lefty),(int((k_idx)==2)*255, int((k_idx)==0)*255, int((k_idx)==1)*255 ),2)

        file_dict[axes[k_idx]][line_idx][0] = (src_ran.shape[1]-1,righty)
        file_dict[axes[k_idx]][line_idx][1] = (0,lefty)

print(file_dict['y'][0])
cv2.namedWindow('box_ran',cv2.WINDOW_NORMAL)
cv2.imshow('box_ran',src_ran)

fl=open("input2.txt","w+");
fl.write("y1_edge_1:%d %d 1\n" %file_dict['y'][0][0])
fl.write("y1_edge_2:%d %d 1\n" %file_dict['y'][0][1])
fl.write("y2_edge_1:%d %d 1\n" %file_dict['y'][1][0])
fl.write("y2_edge_2:%d %d 1\n" %file_dict['y'][1][1])
fl.write("y3_edge_1:%d %d 1\n" %file_dict['y'][2][0])
fl.write("y3_edge_2:%d %d 1\n" %file_dict['y'][2][1])
fl.write("x1_edge_1:%d %d 1\n" %file_dict['x'][0][0])
fl.write("x1_edge_2:%d %d 1\n" %file_dict['x'][0][1])
fl.write("x2_edge_1:%d %d 1\n" %file_dict['x'][1][0])
fl.write("x2_edge_2:%d %d 1\n" %file_dict['x'][1][1])
fl.write("x3_edge_1:%d %d 1\n" %file_dict['x'][2][0])
fl.write("x3_edge_2:%d %d 1\n" %file_dict['x'][2][1])
fl.write("z1_edge_1:%d %d 1\n" %file_dict['z'][0][0])
fl.write("z1_edge_2:%d %d 1\n" %file_dict['z'][0][1])
fl.write("z2_edge_1:%d %d 1\n" %file_dict['z'][1][0])
fl.write("z2_edge_2:%d %d 1\n" %file_dict['z'][1][1])
fl.write("z3_edge_1:%d %d 1\n" %file_dict['z'][1][0])
fl.write("z3_edge_2:%d %d 1\n" %file_dict['z'][1][1])
fl.write("origin:1646 1747 1\n")
fl.write("reference_y:86 588 1\n")
fl.write("reference_x:2322 1239 1\n")
fl.write("reference_z:1808 1109 1")

cv2.waitKey(0)
