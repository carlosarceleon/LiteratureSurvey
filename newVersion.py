import json
import pandas as pd
import numpy as np

data = pd.read_table('LitMatrix.csv',
        sep=';',
        )

listOfDicts = []

def addEntry(df,keyword,exceptions,entryList):

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
    for k in keys:
        entryList.append(
                {
                    u"name"    :'LitReview.'+ str(ix).lstrip().replace(' ','_')+'.'+str(k).lstrip().replace(' ','_'),
                    u"type"    : ix.lstrip().replace(' ','_'),
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
                        entryList[-1][u'imports'].append(
                                'LitReview.'+str(ix2)\
                                        .lstrip()\
                                        .replace(' ','_')+'.'+str(k)\
                                        .lstrip()\
                                        .replace(' ','_'))
                else:
                    entryList[-1][u'imports']\
                            .append('LitReview.'+str(ix2)\
                            .lstrip()\
                            .replace(' ','_')+'.'+str(df.ix[ix2])\
                            .lstrip()\
                            .replace(' ','_'))


for row in data.index.values:
    df = data.ix[row].dropna()
    for ix in df.index.values:
        if ix == "Paper":
            listOfDicts.append(
                    {
                        u"name"    :'LitReview.'+ ix+'.'+df.ix[ix].lstrip().replace(' ','_'),
                        u"type"    : ix.lstrip().replace(' ','_'),
                        u"year"    : int(df.ix[ix][-4  : ]),
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
                            .append('LitReview.'+str(ix2)\
                            .lstrip()\
                            .replace(' ','_')+'.'+str(k)\
                            .lstrip()\
                            .replace(' ','_'))
            else:
                listOfDicts[-1][u'imports']\
                        .append('LitReview.'+str(ix2)\
                        .lstrip()\
                        .replace(' ','_')+'.'+str(df.ix[ix2])\
                        .lstrip()\
                        .replace(' ','_'))
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
    
    # By default, don't add
    Add = True 

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
print listOfDicts

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
