# import pandas as pd
# import numpy as np
from .profanity import predict, predict_prob, YoutubeProfanity
from .keywordYT import KeyWord
import json
class detection:
    def __init__(self):
      self.profaneProb = 0.0
      self.YoutubeProfanity = YoutubeProfanity()
      self.KeyWord = KeyWord()

    def checkAge(self):
        # pdb.set_trace()
        if self.Des["Mature"]==True:
            self.reason = "+18 Age"
            return True,100,self.reason
        try:
            if self.Des['ParentalWarning']=='True':
                reason = "+18 Age"
                return True,100,reason
        except:
            pass
        
        return False,000,None
        
    def checkCatg(self,category):
        # pdb.set_trace()
        if category in self.Des['category']:
            reason = 'Political'
            return True,100, reason
        else:
            return False,000,None
        
            
    def __call__(self,Des):
        # pdb.set_trace()
        self.Des = Des
        score = 0
        statusKEY,probKEY,reasonKEY = self.KeyWord(Des)
        statusPROF,probPROF,reasonPROF = self.YoutubeProfanity(Des)
        # statusCAT,probCAT,reasonCAT = self.checkCatg(category)
        # statusAGE,probAGE,reasonAGE = self.checkAge()
        res = {
            # "category":{
            # "precision":0,
            # "tag":None
            # },
            "profanity":{
            "precision":0,
            "tag":None
            },
            "keywords":{
            "precision":0,
            "tag":None
            },
            # 'age':{
            # 'precision':0,
            # 'tag':None
            # }
        }
        # if ((statusCAT==True)):
        #     # return True,100,'General News'
        #     res["category"]["precision"] = 100
        #     res["category"]["tag"] = "General News"

        # if (statusAGE==True):
        #     # return True,100,'+18'
        #     res['age']['precision'] = 100
        #     res['age']['tag'] = '+18'
        if (statusPROF==True):
            # return True,probPROF,reasonPROF
            # print("lololololol->")
            res["profanity"]["precision"] =int(probPROF*100)
            res["profanity"]["tag"] = reasonPROF

        if (statusKEY==True):
            # return True,100,reasonKEY
            res["keywords"]["precision"] = 100
            res["keywords"]["tag"] = reasonKEY
        # print(type(str(res)))
        return res
        
