import re,random

class Preprocess:
	def __init__(self):
		self.sentence = ''
	
	def remove_extra_end_spaces(self):
		self.sentence = self.sentence.rstrip()
		self.sentence = self.sentence.lstrip()
		self.sentence = re.sub(' +',' ',self.sentence)
		
	def preprocess(self, sentence):
		self.sentence = sentence
		if self.sentence.isspace():
			return None
		self.sentence = re.sub(r"[^A-Za-z0-9& ]+",'',self.sentence)
		self.remove_extra_end_spaces()
		return self.sentence
		
	def find_key_sent(self,ranked_sentences):
		neutral_sentences = open('corpus/neutral_sentences','r+').read().split('\n')[0:]
		#print neutral_sentences
		key_sentence = ''
		#print ranked_sentences[0:]
		for rank,sentence in ranked_sentences:
			temp_sentence = self.preprocess(sentence)
			if temp_sentence.lower() in neutral_sentences or len(temp_sentence.split(' '))<3:
				continue
			else:
				key_sentence = sentence
				return key_sentence
		return key_sentence
