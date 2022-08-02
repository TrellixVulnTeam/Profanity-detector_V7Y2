Profanity Detector in YouTube videos

Folders
```
1. keywordYT
	a. keywordYT.py
	b. preprocess.py
2. profanity
	a. profanity.py
	b. preprocess.py
3. core.py
```

# preprocess.py

class preprocess()

	Goal   : To clean sentences used for various tasks and function.	
	Input  : Takes string / sentences.
	Return : cleaned up sentences.

class preprocessK()

	Goal   : To clean tags used for searching the YouTube videos. Extracted from YT html.
	Input  : Takes list of words / sentences.
	Return :words



This file takes up the sentences, and cleans it up accordingly. Has following functions ..
1. Remove Urls
2. Remove Numericals
3. Remove ASCII
etc




The example data format is json, similar to the following


```
{
   "videoId": "_rnbd6u6gPw",
   "data": {
       "title": "Top 5 LARGEST Flash Floods (caught on video) fuck bitch",
       "description": "Flash floods are a powerful force of nature! Today we're doing the top five largest flash floods caught on video...",
       "channelTitle": "Top Fives",
       "category": "Entertainment",
       "tags": [
           "top five videos",
           "nature videos",
           "nature clips",
           "rivers",
           "sex"
       ]
   }
}

```
### output [expected]

```
{
  "statusCode": 200,
  "body": {
    "success": true,
    "error": [],
    "data": [
      {
        "videoId": "_rnbd6u6gPw",
        "models": {
          "profanity": {
            "precision": 96,
            "tag": "Profane Video"
          },
          "keywords": {
            "precision": 100,
            "tag": [
              "Disasters",
              "Violence",
              "Mature"
            ]
          }
        }
      }
    ]
  }
}

```

### TODO
- [ ] Spell Correction  

*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*<>*

### Libraries in Layers
We use five layers and distributed as shown below.
If file.zip less than <10, upload via the gui directly.
else upload via s3 bucket.

1.  Numpy and Scipy [available on aws lambda]
2.  Spacy without numpy [custom]
3.  textsearch==0.0.17  [custom]
    contractions==0.0.25
    joblib==0.14.1
    inflect==4.1.0
    pyahocorasick==1.4.0
    Unidecode==1.1.1
4.  boto3==1.16.25       [custom]
5.  scikit-learn==0.23.2 [custom]

### Initial steps:
step 1 : cd .aws [location where you have installed ]
step 2 : open -a TextEdit credentials [note the credentials for the account you work on]
step 3 : aws configure [answer the credentials from step 4]

### Library Preparation:
prerequiste : Docker|conda|internet.
step 1 : mkdir dellib [empty folder]
step 2 : create requirements.txt [according to libraries you want in a layer]
step 3 :

```
run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.7 pip install -r requirements.txt --no-deps -t python

```
```
zip -r9 layerName.zip .
```
```
python uploads3.py -lib sklearn.zip -des /Users/nilesh.pandey/Desktop/dellib/
```

step 4 : Upload all layers, check if the zip is less than 60mb, if not reduce the number of libraries in it.

### Machine learning Models:

Machine learning models could go up as high as in GBs.
If the machine learning model is big enough that It can be fitted in aws lambda, then we upload the machine learning model on the s3, and load it once every now and then.

step 1 : Upload ML model using : PS : Read the code to uncomment and comment func.
```
python uploads3.py
```
step 2 : Include uploads3.py, which has function to retrive files from s3 bucket.
step 3 : Load the model.

### S3 permission:
step 1 : click on permission > execution role > policies > |create poilcy| > |json|


```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3ActionsRestrictedConditionalList",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::S3_Bucket*/*",
                "arn:aws:s3:::S3_Bucket*"
            ]
        },
        {
            "Sid": "S3ActionsRestrictedConditionalRead",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::S3_Bucket*/*"
            ]
        }
    ]
}
```
This permission will enable s3upload to read models from s3 bucket.

step 2 : click on permission > execution role > |Attach policies| > |search and attach|

### Deploy

### References:

1. https://xoelop.medium.com/deploying-big-spacy-nlp-models-on-aws-lambda-s3-2857bfc143ba
1. https://github.com/xoelop/nlp-lambda-example

2. https://github.com/theashworld/nlp_on_aws_lambda

3. https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz

4. https://gist.githubusercontent.com/qtangs/69e0db74313e8b97708b88f9a7db9bfb/raw/3003cd7084deff8d010c985fd1a574c2ec8580f3/get_layer_packages.sh

5. example for aws layer from cmd https://gist.github.com/haranjackson/50748c9f1e40940336e730a1783f0dd8



