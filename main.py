import nltk
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import pos_tag

import random,re

from data.qstn_words import *
from rules.pattern import *
from corpus.repeat import *
from syntax_analysis import *
from semantic_analysis import *
from modules.preprocessing import *
from modules.preprocessing.preprocess import *
from textrank import *
'''
Here question is reply by human
answer is reply bot
'''

class Chat:
	def __init__(self):
		self.count = 0
		self.sentence = ''
		self.prev_qstn = ''
		self.qstn_noun = ''#noun retrieved from question
		self.qstn_pronoun = ''#pronoun retrieved from question
		self.ans_noun = ''#retrieved from answer
		self.ans_pronoun = ''
		self.question = ''
		self.original_sent = ''
		self.answer = ''
		#replied from which category
		#so that we can deecide which answer to be replied for the next question
		self.syntax_analysis = Syntax_Analysis()
		self.semantic_analysis = Semantic_Analysis()

	def match_question(self):
		for rule in rules:
			for qstn in rule[0]:
				if qstn == self.sentence:
					return random.choice(rule[1])
		return None
		
	def reply(self):
		temp = self.match_question()
		if not temp:
			self.syntax_analysis.syntax_analyse(self.sentence)
			sa = self.syntax_analysis
			if not sa.words:
				return random.choice(unknown)
			answer = self.semantic_analysis.semantic_analyse(self.original_sent,sa.sentence, sa.tags, sa.words, sa.qstn_type, sa.qstn_word, sa.helping_verb, sa.disc_qstn, sa.disc_word)
			return answer
		else:
			return temp

def main():
	chat = Chat()
	pp = Preprocess()
	chat.count = 0 #count of continuously repeating the question
	
	print 'To exit say "bye"\n'
	print "Bot > Hello!"
	#is_intent_present = False
	while(True):
		
		chat.sentence = raw_input("You > ")
		chat.original_sent = chat.sentence
		temp_sentence = chat.sentence
		sentences = nltk.sent_tokenize(temp_sentence)
		key_sentence = ''
		if(len(sentences)>1):
			key_sentence = pp.find_key_sent(ranks(temp_sentence))
		if(key_sentence):
			temp_sentence = key_sentence
			chat.sentence = key_sentence
			
		# step 1: preprocessing
		chat.sentence = chat.sentence.lower()
		chat.sentence = pp.preprocess(chat.sentence)
		
		#step 2: default answering
		#checking whether sentence is empty
		#print "chat.sentence ",chat.sentence
		if not chat.sentence:
			print "Bot > ",random.choice(null_replies)
			continue
		#exit
		if chat.sentence == 'bye':
			print random.choice(exit_messages)
			break
		
		#counting the no of times question asked
		if chat.prev_qstn == chat.sentence:
			chat.count = chat.count + 1
			if chat.count == 7:
				print "Bot > ",random.choice(warning_messages)
				continue
			if chat.count > 7:
				print "Bot > ",random.choice(force_quit)
				break
			if chat.count>5:
				print "Bot > ",random.choice(tired_replies2)
				continue
			if chat.count > 2:
				print "Bot > ",random.choice(tired_replies1)
				continue
		else:
			chat.prev_qstn = chat.sentence
			chat.count = 1
			
		## Precessing The Sentences With "Natural Language Processing"
		print "Bot > ",chat.reply()
	
if __name__=='__main__':
	main()

