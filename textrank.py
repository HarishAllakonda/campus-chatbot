from nltk.tokenize.punkt import PunktSentenceTokenizer
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import networkx as nx
from fuzzywuzzy import fuzz
import numpy as np

def ranks(text_input):
	sentence_tokenizer = PunktSentenceTokenizer();

	sentences = sentence_tokenizer.tokenize(text_input);

	no_of_sentences = len(sentences)

	c = CountVectorizer()
	bow_matrix = c.fit_transform(sentences)

	#print "bow_matrix : \n",bow_matrix

	normalized_matrix = TfidfTransformer().fit_transform(bow_matrix)

	#print "normalized_matrix\n",normalized_matrix

	similarity_graph = normalized_matrix * normalized_matrix.T

	similarity_graph.toarray()

	#print "similarity_graph :\n",similarity_graph


	nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
	scores = nx.pagerank(nx_graph)
	#for index,score in scores.iteritems():
	#	print index," : ",score

	ranked = sorted(((scores[i],s) for i,s in enumerate(sentences)) , reverse=True )
	
	out=[]
	max_no_of_sents = no_of_sentences;
	for rank in ranked[:max_no_of_sents]:
		for sentence in sentences:
			if(rank[1]==sentence):
				out.append([sentences.index(sentence),rank[1]])

	for i in range(len(out)):
		j=i+1
		for j in range(len(out)):
			if(out[i][0]<out[j][0]):
				temp = out[i]
				out[i] = out[j]
				out[j] = temp

	
	result = []
	for rank in range(len(out)):
		result.append(out[rank])
	return result
