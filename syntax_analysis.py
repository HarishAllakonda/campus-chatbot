import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize,sent_tokenize

from rules.pattern import *
from data.qstn_words import *
from corpus.stopwords import *

'''
4 types of sentences
yes or no type 1
WH type 0
discriptive type 2 
neutral 3
'''

class Syntax_Analysis:
	def __init__(self):
		self.sentence = ''
		self.tags = []
		self.words = []
		self.qstn_type = -1
		self.qstn_word = ''
		self.helping_verb = ''
		self.disc_qstn = ''
		self.disc_word = ''
	
	def remove_stopwords(self):
		self.words = [word for word in self.words if word not in wh_qstn_words]
		self.words = [word for word in self.words if word not in yrn_qstn_words]
		self.words = [word for word in self.words if word not in stopwords]
	
	## finding out type of question 0-wh qstn 1-y/n type 2-disc qstn 3-neutral qstn
	def type_of_question(self):
		for i in range(len(self.tags)):
			if self.qstn_word and self.helping_verb:
				break
			if not self.qstn_word and self.tags[i][1] in wh_qstn_tags and self.tags[i][0] in wh_qstn_words:
				self.qstn_word = self.tags[i][0]
				if(self.qstn_word == 'how'):
					try:
						if self.tags[i+1][0] in ['many','much','far','long']:
							self.qstn_word += " "+self.tags[i+1][0]
					except:
						pass
				if not self.qstn_word:
					if self.tags[i][0] in yrn_qstn_tags and self.tags[i][1] in yrn_qstn_words:
						self.helping_verb = self.tags[i][1]
				else:
					try:
						if self.tags[i+1][0] in yrn_qstn_tags and self.tags[i+1][1] in yrn_qstn_words:
							self.helping_verb = self.tags[i+1][1]
					except:
						pass
			if not self.helping_verb and self.tags[i][1] in yrn_qstn_tags and self.tags[i][0] in yrn_qstn_words:
				self.helping_verb = self.tags[i][0]
		if self.qstn_word:
			self.qstn_type = 0
		elif self.helping_verb:
			self.qstn_type = 1
		else:
			if self.tags[0][0] in disc_qstns:
				self.qstn_type = 2
				self.disc_word = self.tags[0][0]
			else:
				self.qstn_type = 3
			
	def syntax_analyse(self,sentence):
		self.sentence = sentence
		self.qstn_type = -1
		self.qstn_word = ''
		self.helping_verb = ''
		self.disc_qstn = ''
		self.disc_word = ''
		self.words = word_tokenize(self.sentence)
		self.tags = pos_tag(self.words)
		self.type_of_question()
		self.remove_stopwords()
		'''
		print "###############"
		print self.sentence,self.tags,self.words,self.qstn_type,self.qstn_word,self.helping_verb,self.disc_qstn,self.disc_word
		print "###############"
		'''
