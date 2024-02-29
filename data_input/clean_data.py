import pandas as pd
import re
import string
from bs4 import BeautifulSoup


def clean_html(html):

    # parse html content
    soup = BeautifulSoup(html, 'html.parser')

    for data in soup(['style', 'script', 'code', 'a']):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

def clean_string(text, stem="None"):

    final_string = ""

    # Make lower
    text = text.lower()

    # Remove line breaks
    text = re.sub(r'\n', '', text)

    # Remove puncuation
    # translator = str.maketrans('', '', string.punctuation)
    # text = text.translate(translator)

    # Remove stop words
    text = text.split()
    useless_words = nltk.corpus.stopwords.words("english")
    useless_words = useless_words + ['hi', 'im']

    text_filtered = [word for word in text if not word in useless_words]

    # Remove numbers
    text_filtered = [re.sub(r'\w*\d\w*', '', w) for w in text_filtered]

    # Stem or Lemmatize
    # if stem == 'Stem':
    #     stemmer = PorterStemmer() 
    #     text_stemmed = [stemmer.stem(y) for y in text_filtered]
    # elif stem == 'Lem':
    #     lem = WordNetLemmatizer()
    #     text_stemmed = [lem.lemmatize(y) for y in text_filtered]
    # elif stem == 'Spacy':
    #     text_filtered = nlp(' '.join(text_filtered))
    #     text_stemmed = [y.lemma_ for y in text_filtered]
    # else:
    #     text_stemmed = text_filtered

    # final_string = ' '.join(text_stemmed)
    final_string = ' '.join(text_filtered)

    return final_string