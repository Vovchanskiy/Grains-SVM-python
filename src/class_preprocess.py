#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2016年11月25日
@author: li
图像预处理
'''

import cv2
import numpy as np
import sys

class my_Preprocess(object):
	def __init__(self, img_filename, resize=[48, 48]):
		self.img = cv2.imread(img_filename)
		self.img_gray = None
		self.img_bin = None
		
		self._resize(w=resize[0], h=resize[1])
		self._filter()
		self._rgb2gray()
		self._gray2binary(thresh=130, maxval=255)
		self._morphology(radius=3)
		
	def _rgb2gray(self):
		self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
		
	def _gray2binary(self, thresh=127, maxval=255):
		img_thresh = cv2.threshold(self.img_gray, thresh, maxval, cv2.THRESH_BINARY)[1]
		self.img_bin = 255 - img_thresh
		
	def _resize(self, w, h):
		self.img = cv2.resize(self.img, (w, h), interpolation=cv2.INTER_CUBIC)
	
	def _filter(self):
		# param 2 is radius
		img_medianBlured = cv2.medianBlur(self.img, 1)
		
		# param 2: d值，设置为负数则自动由后面两个值公式计算
		# param 3: sigmaColor，颜色空间滤波器的sigma值。这个参数的值越大，
		#          就表明该像素邻域内有更宽广的颜色会被混合到一起，产生较大的半相等颜色区域。
		# param 4: sigmaSpace，坐标空间中滤波器的sigma值，坐标空间的标注方差。他的数值越大，
		#          意味着越远的像素会相互影响，从而使更大的区域足够相似的颜色获取相同的颜色。
		#          当d>0，d指定了邻域大小且与sigmaSpace无关。否则，d正比于sigmaSpace。
		self.img = cv2.bilateralFilter(img_medianBlured, -1, 20, 20)
	
	
	def _morphology(self, radius=3):
		# 形态学滤波:对大米不好处理，薏米有两个沟
		kernel = np.ones((radius, radius), np.uint8)
		self.img_bin = cv2.morphologyEx(self.img_bin, cv2.MORPH_CLOSE, kernel)
		
	def get_img(self):
		return self.img
	
	def get_img_gray(self):
		return self.img_gray
	
	# 返回的二值图像，非0值是前景，对应原图中颜色较深的分量（RGB值低的像素）
	def get_img_binary(self):
		return self.img_bin
	
if __name__ == '__main__':
	mypreprocess = my_Preprocess("../data/s.png")
	
	
	cv2.imshow('image1', mypreprocess.get_img())
	cv2.imshow('image2', mypreprocess.get_img_binary())
	cv2.waitKey(0)
	cv2.destroyAllWindows()
