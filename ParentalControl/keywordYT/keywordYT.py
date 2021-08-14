import json
from textsearch import TextSearch
from .preprocess import preprocess,preprocessK
import pdb

class KeyWord():
    def __init__(self,path=None):
        self.path = path
        self.KeyWords = self.load()
        self.ts = TextSearch(case="ignore", returns="match")
        for x,y in self.KeyWords.items():
            self.ts.add(y)
        self.res = list()
        self.preprocess = preprocess()
        self.preprocessK = preprocessK()



    def checKeyWrds(self):
        # pdb.set_trace()
        self.reason = set()
        if len(self.temp_kwd)>=1 and len(self.temp_title)>=1:
            res1 = set(self.ts.findall(r'{}'.format(self.temp_kwd)))
            res2 = set(self.ts.findall(r'{}'.format(self.temp_title)))
            res3 = set(self.ts.findall(r'{}'.format(self.temp_cat)))
            if(len(res1)!=0) and (len(res2)!=0):
                temp = self.getKey(res1)
                temp.update(self.getKey(res2))
                temp.update(self.getKey(res3))
                self.reason.update(temp)
                return True
            elif(len(res1)!=0):
                self.reason.update(self.getKey(res1))
                return True
            elif(len(res2)!=0):
                self.reason.update(self.getKey(res2))
                return True
            elif(len(res3)!=0):
                self.reason.update(self.getKey(res3))
                return True

        if len(self.temp_kwd)>=1:
            res = set(self.ts.findall(r'{}'.format(self.temp_kwd)))
            if(len(res)!=0):
                self.reason.update(self.getKey(res))
                return True
        if len(self.temp_title)>=1:
            res = set(self.ts.findall(r'{}'.format(self.temp_title)))
            if(len(res)!=0):
                self.reason.update(self.getKey(res))
                return True
        if len(self.temp_cat)>=1:
            res = set(self.ts.findall(r'{}'.format(self.temp_cat)))
            if(len(res)!=0):
                self.reason.update(self.getKey(res))
                return True
        else:
            return False



    def __call__(self,des):
        self.Des = des
        # pdb.set_trace()
        if isinstance(des['title'], str):
            self.temp_title=self.preprocess(des['title'].lower())
        if isinstance(des['tags'], str):
            self.temp_kwd=list(set(self.preprocessK(des['tags'].lower().split()[2:-1])))
        elif isinstance(des['tags'], list):
            self.temp_kwd=list(set(self.preprocessK([x.lower() for x in des['tags']])))
        if isinstance(des['category'],str):
            self.temp_cat=list(set(self.preprocessK(des['category'].lower().split())))
        elif isinstance(des['category'], list):
            self.temp_cat=list(set(self.preprocessK([x.lower() for x in des['category']])))
        # pdb.set_trace()
        if self.checKeyWrds()==True:
            res = [str(words).replace("'", '"') for words in self.reason]
            # print(res)
            return True,100,list(res)
        else:
            return False,000,None


    def load(self):
        if self.path==None:
            with open('./ParentalControl/keywordYT/data/keyword.json', 'r') as fp:
                temp = json.load(fp)
        else:
            with open(self.path, 'r') as fp:
                temp = json.load(fp)            
        return temp

    def getKey(self,tex):
        res = set()
        for obj in self.KeyWords.items():
            a_set = tex
            b_set = set(obj[1])
            if len(a_set.intersection(b_set)) > 0:
                res.add(obj[0])
        return res;
            

