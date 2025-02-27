## Natural Language ToolKit

#### Basic operations
# Tokenization
# Stemming and lemmatization
# POS tagging
# Syntactic parsing
# Edit distance

#### Advanced
# Named entity recognition
# Synonymy and antonymy
# Sentiment analysis

#### References
# https://likegeeks.com/nlp-tutorial-using-python-nltk/
# https://www.nltk.org/book/ch01.html "

### NLTK
#Advantages:
# very comprehensive
# Functions easily defined
# Comes with a rich collection of corpora
# A lot of material available


#Disadvantages:
# Tends to get slow for production-level applications (spaCy is more popular)
# Limitations of syntactic parsing
# Little incorporation of latest developments in machine learning (e.g deep learning applications)

#### Getting started

#importing required libraries
import nltk, pprint
from urllib import request
import re
nltk.download()

#download a text
url = "http://www.gutenberg.org/cache/epub/174/pg174.txt"
response = request.urlopen(url)
raw = response.read().decode('utf8')
len(raw)

type(raw)

### Tokenization:
# Splits sentence on white spaces
# Removes diacritics
# Segments out punctuation

text = nltk.word_tokenize(raw)

#type(text)
text[10:20]

re.findall(r"dent", str(text))

### Stemming and lemmatization

#### Stemming:
# removing inflectional elements from a form

#### Lemmatization:
# modifying the token to its canonical form, normally Nominative singular. Inflections are NOT dropped, e.g.

# Example from Russian:
# "sobake"/dog-n,Genitive Singular --> lemmatizes to "sobaka"; -a is an inflection


#STEMMING
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer

stemmer = PorterStemmer()
#stemmer = SnowballStemmer("english")

stemmer.stem("syllabi")
#try: irregular, rare and ambiguous nouns: "oxen", syllabi", "paintings""

#LEMMATIZATION
from nltk.stem import WordNetLemmatizer
L = WordNetLemmatizer()

#lemmatizing individual words
print(L.lemmatize("peopled", pos = "v"))

#compare to: print(L.lemmatize("paintings", pos = "v"))
#try print(L.lemmatize("peopled")) with and without "pos" = v

#lemmatizing text
for word in text[10:200]:
    print(L.lemmatize(word))

### POS tagging
#Penn Tree bank reference:
# CC coordinating conjunction
# CD cardinal digit
# DT determiner
# EX existential there (like: “there is” … think of it like “there exists”)
# FW foreign word
# IN preposition/subordinating conjunction
# JJ adjective ‘big’
# JJR adjective, comparative ‘bigger’
# JJS adjective, superlative ‘biggest’
# LS list marker 1)
# MD modal could, will
# NN noun, singular ‘desk’
# NNS noun plural ‘desks’
# NNP proper noun, singular ‘Harrison’
# NNPS proper noun, plural ‘Americans’
# PDT predeterminer ‘all the kids’
# POS possessive ending parent’s
# PRP personal pronoun I, he, she
# PRP\\$ possessive pronoun my, his, hers
# RB adverb very, silently
# RBR adverb, comparative better
# RBS adverb, superlative best
# RP particle give up
# TO, to go ‘to’ the store.
# UH interjection, errrrrrrrm
# VB verb, base form take
# VBD verb, past tense took
# VBG verb, gerund/present participle taking
# VBN verb, past participle taken
# VBP verb, sing. present, non-3d take
# VBZ verb, 3rd person sing. present takes
# WDT wh-determiner which
# WP wh-pronoun who, what
# WP$ possessive wh-pronoun whose
# WRB wh-abverb where, when

sentence = nltk.word_tokenize("he donated the painting to the museum")
#try ambiguous cases, e.g. "the old man the boat"
print(sentence)

#print(nltk.pos_tag(sentence))

#try:
#print(nltk.pos_tag("painting"))
#print(nltk.pos_tag(list("painting")))
print(nltk.pos_tag(["painting"]))

### Syntactic parsing

grammar = nltk.CFG.fromstring("""
... S -> NP VP
... PP -> P NP
... NP -> Det N | Det N PP | 'I'
... VP -> V NP | VP PP
... Det -> 'a' | 'an' | 'my'
... N -> 'book' | 'library' |'branch' | 'tree'
... V -> 'borrowed' | 'pruned'
... P -> 'from'
... """)

sent = nltk.word_tokenize("I pruned a branch from my tree")

parser = nltk.ChartParser(grammar)
for tree in parser.parse(sent):
    print(tree)
tree.draw()

from nltk.corpus import treebank
t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()

### NLTK continued
# Edit distance
# Sentiment analysis
# Working with lexicons (synonymy and antonymy)
# Named entity recognition

### Edit distance
# Known as the Levenshtein Distance
# Jaccard distance an alternative metric
# Covered in J&M Ch4
# Measured by the number of deletions, insertions or substitutions
# Common applications: plagiarism detection and spell checking"

