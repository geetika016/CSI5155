import glob
import json
import pandas as pd
import numpy as np
import tldextract


def getnews(directory):
    ###Function to read news content in given directory using the FakeNewsNet dataset
    dictlist = []
    cols = ['title','text','authors','num_images','domain','url','keywords','canonical_link','publish_date','summary','movies','source']
    folders = glob.glob(directory+'/*')
    for index, subdir in enumerate(folders):
        file_path = glob.glob(subdir+'/*')
        #check if glob returned a valid file path (non-empty list)
        if len(file_path) == 1:
            file = open(file_path[0]).read()
            jsondata = json.loads(file)
            dictlist.append(scaledict(jsondata))
    return pd.DataFrame(dictlist,columns=cols)

def scaledict(ajson):
    #process json pulled from FakeNewsNet
    thedict = {'url':ajson['url'],'title':ajson['title'],'text':ajson['text'],'num_images':len(ajson['images']),'authors':str(ajson['authors']),'keywords':len(ajson['keywords']),'canonical_link':len(ajson['canonical_link']),'publish_date':ajson['publish_date'],'summary':ajson['summary'],'movies':ajson['movies'],'source':ajson['source']}
    ext = tldextract.extract(ajson['url'])
    thedict['domain'] = ext.domain
    return thedict

def cleandf(df,col,exclude):
    #loops through df columns and drops values located in exclude variable, both can be single values
    if type(col)=='list':
        try:
            for ind, c in enumerate(col):
                indices = df[df[c]==exclude[ind]].index
                df = df.drop(indices)
        except:
            print('Exception occurred, check kwargs')
    else:
        indices = df[df[col]==exclude].index
        df = df.drop(indices)
    return df
