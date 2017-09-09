
#professions
with open("corpus/data/profession") as f:
	text = f.read()
text = text.split('\n')[:-1]
professions = [line.split('$') for line in text]

with open("corpus/data/synonyms") as f:
	text = f.read()
synonyms = text.split('\n')[:-1]
synonyms = [line.split(',') for line in synonyms]
'''print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5"
print synonyms
print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5"'''
#scholorship
with open("corpus/scholarship") as f:
	text = f.read()
scholarship = text.split('\n')
scholarship = [line.split(',') for line in scholarship]

no_entity_replies = [
	"Please! Ask me relevant questions.",
	"Sorry! I don't what is you are asking about.",
	"Sorry! That is not up to my knowledge!"]

#abbreviations

with open("corpus/data/abbreviation") as f:
	abbreviations = f.read()
abbreviations = abbreviations.split('\n')[:-1]
abbreviations = [line.split('$') for line in abbreviations]

#category
with open("corpus/data/category") as f:
	category = f.read()
category = category.split('\n')[:-1]
category = [line.split('$') for line in category]

#distance
with open("corpus/data/distance") as f:
	distance = f.read()
distance = distance.split('\n')[:-1]
distance = [line.split('$') for line in distance]

#finance
with open("corpus/data/finance") as f:
	finance = f.read()
finance = finance.split('\n')[:-1]
finance = [line.split('$') for line in finance]

#location
with open("corpus/data/location") as f:
	location = f.read()
location = location.split('\n')[:-1]
location = [line.split('$') for line in location]

#reason
with open("corpus/data/reason") as f:
	reason = f.read()
reason = reason.split('\n')[:-1]
reason = [line.split('$') for line in reason]
#about
with open("corpus/data/about") as f:
	about = f.read()
about = about.split('\n')[:-1]
about = [line.split('$') for line in about]

sent_for_answer = ["okay!","Good to hear!","I think that's awesome"]
