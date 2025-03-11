import nltk
from nltk.corpus import treebank
from pprint import pprint
#------------------------------------------------------------------------------
# progressive participles
sentence = """She was hiking."""
tokens = nltk.word_tokenize(sentence)
t = treebank._parse(sentence)
t.pretty_print()
t.pprint()
#(S (NP She)
#   (VP was
#       (VP hiking))
#.)
#------------------------------------------------------------------------------
# deverbal nouns (aka gerunds)
sentence = """She loves hiking."""
#(S (NP She)
#   (VP loves
#       (VP hiking))
#.)
#------------------------------------------------------------------------------
# deverbal adjectives
sentence = """This homework is exciting."""
#(S (NP This homework)
#   (VP is
#       (ADJP exciting))
#.)
#------------------------------------------------------------------------------
# deverbal undecidables
sentence = """These are hiking boots."""
#(S (NP These)
#   (VP are
#       (VP hiking
#           (NP boots)))
#.)
#------------------------------------------------------------------------------
