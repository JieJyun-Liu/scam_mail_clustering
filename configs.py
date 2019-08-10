'''
	Date: 2019/08/10
	Author: Eleven
	Description: Configs of global variables.
'''

import os
import argparse
from os.path import join

class Configs(object):
	def __init__(self):
		self.project_dir = os.getcwd()
		self.dataset = join(self.project_dir, 'data')
		
		parser = argparse.ArgumentParser()
		parser.add_argument('--mode', help='preprocess/train/test', default='preprocess')
		parser.add_argument('--train_dir', help='location of training data', default=join(self.dataset, '419scam/train'))
		parser.add_argument('--test_dir', help='location of test data', default=join(self.dataset, '419scam/test'))
		parser.add_argument('--output_dir', help='location of output data', default=join(self.dataset, 'output'))

		# parser.set_default(shuffle=True)
		self.args = parser.parse_args()

		for key, value in self.args.__dict__.items():
			if key not in ['test', 'shuffle']:
				exec('self.%s = self.args.%s' % (key, key))


cfg = Configs()