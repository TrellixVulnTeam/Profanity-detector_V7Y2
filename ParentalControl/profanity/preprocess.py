import re, string, unicodedata
import contractions
import inflect
from typing import List
import spacy
from spacy.tokens import Doc
import json
import os
import tarfile
import urllib.request

class preprocess():
    def __init__(self):
        if not os.path.isdir("/tmp/en_core_web_sm-2.0.0"):
            urllib.request.urlretrieve(
                "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz",
                "/tmp/en_core_web_sm-2.3.1.tar.gz",
            )
            # Extract all data
            with open("/tmp/en_core_web_sm-2.3.1.tar.gz", "rb") as f:
                t = tarfile.open(fileobj=f)
                t.extractall(path="/tmp/")
            # Cleanup
            os.remove("/tmp/en_core_web_sm-2.3.1.tar.gz")
        self.model = spacy.load("/tmp/en_core_web_sm-2.3.1/en_core_web_sm/en_core_web_sm-2.3.1")
    
    def remove_stopwords(self,tokens):
        return [token for token in tokens if not token.is_stop]

    def remove_unwanted_tokens(self,tokens):
        tokens = [
            token
            for token in tokens
            if not (
                token.is_punct or token.is_space or token.is_quote or token.is_bracket
            )
        ]
        return [token for token in tokens if token.text.strip() != ""]
    
    def lemmatize_words(self,tokens):
        return " ".join([token.lemma_ for token in tokens])

    def remove_URL(self,sample):
        """Remove URLs from a sample string"""
        return re.sub(r"http\S+", "", sample)

    def remove_non_ascii(self,words):
        """Remove non-ASCII characters """
        return unicodedata.normalize('NFKD', words).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def to_lowercase(self,words):
        """Convert all characters to lowercase"""
        return words.lower()

    def remove_punctuation(self,words):
        """Remove punctuation"""
        return words.translate(str.maketrans('', '', string.punctuation))

    def remove_numbers(self,tokens):
        """Remove all interger"""
        return [token for token in tokens if not (token.like_num or token.is_currency)]
    
    @staticmethod
    def download_spacy_model(model="en_core_web_sm"):
        print(f"Downloading spaCy model {model}")
        spacy.cli.download(model)
        print(f"Finished downloading model")
        
    def __call__(self,sample):
        
        text = self.remove_URL(sample)
        doc = self.model(text)
#         return self.remove_numbers(doc)
        return self.remove_non_ascii(self.lemmatize_words(self.remove_unwanted_tokens(self.remove_stopwords(self.remove_numbers(doc)))))


class preprocessK():
    def __init__(self,path=None):
        '''
        Clean up the keyword tag from youtube 
        '''
        self.stopwords = preprocessK.load_stopwords(path)
    
    def remove_non_ascii(self,words):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

    def to_lowercase(self,words):
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words

    def remove_punctuation(self,words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def replace_numbers(self,words):
        """Replace all interger occurrences in list of tokenized words with textual representation"""
        p = inflect.engine()
        new_words = []
        for word in words:
            if word.isdigit():
                new_word = p.number_to_words(word)
                new_words.append(new_word)
            else:
                new_words.append(word)
        return new_words

    @staticmethod
    def remove_stopwords(words,stopwords):
        """Remove stop words from list of tokenized words"""
        new_words = []
        for word in words:
            if word not in stopwords:
                new_words.append(word)
        return new_words
    
    @staticmethod
    def load_stopwords(path=None):
        if path==None:
            with open('./ParentalControl/keywordYT/data/stopwords.json', 'r') as fp:
                temp = json.load(fp)
        else:
            with open(self.path, 'r') as fp:
                temp = json.load(fp)            
        return temp

    def normalize(self,words):
        words = self.remove_non_ascii(words)
        words = self.to_lowercase(words)
        words = self.remove_punctuation(words)
        words = self.replace_numbers(words)
        words = preprocessK.remove_stopwords(words,self.stopwords)
        return words
    def __call__(self,word):
        return self.normalize(word)
if __name__ == "__main__":
    p = preprocess()
    sample = "Blood test for Down's syndrome hailed  http://bbc.in/1BO3eWQ Search Results Web results😋"               

    words = p(sample)
    print(words)