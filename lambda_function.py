import string
import json
import os
import time
from ParentalControl.core import detection
import tarfile
import urllib.request
import boto3
algo = detection()
# if not os.path.isdir("/tmp/en_core_web_sm-2.0.0"):
#     urllib.request.urlretrieve(
#         "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz",
#         "/tmp/en_core_web_sm-2.3.1.tar.gz",
#     )
#     # Extract all data
#     with open("/tmp/en_core_web_sm-2.3.1.tar.gz", "rb") as f:
#         t = tarfile.open(fileobj=f)
#         t.extractall(path="/tmp/")
#     # Cleanup
#     os.remove("/tmp/en_core_web_sm-2.3.1.tar.gz")
# nlp = spacy.load("/tmp/en_core_web_sm-2.3.1/en_core_web_sm/en_core_web_sm-2.3.1")
def lambda_handler(event,context):
	output = {
	"success": True,
	"error": None,
	"data":[] 
	}
	print(event)
    
	req = event
	req = json.loads(json.dumps(req))
	sampleDatas = list(req)
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
		    error_.append(json.loads(json.dumps(str(error))))
		    success = False
		    data.append(res_)
		output["success"] = success
		output["error"]=error_
		output["data"] = data
	# pdb.set_trace()
	return {
	'statusCode':200,
	'body':output#json.dumps(output)
	}

