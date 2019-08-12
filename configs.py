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
		parser.add_argument('--pretrained_model_dir', help='location of pretrained model', default=join(self.project_dir, 'pretrained_model'))
		
		# Model parameters for doc2vec.
		parser.add_argument('--vector_size', help='Dimensionality of the feature vectors.', default=100)
		parser.add_argument('--window_size', help='The maximum distance between the current and predicted word within a sentence.', default=3)
		parser.add_argument('--min_count', help='Ignore words with frequencies < min_count.', default=5)
		parser.add_argument('--sampling_threshold', help='(0, 1e-5)', default=1e-3)
		parser.add_argument('--negative_size', help='>0, use negative sampling : (5,20)', default=5)
		parser.add_argument('--epochs', help='# of epochs', default=40)
		parser.add_argument('--dm', help='dm=1, distributed memory (PV-DM) / dm=0, distributed bag of words (PV-DBOW)', default=0)
		parser.add_argument('--worker_count', help='# of worker threads', default=3)

		# parser.set_default(shuffle=True)
		self.args = parser.parse_args()

		for key, value in self.args.__dict__.items():
			if key not in ['test', 'shuffle']:
				exec('self.%s = self.args.%s' % (key, key))


cfg = Configs()