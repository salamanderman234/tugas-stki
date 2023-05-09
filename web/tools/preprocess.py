from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import re
import string
from nltk import word_tokenize

class Preprocessor :
    def __init__(self, lang: str = "eng") -> None:
        if lang == "id":
            self.lang = "id"
            self.stopwords = set(stopwords.words("indonesian"))
            self.stemmer = StemmerFactory().create_stemmer()
        else:
            self.lang = "eng"
            self.stopwords = set(stopwords.words("english"))
            self.stemmer = WordNetLemmatizer()

    def __clean(self, text: str) -> str:
        steps = [
            lambda text: text.lower(),
            lambda text: text.strip(),
            # remove special char
            lambda text: text.translate(str.maketrans("","",string.punctuation)),
            # remove number
            lambda text: re.sub(r'\d+',' ', text),
            lambda text: re.sub(r'\b[a-zA-Z]\b',' ', text),
            lambda text: re.sub(r' +', ' ', text),
        ]

        new_str = text
        for step in steps:
            new_str = step(new_str)

        return new_str

    def __tokenize(self, text: str) -> list:
        tokens = word_tokenize(text)
        return tokens


    def __stopwords(self, tokens: list) -> list:
        tokens = [token for token in tokens if token not in self.stopwords]
        return tokens
    
    def __stem(self, tokens: list) -> list:
        tokens = [ self.stemmer.stem(token) if self.lang == "id" else self.stemmer.lemmatize(token) for token in tokens]
        return tokens
    
    def __dist(self, tokens: list) -> list :
        return FreqDist(tokens).most_common()

    def process(self, text: str) -> list:
        cleaned_text = self.__clean(text=text)
        tokens = self.__tokenize(cleaned_text)
        tokens = self.__stopwords(tokens)
        tokens = self.__stem(tokens)
        freq_dist = self.__dist(tokens)

        return [{"term" : token[0], "freq": token[1]} for token in freq_dist]
