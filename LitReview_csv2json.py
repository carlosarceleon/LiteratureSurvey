import json
import pandas as pd
import numpy as np
import re

data = pd.read_table('LitMatrix2.tsv',
        sep='\t',
        )

listOfDicts = []

def conformStr(string):
    return str(string).lstrip().rstrip()

def addEntry(df,keyword,exceptions,entryList):
    """ Adds an entry to the list

    Input [df]: a pandas dataframe
    Keyword: the classification of the entry
    Exceptions: a list of the classifications not to add

    """

    keys = []
    if isinstance(df.ix[ix],basestring):
        if '& ' in df.ix[ix]:
            keys = df.ix[ix].split('& ')
        elif '&' in df.ix[ix]:
            keys = df.ix[ix].split('&')
        else:
            keys = [df.ix[ix]]
    else:
        keys = [df.ix[ix]]
    print keys
    for k in keys:
        entryList.append(
                {
                    u"name"    :'LitReview.'+ conformStr(ix)+'.'+conformStr(k),
                    u"type"    : conformStr(ix),
                    u"imports" : []
                    }
                )
        for ix2 in df.index.values:
            if not ix2 in exceptions:
                if isinstance(df.ix[ix2],basestring) and '&' in df.ix[ix2]:
                    if '& ' in df.ix[ix2]:
                        keys = df.ix[ix2].split('& ')
                    if '&' in df.ix[ix2]:
                        keys = df.ix[ix2].split('&')
                    for k in keys:
                        entryList[-1][u'imports']\
                                .append(
                                        'LitReview.'+conformStr(ix2)+'.'+conformStr(k)
                                        )
                else:
                    entryList[-1][u'imports']\
                            .append(
                                    'LitReview.'+conformStr(ix2)+'.'+conformStr(df.ix[ix2])
                                    )


for row in data.index.values:
    df = data.ix[row].dropna()
    for ix in df.index.values:
        if ix == "Paper":
            listOfDicts.append(
                    {
                        u"name"    :'LitReview.'+ ix+'.'+conformStr(df.ix[ix]),
                        u"type"    : conformStr(ix),
                        #u"year"    : int(df.ix[ix][-4  : ]),
                        u"year"    : int(re.search('[0-9]+',df.ix[ix]).group(0)),
                        u"imports" : []
                        }
                    )
            for ix2 in df.index.values:
                if not ix2 == "Paper":
                    if isinstance(df.ix[ix2],basestring) and '&' in df.ix[ix2]:
                        if '& ' in df.ix[ix2]:
                            keys = df.ix[ix2].split('& ')
                        if '&' in df.ix[ix2]:
                            keys = df.ix[ix2].split('&')
                        for k in keys:
                            listOfDicts[-1][u'imports']\
                                    .append(
                                            'LitReview.'+conformStr(ix2)+'.'+conformStr(k)
                                            )
                    else:
                        listOfDicts[-1][u'imports']\
                                .append(
                                        'LitReview.'+conformStr(ix2)+'.'+conformStr(df.ix[ix2])
                                        )
        elif ix == 'Airfoils':
            NotToAdd = [
                    ix,
                    'Findings',
                    'Paper'
                    ]
            addEntry(df,ix,NotToAdd,listOfDicts)
        elif ix == 'Device':
            NotToAdd = [
                    ix,
                    'Paper'
                    ]
            addEntry(df,ix,NotToAdd,listOfDicts)
        elif ix == 'Device subtype':
            NotToAdd = [
                    ix,
                    'Paper'
                    ]
            addEntry(df,ix,NotToAdd,listOfDicts)
        else:
            addEntry(df,ix,df.index.values,listOfDicts)

def removeDups(dictList):
    """ Removes the duplicate imports in the given list of entries

    """
    finalDictList = []

    # Run through the elements
    for i in range(len(dictList)):
        # Run through the elements that will be crosschecked
        for j in range(len(dictList[i+1:])):
            # As long as they are not the same element
            # And only if they have the same name
            # And are not of type Paper
            # Then make an non duplicated list of all the imports found there 
            if not i==j \
                    and dictList[i]['name'] == dictList[j+i+1]['name'] \
                    and not dictList[i]['type'] == 'Paper': 
                dictList[i][u'imports'] = list(set(
                    dictList[i][u'imports'] + dictList[j+i+1][u'imports']
                    ))

        # Approve for adding
        Add = True

        # For the already selected elements, if this one coincides
        # with the name of any, don't add
        for fD in finalDictList:
            if dictList[i]['name'] == fD['name']:
                Add = False

        # Otherwise, add
        if Add:
            finalDictList.append(dictList[i])

    return finalDictList

listOfDicts = removeDups(listOfDicts)

f = open('litRev.json','w')
f.write('[\n')
for entry in listOfDicts:
    f.write(
            json.dumps(entry,indent=3)
            )
    if not entry == listOfDicts[-1]:
        f.write(',\n')
f.write(']\n')
f.close()
