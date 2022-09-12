from mimetypes import init

import sys
import typing
import unicodedata
from collections import defaultdict


class SimpleTokenizer:

  def __init__(self) -> None:
    pass

  unicodeCategory = defaultdict(list)
  for c in map(chr, range(sys.maxunicode + 1)):
    unicodeCategory[unicodedata.category(c)].append(c)

  allowedCharacters = set()

  allowedCategories = ["Lu", "Ll", "Nd"]
  for category in allowedCategories:
    for item in unicodeCategory[category]:
      allowedCharacters.add(item)
 
  def getTokens(self, value) -> typing.List[str]:
    index = 0
    tokenCharacters = []
    tokens = []

    for character in value:
    #while index < len(value):
      #character = value[index]
      if character in self.allowedCharacters:
        tokenCharacters.append(character)
      else:
        success, token = self.generateToken(tokenCharacters)
        if success: 
          tokens.append(token)
        tokenCharacters.clear()
      index += 1

    if len(tokenCharacters) > 0:
      success, token = self.generateToken(tokenCharacters)
      if success:
        tokens.append(token)

    return tokens

  def generateToken(self, characters) -> typing.Tuple[bool, str]:
    token = ""
    for character in characters:
      token += character

    success = True if len(token) > 0 else False
    return success, token












