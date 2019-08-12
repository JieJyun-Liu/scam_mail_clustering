'''
	Date: 2019/08/10
	Author: Eleven
	Description: Main
'''

from utils.FileUtils import load_dataset
from configs import cfg
from doc2vec import d2v

import os
from os.path import join

# def train():

def preprocess():
	for f in os.listdir(cfg.train_dir):
		load_dataset(join(cfg.train_dir,f))


if __name__ == '__main__':
	# load_dataset(cfg.dataset + '/419scam/train/419scam_emails_201401')
	#  Preprocess: raw data to json file.
	if cfg.mode == 'preprocess':
		preprocess()
	else:
		d2v.go()
