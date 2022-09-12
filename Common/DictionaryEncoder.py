from json import JSONEncoder

class DictionaryEncoder(JSONEncoder):
  def default(self, o):
    return o.__dict__
