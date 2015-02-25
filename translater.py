#!/usr/bin/env python
# CS124 Homework 6 Translate
# David Beam (dbeam@stanford.edu) Mark Schramm (mschramm@stanford.edu)

import itertools as it
import re

def loadList(file_name):
    """Loads text files as lists of lines. Used in evaluation."""
    with open(file_name) as f:
        l = [line.strip() for line in f]
    return l

def train():
	englishList = loadList("es-en/train/europarl-v7.es-en.en")
	spanishList = loadList("es-en/train/europarl-v7.es-en.es")
	print englishList[0]
	print spanishList[0]
train()
