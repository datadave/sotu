# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# Script for reading in SOTU speeches checking against a provided word list and providing a frequency output

import json
import sys
import nltk
import re
from sys import stdout

# <codecell>

## Import entire raw text
f = open('./inputs/stateoftheunion1790-2012.txt')
text = f.read()

## split the text into speeches
speeches = text.split('***')

# <codecell>

# Read in a dictionary file of words
thedict = open('./dictionary/economicjusticedictionary_011614.txt').readlines()

# take out newlines
thedict = [line.strip() for line in thedict]

# take the dictionary to define search and avoid phrases
# Note this assumes each line has comma separated values "target,avoid"
searchphrases=[]
avoidphrases=[]
for line in thedict:
    j = line.split(',')
    searchphrases.append(j[0])
    avoidphrases.append(j[1]) 

# <codecell>

# Define the range of speeches to evaluate
startrange=109 
endrange=222

# <codecell>

templist=[] # for bug checking the avoidword system
outlist=[] # Output of all variables in serial format
speechlist=[] # List of individual speeches, dates, speakers, word totals
target=[] # Target search word
avoid=[] # Word/phrase to avoid when searching for target (0 if none)
context=[] # Text surrounding target

# <codecell>

# Create a list with speechnum, date, speaker, totalwords
s=[]
w=[]
for speechnum in range(startrange,endrange+1):
    s = speeches[speechnum]
    w = nltk.Text(nltk.word_tokenize(s.lower().replace('.', ' ')))
    speechlist.append((speechnum,s.split('\n')[4],s.split('\n')[3],len(w)))

# <codecell>

# FIND WORD OCCURRENCES IN SELECTED SPEECHES
# Populate data frame with speech, date, president, character index, targetword, context

for speechnum in range(startrange,endrange+1):
    s = speeches[speechnum] # set "s" as the speech of choice
    # Iterate over words
    for (target,avoid) in zip(searchphrases,avoidphrases):  # The dictionary list includes target and avoidance pairs
            for m in re.finditer(re.escape(target),s,re.I): # gather 2 hundred characters before and after a target
                q = s[m.start()-200:m.start()+200].split()
                context = ("... "+' '.join(q[1:(len(q)-1)])+" ...") # capture the context around the target as a string
                if avoid != '0': # If there's an 'avoid' word then:
                    if not re.search(avoid,s[m.start()-200:m.start()+200],re.I): # if the word isn't nearby:
                        templist.append((speechnum,m.start(),m.group(),'avoidsafe')) # then count the word
                        outlist.append((speechnum,s.split('\n')[4],s.split('\n')[3],m.start(),target,speechlist[speechnum-startrange][3],context))
                    else: # just for bug checking
                        templist.append((speechnum,m.start(),m.group(),'avoidfail')) # if the word is nearby, then don't count it.
                else: # Do the below if there's no avoid word, i.e. if "avoid" = '0'
                    templist.append((speechnum,m.start(),m.group()))
                    outlist.append((speechnum,s.split('\n')[4],s.split('\n')[3],m.start(),target,speechlist[speechnum-startrange][3],context))
                    # 4th line is date, 3rd line is president

# <codecell>

# Output Summaries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# <codecell>

# Create a dataframe
outarray = np.array(outlist).reshape(-1,7)
df = pd.DataFrame(outarray)
df.columns = ['speech','date','president','charindex','target','wordcount','context']

# <codecell>

# Convert the date to datetime
df['date'] = pd.to_datetime(df['date'])

# <codecell>

# Draw a quick table to verify that our dataframe looks correct
df[0:5] 

# <codecell>

# List of scores value count -- scores per date
svc = df.date.value_counts()
svc = pd.DataFrame(svc)
svc = svc.sort()


# <headingcell level=3>

# File Export

# <codecell>

# Output File as date-time-stamped csv
import datetime
x = datetime.datetime.now().strftime('%m-%d-%y_%H%M')
df.to_csv("./outputs/output_"+x+".csv")

# <codecell>

# Output Sample File as JSON
# rows = np.random.choice(df.index.values, 10)
# sampled_df = df.ix[rows]

# <codecell>

# sampled_df.to_json('sotu.json',orient='values')
# sotu = {'text': latetext, 'speechTitles': speechTitles, 'speechStarts': speechStarts, 'fKeys': fKeys, 'fValues': fValues}
# json.dump(sotu, open('webpage/sotu.json', 'wb'))

