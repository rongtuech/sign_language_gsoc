#
# Copyright (C) 2019 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, os, traceback, time

from PySide2 import QtGui, QtCore
from genericworker import *
import numpy as np

import torch
from .inference.PytorchInference import HandPoseDetector
from .inference.ONNXAndTensorInference import BodyDetectorONNXInference, BodyDetectorONNXTensorRTInference


class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		self.timer.start(self.Period)
		#
		# if torch.cuda.is_available():
		# 	self.device = 'cuda:0'
		# else:
		# 	self,device = 'cpu'
		self.weight = ""

		# select inference model: pure pytorch, onnx, tensorrt
		# self.estimator = HandPoseDetector(self.weight)
		self.estimator = BodyDetectorONNXInference(self.weight)
		# self.estimator = BodyDetectorONNXTensorRTInference(self.weight)

	def setParams(self, params):
		return True

	@QtCore.Slot()
	def compute(self):
		print('SpecificWorker.compute...')

		return True

	#
	# getSkeleton
	#
	def getBodyAndHand(self, image, shape):
		image = np.reshape(image, shape)
		body_skeleton, hand_skeleton = self.estimator(image)
		return [body_skeleton, hand_skeleton]
