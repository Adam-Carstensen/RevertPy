from nltk.tokenize import NLTKWordTokenizer

import sys
from typing import List, Tuple
import unicodedata
from collections import defaultdict


class NltkTokenizer():
  def __init__(self) -> None:
    self.tokenizer = NLTKWordTokenizer()   
  
  def getTokens(self, value) -> List[str]:
    tokens = self.tokenizer.tokenize(value)

    return tokens













