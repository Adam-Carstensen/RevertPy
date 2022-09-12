import math

class CosineSimilarity():

  @staticmethod
  def getVectorCosineSimilarity(vector, secondVector):
    squaredVector = []
    for value in vector:
      squaredVector.append(math.pow(value, 2))
    sumSquaredVector = sum(squaredVector)
    vectorMagnitude = math.sqrt(sumSquaredVector)

    squaredSecondVector = []
    for value in secondVector:
      squaredSecondVector.append(math.pow(value, 2))
    sumSquaredSecondVector = sum(squaredSecondVector)
    secondVectorMagnitude = math.sqrt(sumSquaredSecondVector)

    vectorProducts = []
    for i in range(len(vector)):
      if (i < len(vector) and i < len(secondVector)):
        vectorProducts.append(vector[i] * secondVector[i])

    dotProduct = sum(vectorProducts)

    magnitudeProduct = vectorMagnitude * secondVectorMagnitude

    return dotProduct / magnitudeProduct










        
