#!/usr/bin/env python
# coding: utf-8

"""Estonian Spelling Corrector in Python 3; 
adapted from Peter Norvig's English Spelling Corrector; 
see http://norvig.com/spell-correct.html

Original copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php
"""

################ Spelling Corrector for Estonian
import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('suur.txt').read())) # 'suur' means 'big' XD

# Probability of 'word'
def P(word, N=sum(WORDS.values())): 
    return WORDS[word] / N

# Most probable spelling correction for 'word'
def correction(word): 
    return max(candidates(word), key=P)

# Generate possible spelling corrections for 'word'
def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

# The subset of `words` that appear in the dictionary of WORDS.
def known(words): 
    return set(w for w in words if w in WORDS)

# All edits that are one edit away from `word`.
def edits1(word):
    # list of letters needed for replaces and inserts
    letters    = 'aäbdefghijklmnoöõprsštuüvzž'
    # create a list of tuples each containing two halves of the word, split at a different letter
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    # for each pair of splits, try deleting, transposing, replacing, and inserting
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    # return all the unique strings created in the process
    return set(deletes + transposes + replaces + inserts)

# All edits that are two edits away from `word`.
def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

################ Test Code 

def unit_tests():
    assert correction('urija') == 'uurija'              # insert
    assert correction('hekpama') == 'hakkama'           # replace 2
    assert correction('heppama') == 'hüppama'           # replace
    assert correction('normalslt') == 'normaalselt'     # insert 2
    assert correction('valimiised') == 'valimised'      # delete
    assert correction('paeme') == 'peame'               # transpose
    assert correction('normalaseelt') == 'normaalselt'  # transpose + delete
    assert correction('sõna') == 'sõna'                 # known
    assert correction('kuldrenett') == 'kuldrenett'     # unknown
    assert words('See on KATSE.') == ['see', 'on', 'katse']
    assert Counter(words('See on küll KATSE. 123; KATSE on see küll.')) == (
           Counter({'see': 2, 'on': 2, 'küll': 2, 'katse': 2, '123': 1}))
    assert len(WORDS) == 170420 # English was 32192
    assert sum(WORDS.values()) == 1115504 # English was 1115504
    assert WORDS.most_common(10) == [('on', 29923),
 ('ja', 29138),
 ('et', 13428),
 ('ei', 12907),
 ('kui', 9543),
 ('ka', 7368),
 ('ta', 6367),
 ('see', 6293),
 ('oma', 5664),
 ('oli', 5561)]
    assert WORDS['kui'] == 9543
    assert P('kuldrenett') == 0
    assert 0.008 < P('kui') < 0.009
    return 'unit_tests pass'

print(unit_tests())
display_words = ['urija','paeme','valimiised', 'hekkama']
for item in display_words:
    print("{} => {}".format(item, correction(item)))