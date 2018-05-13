#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import cv2
import numpy as np

def get_out(img_name):
    img = cv2.imread(img_name)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 白色背景
    ret, threshold = cv2.threshold(imgray, 244, 255, cv2.THRESH_BINARY_INV)  # 把黑白颜色反转

    # 边缘检测
    image, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 获取各个边缘的面积大小
    areas = list()
    for i, cnt in enumerate(contours):
        areas.append((i, cv2.contourArea(cnt)))

    # 按面积大小对边缘进行排序，从大到小排序
    sorted_areas = sorted(areas, key=lambda d: d[1], reverse=True)#

    # 获取面积最大的边缘
    if len(sorted_areas) > 1:
        max_index = sorted_areas[1][0]
        max_contours = contours[max_index]
    else:
        print('empty img file:', img_name)
        return img

    # 创建目标图像(黑色背景)
    out = np.zeros_like(img)

    # 获取凸包
    hull = cv2.convexHull(max_contours)

    # 填充颜色
    fill_color = (255, 255, 255)
    cv2.drawContours(out, [hull], -1, fill_color, thickness=-1)

    return out

def save_out(out_dir, img_name):
    pure_img_name = img_name.split('/')[-1]
    out_name = out_dir + '/' + pure_img_name
    out = get_out(img_name)
    cv2.imwrite(out_name, out)

def main(source_dir, target_dir):
    source_files_pattern = '/*.png'
    source_files = glob.glob(source_dir + source_files_pattern)
    #print(source_files)
    for source_file in source_files:
        save_out(target_dir, source_file)

def help():
    print('usage: python main.py source_dir target_dir')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        help()
        exit()

    source_dir = sys.argv[1]
    target_dir = sys.argv[2]

    if not os.path.exists(source_dir):
        print('source_dir not exist!')
        print('please try again!')
        help()
        exit()

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    main(source_dir, target_dir)
