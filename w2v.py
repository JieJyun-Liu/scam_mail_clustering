'''
	Date: 2019/08/11
	Author: Eleven
	Description: Extract and write email_bodies to file.
				[TODO or skip] Train 100D w2v by emailbody.
'''
import json
import os
import re

# from gensim.models import Word2Vec, KeyedVectors
from configs import cfg
from utils.FileUtils import write_data_to_file
from os.path import join

class Word2VecModel():
	def __init__(self):
		# if article.txt is none, preprocess email_body
		pass

	def go(self):
		self.preprocess()

	# Get email bodies from output dir.
	def preprocess(self):
		for f in os.listdir(cfg.output_dir):
			if os.path.isdir(join(cfg.output_dir, f)):	continue
			self.get_and_write_email_bodies_to_file(join(cfg.output_dir, f))

	def get_and_write_email_bodies_to_file(self, src_path):
		with open(src_path, 'r') as f:
			lines = f.readlines()
			print("[Get email body] Write " + str(len(lines)) + " sentences from " + src_path)
			for line in lines:
				json_str = json.loads(line)
				data = json.loads(json_str)
				sentences = self.get_sentences(data['email_body'])
				write_data_to_file(join(cfg.output_dir, 'articles'), " <eos> ".join(sentences))
		f.close()

	def get_sentences(self, text):
		pattern = re.compile(r'[A-Z][^\.!?]*[^\.!?]', re.M)
		sentences = pattern.findall(text)
		for i in range(len(sentences)):
			sentences[i] = self.clean_text(sentences[i])

		return sentences

	def clean_text(self, text):
		text = re.sub(r"[,.:\\//\"_\-+=;@%#?!&$]+\ *", " ", text)
		text = text.lower()
		text = re.sub(" \d+", " <number> ", text)
		text = re.sub('\s+', ' ', text).strip()
		
		return text


	# def train(src_path, embedding_dim, context_len, min_freq, iteration, save_path):


	
	# def load(model_path):
	# 	return KeyedVectors.loal_word2vec_format(model_path)

w2v = Word2VecModel()