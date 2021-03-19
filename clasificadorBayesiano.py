from collections import Counter
import re
import copy

def TranfSentence(s):
  s = s.lower()
  result = re.sub(r'[^A-Za-z0-9]', ' ', s)
  return result

def Group_list(lst): 
  return list(zip(Counter(lst).keys(), Counter(lst).values())) 

def CreateDict(Ps, Ns, templateDict):
  #si no copio la lista utilizando este metodo se linkean para siempre
  Pwords = copy.copy(templateDict)
  Nwords = copy.copy(templateDict)
  
  listPWords = Ps.split()
  listNWords = Ns.split()
  
  groupedPWords = Group_list(listPWords)
  groupedNWords = Group_list(listNWords)

  for word in groupedPWords:
      Pwords[word[0]] = word[1]
  for word in groupedNWords:
      Nwords[word[0]] = word[1]
      
  return Pwords, Nwords, len(listPWords), len(listNWords)

def DataFromTXT():
  templateDict = {}
  positiveSentences = ''
  negativeSentences = ''
  countPositiveDocs = 0
  countNegativeDocs = 0
  
  with open('datos.txt') as f:
    lines = f.readlines()
    
    for sentence in lines:
      sentence = TranfSentence(sentence)
      words = sentence.split()
      for word in words:
        templateDict[word] = 0

    for sentence in lines:
      
      if (sentence.find('[+]') != -1):
        sentence = TranfSentence(sentence)
        positiveSentences = positiveSentences + sentence
        countPositiveDocs += 1
      elif (sentence.find('[-]') != -1):
        sentence = TranfSentence(sentence)
        negativeSentences = negativeSentences + sentence
        countNegativeDocs += 1
    
    positiveWords, negativeWords, countPositiveWords, countNegativeWords = CreateDict(positiveSentences, negativeSentences, templateDict)
    diffWords = len(templateDict)
    totalDocs = countPositiveDocs + countNegativeDocs
    probClasePositiva = countPositiveDocs / totalDocs
    probClaseNegativa = countNegativeDocs / totalDocs
    
  return positiveWords, negativeWords, diffWords, probClasePositiva, probClaseNegativa, countPositiveWords, countNegativeWords
      
def ConditionalProb(pW, nW, countPositiveWords, countNegativeWords, diffWords):
  #positive and negative words
  pcw = {}
  ncw = {}
  
  for word in pW:
    pcw[word] = (pW[word] + 1) / (countPositiveWords + diffWords)
  
  for word in nW:
    ncw[word] = (nW[word] + 1) / (countNegativeWords + diffWords)
  
  return pcw, ncw

def AssignClass(s, positiveConditionalProb, negativeConditionalProb, probClasePositiva, probClaseNegativa):
  probPositive = probClasePositiva
  probNegative = probClaseNegativa
  
  for word in s:
    if word in positiveConditionalProb:
      probPositive *= positiveConditionalProb[word]
    if word in negativeConditionalProb:
      probNegative *= negativeConditionalProb[word]

  if probPositive > probNegative:
    return 0, probPositive, probNegative
  else:
    return 1, probPositive, probNegative
  
def ClasificadorBayesiano():
  
  positiveWords, negativeWords, diffWords, probClasePositiva, probClaseNegativa, countPositiveWords, countNegativeWords = DataFromTXT()

  positiveConditionalProb, negativeConditionalProb = ConditionalProb(positiveWords, negativeWords, countPositiveWords, countNegativeWords, diffWords)
  
  sentence = input('Introduce la oración para determinar su clase:\n')
  s = TranfSentence(sentence).split()

  res, probPositive, probNegative = AssignClass(s, positiveConditionalProb, negativeConditionalProb, probClasePositiva, probClaseNegativa)
  
  resString = f"""----------------------------------------------------------
La probabilidad de que sea POSITIVA es: {probPositive}
La probabilidad de que sea NEGATIVA es: {probNegative}
----------------------------------------------------------"""
  
  if res == 0:
    print(f'La oración <{sentence}> es POSITIVA.')
  elif res == 1:
    print(f'La oración <{sentence}> es NEGATIVA.')
  else:
    print('Error en la operación.')

  print(resString)
  
ClasificadorBayesiano()