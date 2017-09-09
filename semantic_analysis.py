import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize,sent_tokenize
from corpus.corpus import *
from corpus import *
import random

verb_tags = ['VB','VBG','VBN','VBZ','VBD']
subject_tags = ['JJ','NN','NNS']
reflexes = [['i','you'],['you','i'],['we','you']]

class Semantic_Analysis:
	
	def __init__(self):
		self.sentence = ''
		self.tags = []
		self.words = []
		self.qstn_type = -1
		self.qstn_word = ''
		self.helping_verb = ''
		self.disc_qstn = ''
		self.disc_word = ''
		
	def is_abbreviation(self,word):
		for ab in abbreviations:
			if ab[0] == word:
				return True
		return False
		
	def rest_wh_answer(self,data_to_access,new_entity):
		temp_answer = self.get_answer(data_to_access,new_entity)
		if not temp_answer:
			return random.choice(no_entity_replies)
		return temp_answer[2]
		
	def get_answer(self, data_list, new_entity):
		set_entity = set(new_entity.split(' '))
		for data in data_list:
			if set(data[0].split(' ')) == set_entity:
				#print data[0].split(' '),set_entity
				return data
		return ""
		
	
	def get_wh_answer(self, tok_new_sent, tok_old_sent, new_entity):
		if self.qstn_word == 'who':
			temp_answer = self.get_answer(professions, new_entity)
			if not temp_answer:
				return random.choice(no_entity_replies)
			answer = ''
			#print "temp_answer",temp_answer
			if self.is_abbreviation(new_entity):
				new_entity = new_entity.upper()
			if(temp_answer[1] == '.'):
				return temp_answer[2]
			else:
				if self.helping_verb:
					answer = new_entity+" "+self.helping_verb+" "+temp_answer[1]
				else:
					answer = new_entity+" is "+temp_answer[1]
				answer += ". "+temp_answer[2].capitalize()+" ."
				return answer
		else:
			answer = ''
			if self.qstn_word == 'where':
				answer = self.rest_wh_answer(location,new_entity)
			elif self.qstn_word == 'which':
				answer = self.rest_wh_answer(category,new_entity)
			elif self.qstn_word == 'why':
				answer = self.rest_wh_answer(reason,new_entity)
				#set(self.qstn_word) == set('how much')
			else:
				answer = self.rest_wh_answer(about,new_entity)
			return answer

	def find_synonym(self,entity):
		for line in synonyms:
			try:
				line.index(entity)
				return line[0]
			except:
				pass
		return ''
	
	def get_subject(self):
		pronouns = ['i','we','you','it','he','she','it','they']
		words = list(set(word_tokenize(self.sentence)))
		for word in words:
			if word.lower() in pronouns:
				for reflex in reflexes:
					if reflex[0] == word.lower():
						return reflex[1]
				return word.lower()
	
	def semantic_analyse(self,original_sent,sentence,tags,words,qstn_type,qstn_word,helping_verb,disc_qstn,disc_word):
		
		self.sentence, self.tags, self.words, self.qstn_type, self.qstn_word, self.helping_verb, self.disc_qstn, self.disc_word = sentence, tags, words, qstn_type, qstn_word, helping_verb, disc_qstn, disc_word
		
		
		entity = ''
		action = ''
		subject = ''
		answer = ''
		flag = 0

		#named_entities = NamedEntityRecognition().ne_recognizer(original_sent)

		intents = []
		for word in self.words:
			for token,tag in self.tags:
				if token==word:
					intents.append((token,tag))
		
		print "Intents",intents

		tokenized_sentence = word_tokenize(self.sentence)
		#print "tokenized_sentence",tokenized_sentence
		for intent in intents:
			if intent[1] in verb_tags and not action:
				action =  intent[0]
		
		flag = 0
		index_value = -1
		if not intents:
			return random.choice(no_entity_replies)
		for intent in intents:
			if intent[1] in subject_tags:
				if(flag ):
					if(tokenized_sentence.index(intent[0]) == index_value+1):
						entity += " "+intent[0]
					else:
						#print "Break",entity
						break
				else:
					entity = intent[0]
					flag = 1
					index_value = tokenized_sentence.index(intent[0])
		print "Entity :"+entity
		if not entity:
			return random.choice(no_entity_replies)
		subject = self.get_subject()
		if(subject ):
			#print "0"
			answer = subject
			if answer:
				#print "1"
				answer+= " "+self.helping_verb
			if answer:
				#print "2"
				answer+= " "+action
			if entity:
				#print "3"
				answer+= " "+entity
		#print "Answer ",answer
		new_entity = self.find_synonym(entity)
		
		print "new_entity",new_entity
		if not new_entity:
			select = random.randrange(0,2)
			if(select):
				index = random.randrange(-1,3)
				if(index==-1):
					if(entity):
						if(self.qstn_word):
							answer = "Sorry! I don't know "+self.qstn_word
							if(self.helping_verb):
								answer += " "+self.helping_verb+" "+entity+"."
								return answer
							else:
								answer += " is "+entity+"."
								return answer
						else:
							answer = "Sorry! I don't know what is "+entity+"."
							return answer
					else:
						answer = no_entity_replies[random.randrange(0,3)]
						return answer
				else:
					answer = no_entity_replies[index]
					return answer
			else:
				return random.choice(sent_for_answer)
		'''
		print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2"
		print self.qstn_word, self.helping_verb, entity
		print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2"
		'''
		print self.qstn_type
		if self.qstn_type == 0:
			answer = self.get_wh_answer(tokenized_sentence,word_tokenize(original_sent), new_entity)
			return answer
		elif self.qstn_type == 1:
			answer = self.get_wh_answer(tokenized_sentence,word_tokenize(original_sent), new_entity)
			return answer
		elif self.qstn_type == 2:
			answer = self.get_wh_answer(tokenized_sentence,word_tokenize(original_sent), new_entity)
			return answer
		else:
			return "Nothing"
