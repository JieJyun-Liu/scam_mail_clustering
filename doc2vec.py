'''
	Date: 2019/08/12
	Author: Eleven
	Description: Train and test doc2vec.
		- K=5, epoch = 40, Silhouette Score: 0.12878385, 0:39:19.228922 s
		- K=5, epoch = 1000, Silhouette Score: 0.20264252, 6+ hours
'''

import gensim
import os
import collections
from gensim.test.utils import get_tmpfile
from gensim.models.doc2vec import Doc2Vec, LabeledSentence
from sklearn import metrics
from sklearn.cluster import Birch
import codecs

from os.path import join
from datetime import datetime
from configs import cfg

class Doc2VecModel():
	def __init__(self):
		pass

	def go(self):
		start=datetime.now()
		if not os.path.isfile(join(cfg.pretrained_model_dir, 'model_doc2vec.model')):
			train_dataset = self.load_dataset(join(cfg.output_dir, 'articles.txt'))
			self.train(train_dataset)
		else:
			self.test()

		print("[INFO] Total costs ", datetime.now()-start, " secs")

    # Load email_body
	def load_dataset(self, file_name):
		with open(file_name, 'r') as f:
			doc_list = f.readlines()

		print("Load dataset ....")
		dataset = []
		for i, content in enumerate(doc_list):
			words = content.split(' ')
			words[-1] = words[-1].strip()
			TaggededDocument = gensim.models.doc2vec.TaggedDocument
			document = TaggededDocument(words, tags=[i])
			dataset.append(document)

		return dataset

	def train(self, dataset):
		print("Train Doc2Vec ....")
		print("[INFO] Dataset: ", len(dataset))
		model = Doc2Vec(dataset, vector_size=cfg.vector_size, window=cfg.window_size, min_count=cfg.min_count, workers=cfg.worker_count)
		fname = join(cfg.output_dir, "model_doc2vec.model")
		model.save(fname)

	def test(self):
		print("Test Doc2Vec ....")
		model_path = join(cfg.pretrained_model_dir, "model_doc2vec.model")
		test_dataset = join(cfg.output_dir, 'articles_test.txt')
		 
		#load model
		model = Doc2Vec.load(model_path)
		test_dataset = [x.strip().split() for x in codecs.open(test_dataset, "r", "utf-8").readlines()]
		self.cluster(model, test_dataset)

	# [Note] It takes 6+ hours for Air do this. (1000 epochs, 5 clusters)
	def cluster(self, model, test_dataset, k=5, start_alpha=0.01):
		X=[]
		for d in test_dataset:
			X.append(model.infer_vector(d, alpha=start_alpha, steps=cfg.epochs))    

		brc = Birch(branching_factor=50, n_clusters=k, threshold=0.1, compute_labels=True)
		brc.fit(X)
		 
		clusters = brc.predict(X)
		labels = brc.labels_

		for idx, cluster_id in enumerate(clusters):
			print("Test article #", idx, ": ", cluster_id)
		silhouette_score = metrics.silhouette_score(X, labels, metric='euclidean')
		print ("### Silhouette_score: ", silhouette_score)


d2v = Doc2VecModel()