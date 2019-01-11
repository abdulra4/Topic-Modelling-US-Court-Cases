import os, sys, random, codecs
import pickle, datetime, logging
# import memory_profiler, line_profiler

import xml.etree.cElementTree as ET
import pandas as pd
import numpy as np

import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models.ldamulticore import LdaMulticore

class TopicModel():

    def createCorpus(self, corpuspath, dataframe):
        #Create files from dataframe and dump them into folder
        for index, r in dataframe.iterrows():
            id=r['citation']
            title=r['name']
            body=r['text']
            category=r['type']
            fname=str(category)+'_'+str(id)+'.txt'
            corpusfile=open(corpuspath+'/'+fname,'a')
            corpusfile.write(str(body) +" " +str(title))
            corpusfile.close()

        #Load corpus into after conversion
        #Read contents of all the articles into a list and randomly sample them
        articlepaths = [os.path.join(corpuspath,p) for p in os.listdir(corpuspath)]

        doc_complete = []
        for path in articlepaths:
            try:
                fp = codecs.open(path, 'r', 'utf-8', errors='ignore')
                doc_content = fp.read()
                doc_complete.append(doc_content)

            #Note that this is to prevent issues with ipynb.checkpoints which come up as directories
            except IsADirectoryError:
                pass

        #Randomly sample articles from the corpus created
        docs_all = random.sample(doc_complete, len(doc_complete))
        # docs = open("docs_law.pkl", 'wb')
        # pickle.dump(docs_all, docs)

        return docs_all

    def cleanWords(self, doc):
        #Using methods from NLTK to clean articles
        stop = set(stopwords.words('english'))
        lemma = WordNetLemmatizer()

        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        normalized = " ".join(lemma.lemmatize(word,'v') for word in stop_free.split())
        x = normalized.split()
        y = [s for s in x if len(s) > 2]
        return y

    def filterWords(self, docs):
        #Filter words for stopwords using a dict
        dict_clean = corpora.Dictionary(docs)
        stoplist = set('court case upon cause ariz. p.3d id. p.2d fee claim argue party court’s  a.r.s.\
                    must ought also use make know many call include part find become like whether apply\
                    often different usually take come give well get since type list say change see \
                    may pursuant determine require actually would way something need things want every\
                    conclude provide summary section'.split())
        stop_ids = [dict_clean.token2id[stopword] for stopword in stoplist if stopword in dict_clean.token2id]
        dict_clean.filter_tokens(stop_ids)

        return dict_clean

    def ldaModel(self, dict_clean, doc_clean, topics, passes):
        #Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above
        term_matrix = [dict_clean.doc2bow(doc) for doc in doc_clean]

        #Creating the object for LDA model using gensim library & Training LDA model on the document term matrix.
        ldamodel = LdaModel(term_matrix, id2word=dict_clean, num_topics=topics, passes=passes)

        #Saving LDA into a file
        # ldafile = open('lda_model.pkl','wb')
        # pickle.dump(ldamodel,ldafile)
        # ldafile.close()

        return ldamodel
