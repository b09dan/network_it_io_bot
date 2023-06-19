import nltk
from nltk.corpus import wordnet

nltk.download('omw-1.4')
nltk.download("wordnet")

def get_synonyms(word):
    synonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

word = "good"
synonyms = get_synonyms(word)
print(synonyms)