#Edit distance: the fewer edit steps the smaller the distance
w1 = "dog"
w2 = "painting"
nltk.edit_distance(w1,w2)

#Jaccard distance: measures dissimilarity; the more similar the forms the smaller the value
w1 = set("dog")
w2 = set("painting")
nltk.jaccard_distance(w1,w2)

#Spell checker:
# given a misspelling, find the correct form with the shortest edit distance
misspelling = "nucular"
correction = ["tree", "linear", "war", "nominal", "night", "nocturnal", "fridge", "swallow", "novel", "blue", "navel", "nocturnal", "nucleus", "nuclear"]
for word in correction:
    distance = nltk.edit_distance(misspelling, word)
    print(word, distance)

# plagiarism detection
# compare source and target texts as to the edit distance at word-level
# texts with the greatest "

sent1 = "Olive Kitteridge is a 2014 four-hour miniseries based on the 2008 novel of the same name by Elizabeth Strout"
sent2 = "Olive Kitteridge is a 2014 4-hour long miniseries based on the 2008 novel of the same name by the writer Elizabeth Strout"
sent3 = "Following a 2008 novel Olive Kitteridge by Elizabeth Strout, a four-hour miniseries by the same name were made in 2014"
sent4 = "Elizabeth Strout's'novel, Olive Kitteridge published in 2008, became the basis for the four-hour miniseries released in 2014"
sent5 = "I love Python programming."

ed_sent_1_2 = nltk.edit_distance(sent1, sent2)
ed_sent_1_3 = nltk.edit_distance(sent1, sent3)
ed_sent_1_4 = nltk.edit_distance(sent1, sent4)
ed_sent_1_5 = nltk.edit_distance(sent1, sent5)


print(ed_sent_1_2, 'Edit Distance between sent1 and sent2')
print(ed_sent_1_3, 'Edit Distance between sent1 and sent3')
print(ed_sent_1_4, 'Edit Distance between sent1 and sent4')
print(ed_sent_1_5, 'Edit Distance between sent1 and sent5')

### Sentiment Analysis"

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

S = SentimentIntensityAnalyzer()
S.polarity_scores("I have not had any pleasure reading the book")

hotel_rev = ['Great place to be when you are in Barcelona.',
             'The place was being renovated when I visited so the seating was limited.',
             'Loved the ambience, loved the food',
             'The food is delicious but not over the top.',
             'Service - Little slow, probably because too many people.',
             'The place is not easy to locate',
             'Mushroom fried rice was tasty']

sid = SentimentIntensityAnalyzer()
for sentence in hotel_rev:
     print(sentence)
     ss = sid.polarity_scores(sentence)
     for k in ss:
         print('{0}: {1}, '.format(k, ss[k]), end='')
     print()

### Working with the lexicon
# Wordnet is a package in NLTK
# Wordnet is a popular lexical resource, built as a collection of sets of synonyms, aka synsets
# Can invoke Wordnet to retrieve synonyms, antonyms, definitions and examples

#import wordnet
from nltk.corpus import wordnet

#obtain a definition and example for "pain"
synsets = wordnet.synsets("money")
#synsets
print(synsets[0].definition())
print(synsets[0].examples())

#obtain synonyms
synonyms = [] #declare an empty list of synonyms

for syn in wordnet.synsets("train"):       # get all synsets for "tank"
    for lemma in syn.lemmas():            # obtain a lemma from each synset
        synonyms.append(lemma.name())     # populate the list of synonyms
print(set(synonyms))

#obtain antonyms
antonyms = []  #declare an empty list of synonyms
for syn in wordnet.synsets("thin"):
    for l in syn.lemmas():
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
print(set(antonyms))

### Named Entity Recognition
# NER is a common NLP task
# Normal entity breakdown: person, geolocation, organization, conceptual work, event, currency, time, date, etc.
# NLTK's NER is embedded into a pre-processing function which also performs POS tagging and "chunking" (a form of shallow parsing)"

#declare an input text
txt = """The present mayor is Bill de Blasio, the first Democrat since 1993.[572] He was elected in 2013 with over 73% of the vote, and assumed office on January 1, 2014. The Democratic Party holds the majority of public offices. As of April 2016, 69% of registered voters in the city are Democrats and 10% are Republicans.[573] New York City has not been carried by a Republican in a statewide or presidential election since President Calvin Coolidge won the five boroughs in 1924. In 2012, Democrat Barack Obama became the first presidential candidate of any party to receive more than 80% of the overall vote in New York City, sweeping all five boroughs. Party platforms center on affordable housing, education, and economic development, and labor politics are of importance in the city."""

#tokenize, pos-tag and NER-tag input
tokens = nltk.word_tokenize(txt)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)
print(entities)
