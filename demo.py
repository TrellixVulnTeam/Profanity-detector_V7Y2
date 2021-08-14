from ParentalControl.core import detection
import time
import pdb

sampleDatas = [{
   "videoId": "C7Gw--6t3s4",
   "data": {
       "title": "Watch Top Moments From The First Presidential Debate | NBC News bitch",
       "description": "Watch highlights from the first presidential debate of 2020 as President Donald Trump and Democratic nominee Joe Biden face off on coronavirus, the Supreme Court and more...",
       "channelTitle": "NBC News",
       "category": "News & Politics",
       "tags": [
           "Politics",
           "2020 Election",
           "Decision 2020",
           "NBC News"
       ]
   }
},
{
   "videoId": "_rnbd6u6gPw",
   "data": {
       "title": "Top 5 LARGEST Flash Floods (caught on video) and sex and fucking",
       "description": "Flash floods are a powerful force of nature! Today we're doing the top five largest flash floods caught on video...",
       "channelTitle": "Top Fives",
       "category": "Entertainment",
       "tags": [
           "top five videos",
           "nature videos",
           "nature clips",
           "rivers",
           "sex",
           "school fight"
       ]
   }
}]


output = {
  "success": True,
  "error": None,
  "data":[] 
}

if __name__ == "__main__":
    algo = detection()
    start_time = time.time()
    data = []
    error_ = []
    for sampleData in sampleDatas:
        res_ = {"videoId": "","models": {}}
        try:
            res = algo(sampleData['data'])
            res_["videoId"] = sampleData["videoId"]
            res_["models"].update(res)
            data.append(res_)
            success = True
        except BaseException as error:
            error_.append(error)
            success = False
            data.append(res_)
    output["success"] = success
    output["error"]=error_
    output["data"] = data
    
    print("--- %s seconds ---" % (time.time() - start_time))
    print(output)