
class Vertex():
  def __init__(self, features) -> None:
    self.features = features

class Features():
  def __init__(self, textFeatures = [], intFeatures = [], floatFeatures = [], dateTimeFeatures = []) -> None:
    self.textFeatures = textFeatures
    self.intFeatures = intFeatures
    self.floatFeatures = floatFeatures
    self.dateTimeFeatures = dateTimeFeatures

  def getFeatureArray(self):
    features = self.textFeatures + self.intFeatures + self.floatFeatures + self.dateTimeFeatures
    return features

  def getResolvableTokens(self, tokenizer):
    features = self.getFeatureArray()
    
    resolvableTokens = []

    for feature in features:
      if feature.resolvable:
        resolvableTokens = resolvableTokens + tokenizer.getTokens(f"{feature.title} {feature.value}")

    return resolvableTokens










class Feature():
  def __init__(self, title, value, description = "", searchable = True, resolvable = True) -> None:
    self.title = title
    self.value = value
    self.description = description
    self.searchable = searchable
    self.resolvable = resolvable




