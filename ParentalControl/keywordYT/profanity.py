import numpy as np
import joblib
# from .preprocess import preprocess,preprocessK
# import pdb

vectorizer = joblib.load('./ParentalControl/profanity/data/vectorizer.joblib')
model = joblib.load('./ParentalControl/profanity/data/model.joblib')

def _get_profane_prob(prob):
  return prob[1]

def predict(texts):
  return model.predict(vectorizer.transform(texts))

def predict_prob(texts):
  return np.apply_along_axis(_get_profane_prob, 1, model.predict_proba(vectorizer.transform(texts)))


class YoutubeProfanity():
	def __init__(self):
		self.vectorizer = joblib.load('./ParentalControl/profanity/data/vectorizer.joblib')
		self.model = joblib.load('./ParentalControl/profanity/data/model.joblib')
		# self.preprocess = preprocess()


	def _get_profane_prob(self,prob):
		return prob[1]

	def predict(self,texts):
		return model.predict(vectorizer.transform(texts))

	def predict_prob(self,texts):
		return np.apply_along_axis(_get_profane_prob, 1, model.predict_proba(vectorizer.transform(texts)))

	def checkProfanity(self,Thresh=0.30):
		porbDes = 0.0
		try:
			final = YoutubeProfanity.brk(self.Des["description"])
			for text in final:
				porbDes += self.predict_prob([text])  
		# try:   
			if self.predict_prob([self.Des["title"]])>Thresh:
			    self.profaneProb = self.predict_prob([self.Des["title"]])
			    self.reason = 'Profane Video'
			    return True
			elif porbDes/len(final)>Thresh:
			    self.profaneProb = porbDes/len(final)
			    self.reason = 'Profane Video'
			    return True
			    
			else:
			    return False
		except:
			return False
        
	def checkSubs(self,ThreshSubs=0.10):        
		porbSubs = 0
		try:
			tempSubs = self.preprocess(''.join((self.Des['subs'])))
			final = YoutubeProfanity.brk(tempSubs)
			for text in final:
				porbSubs += self.predict_prob([''.join(text)])

			if porbSubs/len(final)>ThreshSubs:
				self.profaneProb = porbSubs/len(final)
				self.reason = "Profane Video"
				return True
		except:
			return False
	@staticmethod
	def chunkstring(strings, length):
	    return (strings[0+i:length+i] for i in range(0, len(strings), length))
	@staticmethod
	def brk(string,length=200):        
	    res = []
	    lines = (i.strip() for i in string.splitlines())
	    for line in lines:
	        for chunk in YoutubeProfanity.chunkstring(string, length):
	            res.append(chunk)
	    return res


	def __call__(self,des):
		# pdb.set_trace()
		self.Des = des
		# if (self.checkSubs(ThreshSubs=0.60)==True):
		#     return True,self.profaneProb,self.reason
		if (self.checkProfanity(Thresh=0.60)==True):
		    return True,self.profaneProb,self.reason
		else:
		    return False,000,None



