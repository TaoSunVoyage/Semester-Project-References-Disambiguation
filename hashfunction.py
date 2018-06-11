from nltk import bigrams
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from unidecode import unidecode


def splitName(s):
    """
    Split author's name into a list. 
    Remove punctuations, stopwords.
    Remove accents.
    Remove single letter, e.g. J. Smith -> Smith.
    Use all letters in lower case.
    """
    tokenizer = RegexpTokenizer(r'\w+')
    intermediate = tokenizer.tokenize(s)
    stop = stopwords.words()
    return [unidecode(i.lower()) for i in intermediate if i.lower() not in stop and len(i) > 2]


def getYear(yearStr):
    """
    Return a list of year.
    """
    tokenizer = RegexpTokenizer(r'\d{4}')
    year = tokenizer.tokenize(yearStr)
    return [int(y) for y in year]


def blurYear(yearStr):
    """
    Return a list of blurred year: [Year-1, Year, Year+1]
    """
    year = getYear(yearStr)
    blurList = []
    for y in year:
        blurList.append(y)
        blurList.append(y - 1)
        blurList.append(y + 1)
    return blurList


def getPage(pageStr):
    """
    Return a list of page numbers.
    """
    tokenizer = RegexpTokenizer(r'\d+')
    page = tokenizer.tokenize(pageStr)
    return sorted([int(p) for p in page])[:2]


def blurPage(pageStr):
    """
    Return a list of blurred page: [Page-1, Page, Page+1]
    """
    page = getPage(pageStr)
    blurList = []
    blurList.append(page)
    if len(page)>1:
        blurList.append([page[0], page[1]-1])
        blurList.append([page[0], page[1]+1])
        blurList.append([page[0]-1, page[1]])
        blurList.append([page[0]+1, page[1]])
        blurList.append([page[0]+1, page[1]-1])
        blurList.append([page[0]-1, page[1]-1])
        blurList.append([page[0]+1, page[1]+1])
        blurList.append([page[0]-1, page[1]+1])
    elif len(page)==1:
        blurList.append([page[0]+1])
        blurList.append([page[0]-1])
    return blurList


def getBigram(s):
    """
    Return a list of bigrams from one sequence.
    Remove stopwords but keep numbers.
    Remove punctuations, accents.
    Use all letters in lower case.
    """
    tokenizer = RegexpTokenizer(r'\w+')
    stop = stopwords.words()
    token = [unidecode(i.lower()) for i in tokenizer.tokenize(s) if i.lower() not in stop and len(i) > 2]
    return set(bigrams(token))


def getNum(citation):
    """
    Get sorted numbers from citations, except year.
    """
    tokenizer = RegexpTokenizer(r'\d+')
    num_all = tokenizer.tokenize(citation['surface'])
    year = [y for ys in citation['year'] for y in getYear(ys)]
    return sorted([int(n) for n in num_all if int(n) not in year])


class HashGenerator:
    """

    """
    def __init__(self):
        super().__init__()
        self.name = 'Hash Generator'
        
    def generate(self, citation):
        raise NotImplementedError 

        
class CitationBaselineHashGenerator(HashGenerator):
    """
    Hash Generator with Everything.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Baseline'
        
    def generate(self, citation):
        surface = citation['surface']
        tokenizer = RegexpTokenizer(r'\w+')
        stop = stopwords.words()
        token = [unidecode(i.lower()) for i in tokenizer.tokenize(surface) if i.lower() not in stop and len(i) > 2]
        yield "#".join(token)


class CitationAuthorHashGenerator(HashGenerator):
    """
    Hash Generator with only Author.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Author'
        
    def generate(self, citation):
        for author in citation['author']:
            aName = splitName(author) 
            for a in aName[:4]:  # Take only the first four in author as hash
                yield a


class CitationTitleHashGenerator(HashGenerator):
    """
    Hash Generator with the Bigrams of Title.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Bigrams of Title'
        
    def generate(self, citation):
        for title in citation['title']:
            tBigram = getBigram(title)
            for t in tBigram: 
                yield t[0]+"#"+t[1]


class CitationAuthorTitleHashGenerator(HashGenerator):
    """
    Hash Generator with Author and the Bigrams of Title.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Author + Bigrams of Title'
        
    def generate(self, citation):
        for author in citation['author']:
            for title in citation['title']:
                aName = splitName(author) 
                tBigram = getBigram(title)
        
                for a in aName[:4]:  # Take only the first four in author as hash
                    for t in tBigram: 
                        yield a+"#"+t[0]+"#"+t[1]

                
class CitationAuthorYearHashGenerator(HashGenerator):
    """
    Hash Generator with Author and Year.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Author + Year'
        
    def generate(self, citation):
        for author in citation['author']:
            for year in citation['year']:
                aName = splitName(author)
                yNum  = getYear(year)
        
                for a in aName[:4]:  # Take only the first four in author as hash
                    for y in yNum: 
                        yield a+"#"+str(y)


class CitationAuthorBlurYearHashGenerator(HashGenerator):
    """
    Hash Generator with Author and Blurred Year.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Author + Blurred Year'
        
    def generate(self, citation):
        for author in citation['author']:
            for year in citation['year']:
                aName = splitName(author)
                yNum  = blurYear(year)
        
                for a in aName[:4]:  # Take only the first four in author as hash
                    for y in yNum: 
                        yield a+"#"+str(y)


