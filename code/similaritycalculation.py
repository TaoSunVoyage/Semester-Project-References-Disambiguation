
from nltk import ngrams
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from unidecode import unidecode
from collections import Counter
import math


def tokenize(s):
    """
    Tokenize a string into a list.
    Remove punctuations, stopwords.
    Remove accents.
    Remove single letter, e.g. J. Smith -> Smith.
    Use all letters in lower case.
    """
    tokenizer = RegexpTokenizer(r'\w+')
    intermediate = tokenizer.tokenize(s)
    stop = stopwords.words()
    return [unidecode(i.lower()) for i in intermediate if i.lower() not in stop and len(i) > 1]


def getNgrams(s, n):
    """
    Get the Ngrams list from a string.
    """
    return list(ngrams(tokenize(s), n))



# Transplant from the Scala code

def interSimilarity(a, b):
    """
    Caluclate the intersected similarity.
    """
    vec1 = Counter(a)
    vec2 = Counter(b)

    intersection = vec1 & vec2  # min(vec1[x], vec2[x])
    numerator = sum(intersection.values())

    sum1 = sum(vec1.values())
    sum2 = sum(vec2.values())
    denominator = sum1 + sum2

    if denominator:
            return 2 * float(numerator) / denominator
    else:
        return 0.0


def trigramSimilarity(s1, s2):
    """
    Caluclate the intersected similarity of Trigrams.
    """
    return interSimilarity(getNgrams(s1, 3), getNgrams(s2, 3))


def bigramSimilarity(s1, s2):
    """
    Caluclate the intersected similarity of Bigrams.
    """
    return interSimilarity(getNgrams(s1, 2), getNgrams(s2, 2))



def tokenSimilarity(s1, s2):
    """
    Caluclate the intersected similarity of Tokens.
    """
    return interSimilarity(tokenize(s1), tokenize(s2))



# Source: https://rosettacode.org/wiki/Longest_common_subsequence
# Change the return type

def lcs(a, b):
    """
    Return the list of the LCS of two lists.
    """
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = []
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result.insert(0, a[x-1])
            x -= 1
            y -= 1
    return result



def lcsSimilarity(s1, s2):
    """
    Calculate the LCS similarity.
    """
    t1 = tokenize(s1)
    t2 = tokenize(s2)
    minlen = min(len(t1), len(t2))
    if minlen:
        lcslen = len(lcs(t1, t2))
        return lcslen / minlen
    else:
        return 0.0

    
def matchSimilarity(s1, s2):
    """
    Calcualte the match similarity.
    """
    if s1==s2:
        return 1.0
    else:
        return 0.0
    
    
def my_max(l):
    if len(l) == 0:
        return 0
    else:
        return max(l)
    
def yearSimilarity(y1, y2):
    tokenizer = RegexpTokenizer(r'\d\d\d\d')
    y1_list = tokenizer.tokenize(y1)
    y2_list = tokenizer.tokenize(y2)
    return my_max([matchSimilarity(i, j) for i in y1_list for j in y2_list])




def featureVectorBuilder(ref, seed_ref):
    fv = dict()

    if 'author' in ref and 'author' in seed_ref:
        fv['authorBigram'] = max([bigramSimilarity(a1, a2) for a1 in ref['author'] for a2 in seed_ref['author']])
        fv['authorToken'] = max([tokenSimilarity(a1, a2) for a1 in ref['author'] for a2 in seed_ref['author']])
    else:
        fv['authorBigram'] = 0
        fv['authorToken'] = 0

    if 'title' in ref and 'title' in seed_ref:
        fv['titleTrigram'] = max([trigramSimilarity(t1, t2) for t1 in ref['title'] for t2 in seed_ref['title']])
        fv['titleToken'] = max([tokenSimilarity(t1, t2) for t1 in ref['title'] for t2 in seed_ref['title']])
    else:
        fv['titleTrigram'] = 0
        fv['titleToken'] = 0
        
    if 'publisher' in ref and 'publisher' in seed_ref:
        fv['publisherLCS'] = max([lcsSimilarity(p1, p2) for p1 in ref['publisher'] for p2 in seed_ref['publisher']])
    else:
        fv['publisherLCS'] = 0
    
    if 'year' in ref and 'year' in seed_ref:
        fv['yearMatch'] = max([yearSimilarity(y1, y2) for y1 in ref['year'] for y2 in seed_ref['year']])
    else:
        fv['yearMatch'] = 0

    return fv