class CitationAuthorYearPageHashGenerator(HashGenerator):
    """
    Hash Generator with Author, Year and Page.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Author + Year + Page'
        
    def generate(self, citation):
        for author in citation['author']:
            for year in citation['year']:
                for page in citation['page']:
                    aName = splitName(author)
                    yNum  = getYear(year)
                    pNum  = getPage(page)
        
                    for a in aName[:4]:  # Take only the first four in author as hash
                        for y in yNum:
                            s = a+"#"+str(y)
                            for p in pNum:
                                s = s+"#"+str(p)
                            yield s

                                
class CitationAuthorBlurYearPageHashGenerator(HashGenerator):
    """
    Hash Generator with Author, Blured Year and Blured Page.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Author + Blured Year + Blured Page'
        
    def generate(self, citation):
        for author in citation['author']:
            for year in citation['year']:
                for page in citation['page']:
                    aName = splitName(author)
                    yNum  = blurYear(year)
                    pNum  = blurPage(page)
        
                    for a in aName[:4]:  # Take only the first four in author as hash
                        for y in yNum:
                            for ps in pNum:
                                s = a+"#"+str(y)
                                for p in ps:
                                    s = s+"#"+str(p)
                                yield s
    
                
class CitationAuthorTitleYearHashGenerator(HashGenerator):
    """
    Hash Generator with Author, Bigrams of Title and Year.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Author + Bigrams of Title + Year'
        
    def generate(self, citation):
        for author in citation['author']:
            for title in citation['title']:
                for year in citation['year']:
                    aName = splitName(author)
                    tBigram = getBigram(title)
                    yNum  = getYear(year)
        
                    for a in aName[:4]:  # Take only the first four in author as hash
                        for t in tBigram:
                            for y in yNum: 
                                yield a+"#"+t[0]+"#"+t[1]+"#"+str(y)


class CitationAuthorTitleBlurYearHashGenerator(HashGenerator):
    """
    Hash Generator with Author, Bigrams of Title and Blurred Year.
    """
    def __init__(self):
        super().__init__()
        self.name = 'Author + Bigrams of Title + Blurred Year'
        
    def generate(self, citation):
        for author in citation['author']:
            for title in citation['title']:
                for year in citation['year']:
                    aName = splitName(author)
                    tBigram = getBigram(title)
                    yNum  = blurYear(year)
        
                    for a in aName[:4]:  # Take only the first four in author as hash
                        for t in tBigram:
                            for y in yNum: 
                                yield a+"#"+t[0]+"#"+t[1]+"#"+str(y)


class CitationAuthorYearNumHashGenerator(HashGenerator):
    """
    Hash Generator with Author, Year, Num.
    """
    def __init__(self, n):
        super().__init__()
        self.name = 'Author + Year + Num'
        self.number = n
        
    def generate(self, citation):
        for author in citation['author']:
            for year in citation['year']:
                aName = splitName(author)
                yNum  = getYear(year)
                nNum  = getNum(citation)
                for a in aName[:4]:  # Take only the first four in author as hash
                    for y in yNum:
                        s = a+"#"+str(y)
                        for n in nNum[:self.number]:
                            s = s+"#"+str(n)
                        yield s


def hashCombined(citation):
    """
    Combined possible hash functions.
    """
    keys = citation.keys()
    
    if 'author' not in keys:
        print('We should have author information!')
        return None
    if 'title' not in keys:
        print('We should have title information!')   
        return None
    
    # Baseline
    g0 = CitationBaselineHashGenerator()

    # Bigrams of Title
    g1 = CitationTitleHashGenerator()

    # Author + Year
    # g2 = CitationAuthorYearHashGenerator()
    g3 = CitationAuthorBlurYearHashGenerator()

    # Author + Year + Page
    # g4 = CitationAuthorYearPageHashGenerator()
    g5 = CitationAuthorBlurYearPageHashGenerator()

    # Author + Year + Num
    g6 = CitationAuthorYearNumHashGenerator(n=3)

    ###############Not in the Paper#################
    # Author
    # g7 = CitationAuthorHashGenerator()

    # Author + Title
    g8 = CitationAuthorTitleHashGenerator()

    # Author + Title + Year
    # g9 = CitationAuthorTitleYearHashGenerator()
    #g10 = CitationAuthorTitleBlurYearHashGenerator()
    
    hashList = []
    hashList += list(g0.generate(citation))  # Baseline
    hashList += list(g1.generate(citation))  # Title
    hashList += list(g8.generate(citation))  # Author + Title

#   hashList += list(g2.generate(citation))  # Author + Year
    hashList += list(g3.generate(citation))  # Author + Blurred Year

    hashList += list(g6.generate(citation))  # Author + Year + Num

    if 'page' in keys:
#        hashList += list(g4.generate(citation))  # Author + Year + Page
        hashList += list(g5.generate(citation))  # Author + Blurred Year + Blurred Page

    return list(set(hashList))